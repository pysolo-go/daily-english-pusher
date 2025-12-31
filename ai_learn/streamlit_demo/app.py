import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- Page Config ---
st.set_page_config(
    page_title="AI Chat & Translator",
    page_icon="🤖",
    layout="wide"
)

# --- Init Environment ---
# Load env from two levels up (root of project)
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent.parent
env_path = root_dir / '.env'
if env_path.exists():
    load_dotenv(env_path)

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

if not api_key:
    st.error("🚨 OPENAI_API_KEY not found! Please check your .env file.")
    st.stop()

# --- Sidebar: Settings ---
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Mode Selection
    app_mode = st.radio(
        "Choose Mode",
        ["Chat Assistant", "Translator"]
    )
    
    st.divider()
    
    # Model Settings (Simplified for demo)
    temperature = st.slider(
        "Temperature (Creativity)", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.7,
        help="Controls randomness: 0.0 is focused/deterministic (good for facts/code), 1.0 is creative/random (good for stories)."
    )
    
    if app_mode == "Translator":
        target_lang = st.selectbox(
            "Target Language",
            ["English", "Chinese (Simplified)", "Japanese", "French", "Spanish", "German"]
        )
        tone = st.selectbox(
            "Tone",
            ["Neutral", "Formal", "Casual", "Academic"],
            help="""
            Style of translation:
            - Neutral: Standard/Balanced.
            - Formal: Professional/Business (e.g., 'Please be advised').
            - Casual: Slang/Friendly (e.g., 'What's up?').
            - Academic: Scholarly/Complex (e.g., 'It is hypothesized that').
            """
        )

# --- Main Interface ---
st.title("🤖 AI Assistant")

# Initialize Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Logic ---
def get_llm():
    return ChatOpenAI(
        model="Qwen/Qwen2.5-7B-Instruct",
        openai_api_key=api_key,
        openai_api_base=base_url,
        temperature=temperature
    )

def handle_chat(prompt_text):
    llm = get_llm()
    
    # Simple Chat Logic
    # In a real app, we would pass history to the LLM
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful and friendly AI assistant."),
        ("user", "{text}")
    ])
    
    chain = prompt_template | llm | StrOutputParser()
    
    return chain.stream({"text": prompt_text})

def handle_translation(text, lang, tone):
    llm = get_llm()
    
    system_msg = f"You are a professional translator. Translate the following text into {lang}. Tone: {tone}."
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("user", "{text}")
    ])
    
    chain = prompt_template | llm | StrOutputParser()
    return chain.stream({"text": text})

# --- User Input ---
if user_input := st.chat_input("Type your message here..."):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. AI Response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        if app_mode == "Chat Assistant":
            stream = handle_chat(user_input)
        else:
            stream = handle_translation(user_input, target_lang, tone)
            
        for chunk in stream:
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")
            
        response_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
