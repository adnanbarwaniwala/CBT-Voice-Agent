import streamlit as st
from audio_recorder_streamlit import audio_recorder
from groq import Groq
from openai import OpenAI
from prompts import *
import time

groq_api_key = os.getenv('GROQ_API_KEY')
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

st.set_page_config(
    page_title="CBT Voice Agent",
    page_icon='🧠'
)

st.title("🎙️ CBT Voice Agent 🫂")
st.markdown("**Hi there! Express your feelings by clicking on the voice recorder. How can I help you today?**")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

def speech_to_text(path):
    with st.spinner('Converting audio to text...'):
        # Initialize the Groq client
        client = Groq(api_key=groq_api_key)
        # Open the audio file
        with open(path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(path, file.read()),
                model="distil-whisper-large-v3-en",
                prompt="Specify context or spelling",
                response_format="json",
                temperature=0.0
            )

    with st.expander("👦🏻 User Query"):
        st.markdown("### 👦🏻 User Query")
        st.markdown(f"**{transcription.text.strip()}**")
    st.divider()
    return transcription.text


def analysis_agent_node(state):
    with st.spinner("Analysis Agent..."):
        messages = [{'role': 'system', 'content': analysis_agent_system_prompt}]
        if len(st.session_state.messages) != 0:
            messages.extend(st.session_state.messages)
        messages.extend(state['messages'])

        client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
        )
    with st.sidebar:
        with st.expander("Analysis Agent Reasoning"):
                st.write(response.choices[0].message.reasoning_content)
        with st.expander("Analysis Agent Final Answer"):
                st.write(response.choices[0].message.content)

    return {'analysis': response.choices[0].message.content}


def intervention_agent_node(state):
    with st.spinner("Intervention Agent..."):
        messages = [
            {'role': 'system', 'content': intervention_agent_system_prompt},
            {'role': 'user', 'content': f"Output from the Analysis Agent: \n```{state['analysis']}```"}
        ]
        client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
        )

    with st.sidebar:
        with st.expander("Intervention Agent Reasoning"):
            st.write(response.choices[0].message.reasoning_content)
        with st.expander("Intervention Agent Final Answer"):
            st.write(response.choices[0].message.content)

    return {'intervention': response.choices[0].message.content}


def support_and_feedback_agent_node(state):
    with st.spinner("Support and Feedback Agent..."):
        messages = [
            {'role': 'system', 'content': support_and_feedback_agent_system_prompt},
            {'role': 'user', 'content': f"Output from the Intervention Agent: \n```{state['intervention']}```"}
        ]
        client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
        )

    with st.sidebar:
        with st.expander("Support and Feedback Agent Reasoning"):
            st.write(response.choices[0].message.reasoning_content)
        with st.expander("Support and Feedback Agent Final Answer"):
            st.write(response.choices[0].message.content)

    return {'messages': [{'role': 'assistant', 'content': response.choices[0].message.content}]}


def create_graph():
    from langgraph.graph import StateGraph, END
    from typing import TypedDict, List, Sequence, Annotated
    import operator

    class AgentState(TypedDict):
        analysis: str
        intervention: str
        messages:  Annotated[List[dict[str, str]], operator.add]

    graph = StateGraph(AgentState)

    graph.add_node('analysis_agent', analysis_agent_node)
    graph.add_node('intervention_agent', intervention_agent_node)
    graph.add_node('support_and_feedback_agent', support_and_feedback_agent_node)

    graph.set_entry_point("analysis_agent")
    graph.add_edge("analysis_agent", "intervention_agent")
    graph.add_edge("intervention_agent", "support_and_feedback_agent")
    graph.add_edge("support_and_feedback_agent", END)

    app = graph.compile()
    return app


def model_response_to_audio(response):
    import io
    from elevenlabs.client import ElevenLabs
    client = ElevenLabs(api_key=elevenlabs_api_key)
    with st.spinner('Converting response to audio...'):
        try:
            audio_generator = client.generate(text=response, voice="Jessica", model="eleven_multilingual_v2")
            audio_buffer = io.BytesIO()
            for chunk in audio_generator:
                audio_buffer.write(chunk)
        except Exception:
            st.write("The text-to-speech (tts) API character quota has been reached. Unfortunately you'll only be",
                     "to use the tts ability of the app next month now. Sorry for the inconvenience!!")
            return "error"

    audio_buffer.seek(0)
    return audio_buffer


def autoplay_audio(audio_buffer):
    if audio_buffer != "error":
        import base64
        with st.spinner('Final audio processing...'):
            audio_bytes = audio_buffer.read()
            base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
            audio_html = f'<audio src="data:audio/mp3;base64,{base64_audio}" controls autoplay>'

        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        return


def display_elpased_time(start, end):
    elapsed = int(end - start)
    elapsed_mins = elapsed // 60
    elapsed_seconds = elapsed - (elapsed_mins * 60)

    timer_html = f"""
            <div style="
                background-color: #222;
                color: #fff;
                border: 1px solid #4CAF50;
                border-radius: 5px;
                padding: 5px 10px;
                display: inline-block;
                margin: 10px 0;">
              ⏱️ Reasoned for {elapsed_mins} minutes and {elapsed_seconds} seconds
            </div>
            """
    st.markdown(timer_html, unsafe_allow_html=True)


audio_bytes = audio_recorder(pause_threshold=3.0, text='Express your feelings:',)
file_path = "recorded_audio.wav"

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")  # Play the recorded audio
    start_time = time.time()

    with open(file_path, "wb") as f:
        f.write(audio_bytes) # Saving the audio file locally
    user_query = speech_to_text(file_path) # Converting question in audio form to text

    master_agent = create_graph()
    result = master_agent.invoke({'messages': [{'role': 'user', 'content': user_query}]})
    audio_buffer = model_response_to_audio(result['messages'][-1]['content'])

    end_time = time.time()
    display_elpased_time(start_time, end_time)
    autoplay_audio(audio_buffer)

    st.session_state.messages.append(result['messages'][-2])
    st.session_state.messages.append(result['messages'][-1])

    with st.expander("🤖 Model Response", expanded=True):
        st.markdown("### 🤖 Model Response")
        st.markdown(f"{result['messages'][-1]['content']}")
    st.divider()

    with st.expander("📜 Chat History"):
        st.markdown("### 📜 Chat History")
        for i, msg in enumerate(st.session_state.messages):
            if i % 2 == 0:
                with st.chat_message('Human'):
                    st.markdown(msg['content'])
            else:
                with st.chat_message('AI'):
                    st.markdown(msg['content'])
