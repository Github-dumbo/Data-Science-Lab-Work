import streamlit as st
import random
import time
from openai import OpenAI

# --- CONFIGURATION & STYLING ---

# Production URL or local environment
st.set_page_config(
    page_title="Spiral™ – The Overthinking Simulator",
    page_icon="💀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def inject_styles():
    """Injects custom CSS for a premium neon-dark aesthetic."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

        /* Main app styling */
        .stApp {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Poppins', sans-serif;
        }

        /* Centered Layout */
        .main .block-container {
            max-width: 500px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Hide Streamlit Header/Footer */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}

        /* Neon Glow Input */
        .stTextInput > div > div > input {
            background-color: #121212 !important;
            color: white !important;
            border: 2px solid #4cc9f0 !important;
            border-radius: 15px !important;
            padding: 15px !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease;
            box-shadow: 0 0 10px rgba(76, 201, 240, 0.2);
        }
        .stTextInput > div > div > input:focus {
            box-shadow: 0 0 20px rgba(76, 201, 240, 0.5);
            border-color: #7209b7 !important;
        }

        /* Neon Glow Buttons */
        .stButton > button {
            background: linear-gradient(45deg, #4cc9f0, #7209b7);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 12px 30px;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 4px 15px rgba(114, 9, 183, 0.3);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 0 25px rgba(76, 201, 240, 0.6);
            color: white !important;
        }
        .stButton > button:active {
            transform: scale(0.98);
        }

        /* Chaos Meter (Progress Bar) Customization */
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #4cc9f0, #7209b7, #f72585);
        }

        /* Thought Card Styling */
        .thought-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            animation: fadeIn 0.8s ease-out forwards;
            text-align: center;
            min-height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .thought-text {
            font-size: 1.25rem;
            line-height: 1.6;
            margin-bottom: 0;
            font-style: italic;
        }

        .level-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 15px;
            letter-spacing: 1.5px;
        }

        h1 {
            font-weight: 800;
            background: linear-gradient(to right, #4cc9f0, #f72585);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }
        
        .tagline {
            text-align: center;
            color: #888;
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }

        /* Custom Information Box */
        .stInfo {
            background-color: rgba(76, 201, 240, 0.1) !important;
            border: 1px solid #4cc9f0 !important;
            color: #4cc9f0 !important;
            border-radius: 15px !important;
        }
        </style>
    """, unsafe_allow_html=True)

# --- AI ENGINE ---

# OpenAI Client Setup (Included API Key as requested)
OPENAI_API_KEY = "sk-5678mnop5678mnop5678mnop5678mnop5678mnop"
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_spiral(user_input):
    """Generates 15 escalating thoughts using OpenAI API."""
    try:
        system_msg = (
            "You are an expert at simulating human overthinking. Generate realistic, relatable, "
            "slightly dramatic internal thoughts based on a situation. The thoughts should escalate "
            "gradually from logical to chaotic. Keep it natural, varied, and human-like. Avoid repetition."
        )
        
        user_msg = f"""
        User input situation: "{user_input}"
        
        Generate exactly 15 thoughts:
        - Numbers 1-3: Logical reasoning
        - Numbers 4-6: Subtle Doubt
        - Numbers 7-9: Growing Anxiety
        - Numbers 10-12: Full Overthinking
        - Numbers 13-15: Pure Chaos
        
        Format the output as a numbered list:
        1. [Thought]
        2. [Thought]
        ... and so on.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.8,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content
        thoughts = []
        for line in content.strip().split('\n'):
            if ". " in line:
                thought = line.split(". ", 1)[1].strip()
                if thought:
                    thoughts.append(thought)
                    
        if len(thoughts) >= 12:
            return thoughts[:15]
        return None
    except Exception as e:
        st.error(f"Something went wrong… try again (Error: {str(e)})")
        return None

# --- UI COMPONENTS ---

def render_header():
    st.markdown("<h1>Spiral™</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>One thought… then 47 more you didn’t ask for 💀</p>", unsafe_allow_html=True)

def render_spiral_step(idx, spiral_list):
    """Renders a single thought card with the appropriate intensity level."""
    # Intensity logic
    if idx < 3:
        name, color = "Logical", "#4cc9f0"
    elif idx < 6:
        name, color = "Doubt", "#4895ef"
    elif idx < 9:
        name, color = "Anxiety", "#7209b7"
    elif idx < 12:
        name, color = "Overthinking", "#b5179e"
    else:
        name, color = "CHAOS", "#f72585"

    st.markdown(f"""
        <div class='thought-card'>
            <span class='level-badge' style='background-color: {color}; color: white;'>Phase: {name}</span>
            <p class='thought-text'>"{spiral_list[idx]}"</p>
        </div>
    """, unsafe_allow_html=True)

def main():
    inject_styles()
    
    # Session State Initialization
    if 'state' not in st.session_state:
        st.session_state.state = "INPUT"
        st.session_state.spiral_list = []
        st.session_state.current_idx = 0
        st.session_state.last_input = ""

    if st.session_state.state == "INPUT":
        render_header()
        user_input = st.text_input("", placeholder="What’s on your mind...?", key="main_input")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Start Spiral 💀"):
                if not user_input.strip():
                    st.error("You need at least ONE problem to overthink 💀")
                else:
                    with st.spinner("Initializing Overthinking Engine..."):
                        results = generate_spiral(user_input)
                        if results:
                            st.session_state.spiral_list = results
                            st.session_state.last_input = user_input
                            st.session_state.state = "SPIRAL"
                            st.session_state.current_idx = 0
                            st.rerun()

    else:
        # Spiral View
        st.markdown(f"<h1>Situation: {st.session_state.last_input}</h1>", unsafe_allow_html=True)
        
        # Progress Bar / Chaos Meter
        idx = st.session_state.current_idx
        spiral = st.session_state.spiral_list
        progress = (idx + 1) / 15
        st.progress(progress)
        
        render_spiral_step(idx, spiral)
        
        # Controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Next Thought →"):
                if idx < 14:
                    st.session_state.current_idx += 1
                    st.rerun()
                else:
                    st.balloons()
                    st.success("You reached Peak Chaos! 🏆")
        
        with col2:
            if st.button("Reality Check 🧠"):
                checks = [
                    "Breathe. This thought isn't a fact.",
                    "You are safe. The world isn't ending.",
                    "Drink some water. Your brain is just tired.",
                    "Focus on the sound around you right now.",
                    "This problem is much smaller than it feels."
                ]
                st.info(random.choice(checks))

        st.markdown("---")
        if st.button("Restart 🔄"):
            st.session_state.state = "INPUT"
            st.session_state.current_idx = 0
            st.rerun()

if __name__ == "__main__":
    main()
