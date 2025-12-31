import streamlit as st
import json
import sys
from pathlib import Path

# Init environment
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(root_dir))

from ai_learn.comprehensive_demo.localization import init_lang, get_text, lang_selector, render_sidebar

# Init Language
init_lang()
lang = st.session_state.lang

st.set_page_config(page_title=get_text("Finetune_Data", "page_title", lang), page_icon="🛠️", layout="wide")

# Language Selector
lang_selector()

# Render Sidebar
render_sidebar()

# Page Content
st.title(get_text("Finetune_Data", "title", lang))

# Tabs
tab_guide, tab_editor = st.tabs([
    get_text("Finetune_Data", "tab_guide", lang),
    get_text("Finetune_Data", "tab_editor", lang)
])

# --- Tab 1: Concept Guide ---
with tab_guide:
    st.header(get_text("Finetune_Data", "guide_title", lang))
    st.markdown(get_text("Finetune_Data", "guide_intro", lang))
    
    st.divider()
    
    col_info, col_vis = st.columns([1, 1])
    
    with col_info:
        st.subheader(get_text("Finetune_Data", "guide_structure_title", lang))
        st.markdown(get_text("Finetune_Data", "guide_structure_desc", lang))
        st.info(get_text("Finetune_Data", "role_system", lang))
        st.warning(get_text("Finetune_Data", "role_user", lang))
        st.success(get_text("Finetune_Data", "role_assistant", lang))
        
    with col_vis:
        st.subheader("JSONL Example")
        st.code("""
{"messages": [
    {"role": "system", "content": "You are a math tutor."},
    {"role": "user", "content": "What is 2+2?"},
    {"role": "assistant", "content": "2+2 is 4."}
]}
{"messages": [
    {"role": "system", "content": "You are a code expert."},
    {"role": "user", "content": "Write a Python print function."},
    {"role": "assistant", "content": "print('Hello World')"}
]}
        """, language="json")
        st.caption("JSONL = JSON Lines. One complete JSON object per line.")

    st.divider()
    
    st.subheader(get_text("Finetune_Data", "quality_title", lang))
    st.markdown(get_text("Finetune_Data", "checklist_1", lang))
    st.markdown(get_text("Finetune_Data", "checklist_2", lang))
    st.markdown(get_text("Finetune_Data", "checklist_3", lang))

# --- Tab 2: Data Editor ---
with tab_editor:
    st.markdown(get_text("Finetune_Data", "description", lang))
    
    # Template Selection
    template_options = {
        "None": get_text("Finetune_Data", "template_none", lang),
        "Chat": get_text("Finetune_Data", "template_chat", lang),
        "Code": get_text("Finetune_Data", "template_code", lang),
        "Medical": get_text("Finetune_Data", "template_medical", lang)
    }
    
    selected_template_key = st.radio(
        get_text("Finetune_Data", "template_label", lang),
        options=list(template_options.keys()),
        format_func=lambda x: template_options[x],
        horizontal=True
    )
    
    # Template Logic
    default_system = "You are a helpful AI assistant."
    default_user = ""
    default_assistant = ""
    
    if selected_template_key == "Chat":
        default_system = "You are a witty and humorous friend."
        default_user = "Tell me a joke about programming."
        default_assistant = "Why do programmers prefer dark mode? Because light attracts bugs!"
    elif selected_template_key == "Code":
        default_system = "You are a Python expert. Provide efficient and commented code."
        default_user = "Write a function to calculate Fibonacci numbers."
        default_assistant = "def fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)"
    elif selected_template_key == "Medical":
        default_system = "You are a professional cardiologist. Provide accurate medical advice but always advise seeing a doctor."
        default_user = "I feel a sharp pain in my chest when I run."
        default_assistant = "Chest pain during exertion can be a sign of angina or other heart issues. Please stop exercising immediately and consult a cardiologist for a proper checkup."
    
    st.markdown("---")
    
    # Input Section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input (Context)")
        system_prompt = st.text_area(
            get_text("Finetune_Data", "system_label", lang), 
            value=default_system,
            height=100,
            key=f"sys_{selected_template_key}" # Unique key to force refresh on template change
        )
        user_input = st.text_area(
            get_text("Finetune_Data", "user_label", lang),
            value=default_user,
            height=150,
            placeholder="e.g., Explain Quantum Computing like I'm 5.",
            key=f"usr_{selected_template_key}"
        )
    
    with col2:
        st.subheader("Output (Target)")
        assistant_response = st.text_area(
            get_text("Finetune_Data", "assistant_label", lang),
            value=default_assistant,
            height=290,
            placeholder="e.g., Quantum computing is like a super maze solver...",
            key=f"ast_{selected_template_key}"
        )
    
    # Add Button
    if st.button(get_text("Finetune_Data", "add_btn", lang), type="primary"):
        if not user_input or not assistant_response:
            st.warning("Please fill in both User Input and Assistant Response.")
        else:
            # Construct OpenAI-format JSON structure
            new_entry = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": assistant_response}
                ]
            }
            
            # Save to session state
            if "dataset" not in st.session_state:
                st.session_state.dataset = []
            st.session_state.dataset.append(new_entry)
            st.success(get_text("Finetune_Data", "success_add", lang))
    
    # Preview Section
    if "dataset" in st.session_state and st.session_state.dataset:
        st.markdown("---")
        st.subheader(get_text("Finetune_Data", "preview_header", lang))
        
        # Convert list to JSONL string
        jsonl_output = ""
        for entry in st.session_state.dataset:
            jsonl_output += json.dumps(entry, ensure_ascii=False) + "\n"
        
        st.code(jsonl_output, language="json")
        st.caption(f"Total Records: {len(st.session_state.dataset)}")
        
        # Action Buttons
        c1, c2, c3 = st.columns([1, 1, 4])
        with c1:
            st.download_button(
                label=get_text("Finetune_Data", "download_btn", lang),
                data=jsonl_output,
                file_name="my_finetune_data.jsonl",
                mime="application/jsonl"
            )
        with c2:
            if st.button(get_text("Finetune_Data", "clear_btn", lang)):
                st.session_state.dataset = []
                st.rerun()
