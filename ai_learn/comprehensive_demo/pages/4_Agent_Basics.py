import streamlit as st
import sys
import io
import contextlib
import asyncio
import nest_asyncio
import concurrent.futures
from pathlib import Path

# Apply nest_asyncio to allow nested event loops (useful for Streamlit/Jupyter)
nest_asyncio.apply()

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(root_dir))

from ai_learn.rag_basics.rag_utils import init_rag_env
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai_like import OpenAILike
import requests
import wikipedia
from datetime import datetime

from ai_learn.comprehensive_demo.localization import init_lang, get_text, lang_selector, render_sidebar

# Init Language
init_lang()
lang = st.session_state.lang

st.set_page_config(page_title=get_text("Agent_Basics", "page_title", lang), page_icon="🤖")

# Language Selector
lang_selector()

# Render Sidebar
render_sidebar()

st.title(get_text("Agent_Basics", "title", lang))
st.markdown(get_text("Agent_Basics", "description", lang))

# 1. Define Tools
def multiply(a: int, b: int) -> int:
    """Multiply two integers and returns the result integer"""
    print(f"🛠️ Tool Triggered: multiply({a}, {b})")
    return a * b

def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    print(f"🛠️ Tool Triggered: get_weather({city})")
    try:
        # wttr.in format=3 gives a one-line summary: "City: Condition Temp"
        response = requests.get(f"https://wttr.in/{city}?format=3", timeout=10)
        if response.status_code == 200:
            return f"Weather info: {response.text.strip()}"
        else:
            return f"Could not fetch weather for {city} (Status: {response.status_code})"
    except Exception as e:
        return f"Error occurred while fetching weather: {str(e)}"

def search_wikipedia(query: str) -> str:
    """Search Wikipedia for a query and return the summary."""
    print(f"🛠️ Tool Triggered: search_wikipedia({query})")
    try:
        # Set language to English or auto-detect? Defaulting to English for broad coverage, 
        # but wikipedia library can switch languages. Let's stick to default (en) for stability 
        # or try to match query. For simplicity, we use default.
        # To support Chinese, we could set wikipedia.set_lang("zh") if query contains Chinese.
        
        # Simple heuristic for language
        if any("\u4e00" <= char <= "\u9fff" for char in query):
            wikipedia.set_lang("zh")
        else:
            wikipedia.set_lang("en")
            
        results = wikipedia.summary(query, sentences=2)
        return f"Wikipedia Summary for '{query}': {results}"
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found for '{query}': {e.options[:5]}"
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{query}'."
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"

def get_system_time() -> str:
    """Get the current system local time."""
    print(f"🛠️ Tool Triggered: get_system_time()")
    return f"Current System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# Helper function to run agent in a completely isolated thread
# This avoids all Event Loop conflicts in Streamlit/Tornado
def run_agent_isolated(prompt: str) -> str:
    
    # Define the async runner
    async def _run():
        # Initialize EVERYTHING inside the thread/loop
        # This ensures the HTTP client binds to the correct loop
        api_key, base_url = init_rag_env()
        
        llm = OpenAILike(
            model="deepseek-ai/DeepSeek-V3", 
            api_key=api_key, 
            api_base=base_url,
            temperature=0.1,
            is_chat_model=True
        )
        
        multiply_tool = FunctionTool.from_defaults(fn=multiply)
        weather_tool = FunctionTool.from_defaults(fn=get_weather)
        wiki_tool = FunctionTool.from_defaults(fn=search_wikipedia)
        time_tool = FunctionTool.from_defaults(fn=get_system_time)
        
        tools = [multiply_tool, weather_tool, wiki_tool, time_tool]
        
        agent = ReActAgent(tools=tools, llm=llm, verbose=True)
        return await agent.run(user_msg=prompt)

    # Run in a new loop
    return asyncio.run(_run())

# Execution Helper using ThreadPool
def execute_agent_safe(prompt):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(run_agent_isolated, prompt)
        return future.result()

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "logs" in msg and msg["logs"]:
            with st.expander(get_text("Agent_Basics", "history_logs", lang)):
                st.code(msg["logs"])

if prompt := st.chat_input(get_text("Agent_Basics", "input_placeholder", lang)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        logs_placeholder = st.expander(get_text("Agent_Basics", "reasoning_logs", lang), expanded=True)
        
        # Capture stdout to show tool usage
        f = io.StringIO()
        final_response = ""
        
        with contextlib.redirect_stdout(f):
            try:
                # Run agent in isolated thread
                response = execute_agent_safe(prompt)
                final_response = str(response)
            except Exception as e:
                final_response = f"Error: {e}"
                import traceback
                traceback.print_exc()
        
        logs = f.getvalue()
        
        # Display Logs
        if logs:
            logs_placeholder.code(logs)
        else:
            logs_placeholder.info(get_text("Agent_Basics", "no_logs", lang))
            
        message_placeholder.markdown(final_response)
        
        # Save to history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": final_response,
            "logs": logs
        })
