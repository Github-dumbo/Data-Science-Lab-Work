# MindMirror™ – Your Digital Psychological Twin

## Description
MindMirror™ is a premium, full-stack AI application designed to create a dynamic digital twin of a user's mind. It learns from your inputs, builds a real-time psychological profile (evaluating traits like overthinking, emotional reactivity, and logic), and can simulate how you would think, react, and respond in hypothetical scenarios. The system feels like a "digital version of your mind."

## Dataset
* **Source:** User-generated (Live Data)
* **Description of data:** The application starts with a blank slate and progressively builds a local Knowledge Graph & Psychological Profile via the `data/profile.json` and `data/memory.json` stores as the user interacts with the Input Engine.

## Steps Performed
1. **Frontend Architecture:** Initialized a modern Vite React application featuring a dark futuristic theme, Tailwind CSS styling, and Framer Motion micro-animations.
2. **Backend Architecture:** Developed a fast and robust Python FastAPI backend to handle API routing, state management, and CORS securely.
3. **AI Engine Integration:** Connected the OpenAI API using custom structured system prompts for accurate personality mapping, realistic twin chatting, and intricate scenario simulation.
4. **Data Persistence:** Implemented local JSON-based file storage to retain and build out the user's psychological memory long-term.
5. **Polishing / Refinement:** Built an intuitive sidebar layout, typing animations, progress chart metrics for traits, and robust API error handling.

## Results
* **Key findings:** Context-aware prompts drastically improve the realism of digital twins. By separating "Traits" from raw "Memory", the AI reliably simulates deep emotional responses to scenarios.
* **Metrics:** 
  - Dynamic 0-100% trait evaluation on 5 cognitive axes.
  - Multi-tiered simulation returning structured JSON for inner logic, emotion, and predicted decision.

## Tools Used
* **Python** (FastAPI, Uvicorn, Pydantic)
* **Frontend** (React, Vite, Tailwind CSS, Framer Motion, Lucide Icons)
* **AI/ML** (OpenAI `gpt-3.5-turbo` structured JSON outputs)

## How to Run

1. Clone or download the repository to your local machine:
   ```bash
   cd "MindMirror™ – Your Digital Psychological Twin"
   ```

2. **Install backend dependencies:**
   Ensure you have Python 3.9+ installed.
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies:**
   Ensure you have Node.js 18+ installed.
   ```bash
   cd frontend
   npm install
   ```

4. **Add OpenAI API key:**
   The backend logic utilizes the OpenAI key you've securely provided. To change it later, update `main.py` where `client = OpenAI(...)` is initiated.
   *(Note: hardcoded per system setup for immediate deployment testing.)*

5. **Run backend server:**
   ```bash
   # From the backend directory
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Run frontend:**
   ```bash
   # From the frontend directory, in a separate terminal
   npm run dev
   ```

7. **Open app in browser:**
   Navigate to `http://localhost:5173` (or the port Vite outputs) in your favorite web browser.

## Conclusion
MindMirror represents a robust architectural approach to personalized AI tools. By leveraging modern tech-stacks with granular prompting, the application successfully distills qualitative thoughts into quantitative matrices, enabling a stunningly accurate "Digital Psychological Twin". This can serve as an immersive tool for personal reflection and decision exploration.

## Author
Nehal Santosh Lashkar
