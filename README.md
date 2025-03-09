# 🎙️🧠 **CBT Voice Agent**

CBT Voice Agent is a voice-enabled assistant that provides personalized support using **Cognitive Behavioral Therapy (CBT)**. It allows users to express their feelings verbally, processes the input using an agentic workflow powered by the Deepseek-R1 LLM and LangGraph library, and delivers supportive, actionable advice through audio responses.

## 🚀 **Features**

- 🎤 **Voice Interaction**:
  - Speak directly to the app to express your feelings or concerns.
  - Speech is transcribed to text using the `OpenAI Whisper model`.
- 🤖 **AI-driven CBT Support**: Uses a structured, agentic workflow to provide targeted CBT interventions.
- 🗣️ **Natural Conversational Responses**:
  - Delivers empathetic and human-like audio responses.
  - The `Elevenlabs` library is used for text-to-speech.


## ⚙️ **Understanding the Agentic Workflow**:

The workflow is created using the `LangGraph library`. It uses three specialized AI agents. Each agent is powered by the `Deepseek-R1 LLM`. They work in this sequence:

### 1️⃣ **Analysis Agent 🔍**

- **Functionality**:  
  - Processes the transcribed user query.
  - Identifies underlying emotions, cognitive distortions, and thought patterns.

- **Output**:  
  Provides a structured analysis of the user's emotional state.

### 2️⃣ **Intervention Agent 🛠️**

- **Functionality**:  
  - Receives analysis from the Analysis Agent.
  - Designs targeted CBT interventions (e.g., cognitive restructuring, behavioral activation).
  - Uses structured Socratic questioning or CBT activities to guide the user.

- **Output**:  
  Generates a clear, actionable CBT strategy for the user's specific issue.

### 3️⃣ **Support & Feedback Agent 💬**

- **Functionality**:  
  - Receives the intervention from the Intervention Agent.
  - Adds empathetic validation, encouragement, and supportive feedback.
  - Prompts the user for reflection on their emotional state and intervention effectiveness.

- **Output**:  
  Delivers a supportive, empathetic, and complete audio response to the user.


## 🗃️ **Agentic Workflow Structure**

```
User Input (Audio) 🎙️
      │
      ├──► Speech-to-Text 🎧
      │
      └──► Analysis Agent 🔍
                  │
                  └──► Intervention Agent 🛠️
                              │
                              └──► Support & Feedback Agent 💬
                                          │
                                          ├──► Text-to-Speech 🎧
                                          │
                                          └──► User Receives Audio Response 🎙️
```

## 🧠 **Why CBT?**

The app leverages CBT principles to:

- Identify and challenge negative thought patterns (cognitive distortions).
- Provide practical coping strategies.
- Encourage positive behavioral changes through structured interventions.
- Deliver empathetic, validated emotional support.


## 📁 **Project Structure**

```bash
📂 CBT_Voice_Agent
│
├── 📄 LICENSE              # License information
├── 📄 README.md            # Project overview and documentation
├── 📄 requirements.txt     # Python dependencies
├── 📄 cbt_voice_agent.py   # Main application script (Streamlit app & agentic workflow)
└── 📄 prompts.py           # Prompt definitions for Analysis, Intervention, and Support Agents
```

## 📜 **License**

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please open an issue or contact me directly:

- **Email**: adnanbarwaniwala7@gmail.com

## 🙏 Thank You

Thank you for spending time on my repo. Hope you enjoyed it!
