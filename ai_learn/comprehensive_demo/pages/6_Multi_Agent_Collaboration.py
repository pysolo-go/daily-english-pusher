import streamlit as st
import sys
import asyncio
import nest_asyncio
from pathlib import Path
from typing import Union

# Apply nest_asyncio
nest_asyncio.apply()

# Add project root
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(root_dir))

from ai_learn.rag_basics.rag_utils import init_rag_env
from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    step,
    Context,
    Event
)
from llama_index.llms.openai_like import OpenAILike
from llama_index.core.llms import ChatMessage
from ai_learn.comprehensive_demo.localization import init_lang, get_text, lang_selector, render_sidebar

# Init Language
init_lang()
lang = st.session_state.lang

# -----------------------------------------------------------------------------
# Page Config
# -----------------------------------------------------------------------------
st.set_page_config(page_title=get_text("Multi_Agent", "page_title", lang), page_icon="🤝")

# Language Selector
lang_selector()

# Render Sidebar
render_sidebar()

st.title(get_text("Multi_Agent", "title", lang))
st.markdown(get_text("Multi_Agent", "description", lang))

# -----------------------------------------------------------------------------
# 1. Define Events (The "Handoff" Packets)
# -----------------------------------------------------------------------------
class ReportEvent(Event):
    """Event passed from Researcher to Writer containing raw facts."""
    topic: str
    facts: str

# -----------------------------------------------------------------------------
# 2. Define Workflow
# -----------------------------------------------------------------------------
class BlogCreationWorkflow(Workflow):
    def __init__(self, llm, timeout: int = 120, verbose: bool = False):
        super().__init__(timeout=timeout, verbose=verbose)
        self.llm = llm

    @step
    async def researcher_agent(self, ctx: Context, ev: StartEvent) -> ReportEvent:
        """
        Agent 1: The Researcher.
        Focuses purely on gathering information (simulated here via LLM knowledge).
        """
        topic = ev.get("topic")
        lang = st.session_state.get("lang", "zh")
        st.write(get_text("Multi_Agent", "researcher_start", lang).format(topic))
        
        # Researcher's System Prompt (Persona)
        system_prompt = get_text("Multi_Agent", "researcher_sys_prompt", lang)
        
        user_prompt = get_text("Multi_Agent", "researcher_user_prompt", lang).format(topic)
        
        # Simulate 'working'
        with st.status(get_text("Multi_Agent", "researcher_status", lang), expanded=True) as status:
            st.write(get_text("Multi_Agent", "researcher_step1", lang))
            st.write(get_text("Multi_Agent", "researcher_step2", lang))
            
            response = await self.llm.achat([
                ChatMessage(role="system", content=system_prompt),
                ChatMessage(role="user", content=user_prompt)
            ])
            facts = str(response.message.content)
            status.update(label=get_text("Multi_Agent", "researcher_complete", lang), state="complete", expanded=False)
            
        st.info(get_text("Multi_Agent", "researcher_output_header", lang).format(facts))
        
        # Handoff to the next agent
        return ReportEvent(topic=topic, facts=facts)

    @step
    async def writer_agent(self, ctx: Context, ev: ReportEvent) -> StopEvent:
        """
        Agent 2: The Writer.
        Focuses on narrative, flow, and formatting.
        """
        lang = st.session_state.get("lang", "zh")
        st.write(get_text("Multi_Agent", "writer_start", lang))
        
        # Writer's System Prompt (Persona)
        system_prompt = get_text("Multi_Agent", "writer_sys_prompt", lang)
        
        user_prompt = get_text("Multi_Agent", "writer_user_prompt", lang).format(ev.topic, ev.facts)
        
        with st.status(get_text("Multi_Agent", "writer_status", lang), expanded=True) as status:
            st.write(get_text("Multi_Agent", "writer_step1", lang))
            st.write(get_text("Multi_Agent", "writer_step2", lang))
            st.write(get_text("Multi_Agent", "writer_step3", lang))
            
            response = await self.llm.achat([
                ChatMessage(role="system", content=system_prompt),
                ChatMessage(role="user", content=user_prompt)
            ])
            blog_post = str(response.message.content)
            status.update(label=get_text("Multi_Agent", "writer_complete", lang), state="complete", expanded=False)

        return StopEvent(result=blog_post)

# -----------------------------------------------------------------------------
# 3. Execution Helper
# -----------------------------------------------------------------------------
def run_collaboration(topic: str):
    async def _run():
        api_key, base_url = init_rag_env()
        llm = OpenAILike(
            model="deepseek-ai/DeepSeek-V3", 
            api_key=api_key, 
            api_base=base_url,
            temperature=0.7,
            is_chat_model=True
        )
        
        workflow = BlogCreationWorkflow(llm=llm, verbose=True, timeout=240)
        return await workflow.run(topic=topic)

    return asyncio.run(_run())

# -----------------------------------------------------------------------------
# 4. UI
# -----------------------------------------------------------------------------
# Initialize session state for result history if not exists
if "multi_agent_history" not in st.session_state:
    st.session_state.multi_agent_history = []  # List of dicts: {"topic": str, "content": str}

topic = st.text_input(
    get_text("Multi_Agent", "topic_input", lang), 
    value="The Future of Quantum Computing"
)

if st.button(get_text("Multi_Agent", "start_btn", lang)):
    if not topic:
        st.warning(get_text("Multi_Agent", "warning_topic", lang))
    else:
        try:
            final_result = run_collaboration(topic)
            
            # Append new result to history (at the beginning, so newest first)
            st.session_state.multi_agent_history.insert(0, {
                "topic": topic,
                "content": final_result
            })
            
        except Exception as e:
            st.error(get_text("Multi_Agent", "error", lang).format(e))
            import traceback
            st.code(traceback.format_exc())

# Display all history
if st.session_state.multi_agent_history:
    st.markdown("---")
    st.subheader("📜 Generated History / 生成历史")
    
    for i, item in enumerate(st.session_state.multi_agent_history):
        with st.expander(f"Topic: {item['topic']} (Latest)" if i == 0 else f"Topic: {item['topic']}", expanded=(i == 0)):
            st.markdown(item['content'])
