import streamlit as st
import sys
from pathlib import Path
from openai import OpenAI
import os
from dotenv import load_dotenv

# Init environment
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(root_dir))
load_dotenv(root_dir / ".env")

from ai_learn.comprehensive_demo.localization import init_lang, get_text, lang_selector, render_sidebar

# Init Language
init_lang()
lang = st.session_state.lang

st.set_page_config(page_title=get_text("Basic_Chat", "page_title", lang), page_icon="🤖")

# Language Selector
lang_selector()

# Render Sidebar
render_sidebar()

st.header(get_text("Basic_Chat", "header", lang))

# Sidebar settings
with st.sidebar:
    st.subheader(get_text("Basic_Chat", "model_config", lang))
    
    # Provider Selection
    provider_options = ["SiliconFlow (Cloud)", "Ollama (Local)"]
    provider_labels = {
        "SiliconFlow (Cloud)": "SiliconFlow (Cloud)",
        "Ollama (Local)": "Ollama (Local)"
    }
    selected_provider = st.selectbox(
        get_text("Basic_Chat", "provider_select", lang),
        provider_options
    )
    
    # Model Configuration based on Provider
    if selected_provider == "SiliconFlow (Cloud)":
        model_name = "deepseek-ai/DeepSeek-V3"
        base_url = "https://api.siliconflow.cn/v1"
        api_key = os.getenv("SILICONFLOW_API_KEY")
        st.caption(f"Default: {model_name}")
    else:
        # Local Ollama
        model_name = st.text_input(
            get_text("Basic_Chat", "model_select", lang), 
            value="qwen2.5:1.5b"
        )
        base_url = "http://localhost:11434/v1"
        api_key = "ollama" # Ollama doesn't require a real key
        st.caption("Ensure 'ollama serve' is running")

    temperature = st.slider(get_text("Basic_Chat", "temperature", lang), 0.0, 1.5, 0.7)
    system_prompt = st.text_area(
        get_text("Basic_Chat", "system_prompt", lang), 
        value=get_text("Basic_Chat", "system_prompt_default", lang)
    )

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input(get_text("Basic_Chat", "input_placeholder", lang)):
    # 1. Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Call API (Compatible with both SiliconFlow and Ollama)
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Stream response
            stream = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *st.session_state.messages
                ],
                temperature=temperature,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        # 3. Save assistant message
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(f"Error: {e}")
        if selected_provider == "Ollama (Local)":
            st.info("💡 Tip: Make sure Ollama is installed and running (`ollama serve`). Run `ollama pull <model>` to download the model.")
