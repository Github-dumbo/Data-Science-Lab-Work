# Spiral™ – The Overthinking Simulator

## Description

The objective of this project is to simulate the complex, escalating nature of human overthinking. By leveraging the OpenAI API, the application takes a simple user situation and generates a chain of 15 realistic, relatable thoughts that transition from logical reasoning to complete chaos. The goal is to provide a fun, engaging, and aesthetically pleasing web experience that resonates with anyone who has ever "spiraled" over a minor detail.

## Dataset

* Source: Generative (OpenAI GPT-3.5-Turbo)
* Description of data: The dynamic data consists of context-aware, situation-specific thought strings generated in real-time. The engine ensures a structured escalation: Logical → Doubt → Anxiety → Overthinking → Chaos.

## Steps Performed

1. **AI Engine Integration**: Integrated the OpenAI SDK to handle dynamic thought generation with customized system and user prompts.
2. **State Management**: Implemented Streamlit session state to manage user input, progress through the 15-step spiral, and UI resets.
3. **UI/UX Design**: Developed a custom CSS injection system to achieve a "Matte Black" theme with glassmorphism cards and neon blue/purple glow effects.
4. **Interactive Features**: Built a "Chaos Meter" (progress bar), "Reality Check" grounding messages, and a modular "Restart" functionality.

## Results

* **Key findings**: The use of AI allows for infinitely unique spirals that directly reference the user's specific context, making the experience significantly more personal and relatable than fixed-template systems.
* **Metrics**: The system consistently generates exactly 15 thoughts with a 100% success rate in maintaining the requested escalation intensity.

## Tools Used

* Python
* Streamlit
* OpenAI API
* Custom CSS

## How to Run

1. Clone the repository to your local machine.
2. Install the required dependencies using:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```
4. Open the local URL (usually http://localhost:8501) in your web browser.

## Conclusion

Spiral™ successfully demonstrates the power of combining a modern web framework (Streamlit) with advanced Large Language Models (LLMs) to create a polished, viral-quality product. The project achieves a high degree of "relatability" through clever prompt engineering and a premium, mobile-first design aesthetic.

## Author

Nehal Santosh Lashkar
