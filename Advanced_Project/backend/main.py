from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import datetime
from openai import OpenAI
from typing import List, Optional, Dict, Any

app = FastAPI(title="MindMirror API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI
# Using hardcoded key per user instructions for this demo
client = OpenAI(api_key="sk-ijkl1234ijkl1234ijkl1234ijkl1234ijkl1234")

# Paths for JSON storage
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
PROFILE_FILE = os.path.join(DATA_DIR, "profile.json")
MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")

def load_json(filepath: str, default: Any) -> Any:
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(filepath: str, data: Any):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

class AnalyzeRequest(BaseModel):
    input_text: str
    
class ChatRequest(BaseModel):
    message: str

class SimulateRequest(BaseModel):
    scenario: str

@app.get("/")
def read_root():
    return {"status": "MindMirror Backend Active"}

@app.get("/api/profile")
def get_profile():
    return load_json(PROFILE_FILE, {
        "traits": {
            "Overthinking": 0,
            "Emotional Reactivity": 0,
            "Logic & Reasoning": 0,
            "Social Confidence": 50,
            "Risk Tolerance": 50
        },
        "summary": "No profile built yet."
    })

@app.get("/api/memory")
def get_memory():
    return load_json(MEMORY_FILE, [])

@app.post("/api/analyze")
def analyze_input(req: AnalyzeRequest):
    try:
        # Load existing profile to give context to the AI
        current_profile = get_profile()
        
        system_prompt = f"""
        You are the Personality Engine for MindMirror. 
        Analyze the user's latest thought/input: "{req.input_text}"
        
        Current Profile: {json.dumps(current_profile)}
        
        Task:
        1. Adjust the user's personality traits based on this input. Traits are on a 0-100 scale: Overthinking, Emotional Reactivity, Logic & Reasoning, Social Confidence, Risk Tolerance.
        2. Provide a short, updated qualitative summary of how the user's mind works.
        3. Identify 1-2 new key psychological insights resulting from this input.
        
        Respond ONLY with a valid JSON in the exact structure:
        {{
            "traits": {{"Overthinking": int, "Emotional Reactivity": int, "Logic & Reasoning": int, "Social Confidence": int, "Risk Tolerance": int}},
            "summary": "string",
            "new_insights": ["string"]
        }}
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        result_text = response.choices[0].message.content.strip()
        # Parse JSON
        new_profile_data = json.loads(result_text)
        
        # Save updated profile
        save_json(PROFILE_FILE, new_profile_data)
        
        # Save to memory
        memories = get_memory()
        memories.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "input": req.input_text,
            "insights_generated": new_profile_data.get("new_insights", [])
        })
        save_json(MEMORY_FILE, memories)
        
        return {"status": "success", "profile": new_profile_data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
def twin_chat(req: ChatRequest):
    try:
        current_profile = get_profile()
        memories = get_memory()
        
        # Format memories for context
        memory_context = [m['input'] for m in memories[-10:]]
        
        system_prompt = f"""
        You are a Digital Psychological Twin of the user. 
        Think, react, and respond EXACTLY like them based on their personality profile.
        
        Personality Profile:
        {json.dumps(current_profile)}
        
        Recent Thoughts (Memory Context):
        {json.dumps(memory_context)}
        
        Task: Respond to the following message directly as the user would. Do not break character. 
        Let their traits (e.g. overthinking, emotional reactivity, logic) deeply influence your response style, tone, and depth.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.message}
            ],
            temperature=0.9, # Higher temp for more personality variance
            max_tokens=300
        )
        
        return {"response": response.choices[0].message.content.strip()}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/simulate")
def simulate_scenario(req: SimulateRequest):
    try:
        current_profile = get_profile()
        
        system_prompt = f"""
        You are the Simulation Engine for the MindMirror project. 
        Predict what this specific user would do in the following scenario, based strictly on their psychological profile.
        
        Personality Profile:
        {json.dumps(current_profile)}
        
        Scenario: "{req.scenario}"
        
        Task:
        Provide a step-by-step simulation of their internal reasoning, their emotional reaction, and their final predicted decision.
        
        Format your response EXACTLY as this JSON structure:
        {{
            "emotional_reaction": "string summarizing immediate feeling",
            "internal_reasoning": [
                "Step 1: thought...",
                "Step 2: thought..."
            ],
            "predicted_decision": "string explaining the final action they will take"
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system_prompt}],
            temperature=0.7,
            max_tokens=600
        )
        
        result_text = response.choices[0].message.content.strip()
        prediction = json.loads(result_text)
        
        return {"simulation": prediction}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # run with `uvicorn main:app --reload`
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
