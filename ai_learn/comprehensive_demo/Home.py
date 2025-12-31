import streamlit as st
import sys
from pathlib import Path

# Add project root to sys.path to allow importing from ai_learn
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))

from ai_learn.comprehensive_demo.localization import init_lang, lang_selector, get_text, render_sidebar

# Init Language
init_lang()
lang = st.session_state.lang

st.set_page_config(
    page_title=get_text("Home", "page_title", lang),
    page_icon="🚀",
    layout="wide"
)

# Language Selector (Top Right)
lang_selector()

# Render Sidebar
render_sidebar()

st.title(get_text("Home", "title", lang))

st.markdown(get_text("Home", "welcome", lang))

st.sidebar.success(get_text("Home", "sidebar_tip", lang))

