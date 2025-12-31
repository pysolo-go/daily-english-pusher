
import streamlit as st
import sys
import asyncio
import nest_asyncio
from pathlib import Path
from typing import Optional, Union

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
st.set_page_config(page_title=get_text("Agent_Workflow", "page_title", lang), page_icon="🔄")

# Language Selector
lang_selector()

# Render Sidebar
render_sidebar()

st.title(get_text("Agent_Workflow", "title", lang))
st.markdown(get_text("Agent_Workflow", "description", lang))

# -----------------------------------------------------------------------------
# 1. Define Events
# -----------------------------------------------------------------------------
class ReviewEvent(Event):
    joke: str

class FeedbackEvent(Event):
    feedback: str
    original_joke: str

# -----------------------------------------------------------------------------
# 2. Define Workflow
# -----------------------------------------------------------------------------
class JokeWorkflow(Workflow):
    def __init__(self, llm, timeout: int = 60, verbose: bool = False):
        super().__init__(timeout=timeout, verbose=verbose)
        self.llm = llm
        self.attempts = 0
        self.max_attempts = 3
        self.topic = None

    @step
    async def generate_joke(self, ctx: Context, ev: StartEvent) -> Union[ReviewEvent, StopEvent]:
        # Handle both StartEvent and FeedbackEvent manually since Union type hint in @step 
        # might be causing issues with older Python versions or specific library versions
        
        # Logic to determine if it's a retry is handled by checking internal state or event type
        # But here, LlamaIndex workflow engine routes events based on type annotation.
        # If we want to handle multiple input types, we can't easily do it in one function signature 
        # if the library checks strict types.
        # HOWEVER, LlamaIndex Workflow allows union types.
        # The error "unsupported operand type(s) for |" suggests Python < 3.10 syntax usage 
        # (StartEvent | FeedbackEvent) in a runtime environment that doesn't support it, 
        # OR the library's metaclass inspection failing on it.
        
        # Let's fix the type hint to be compatible with Python 3.9 (Union[A, B])
        
        self.attempts += 1
        lang = st.session_state.get("lang", "zh")
        
        # Initialize topic if it's a StartEvent
        if isinstance(ev, StartEvent):
            topic = ev.get("topic")
            if topic:
                self.topic = topic
            elif not self.topic:
                # If topic not in ev and not set, default
                self.topic = "AI"
                
            prompt = get_text("Agent_Workflow", "prompt_gen", lang).format(self.topic)
            st.write(get_text("Agent_Workflow", "generator_attempt", lang).format(self.attempts, self.topic))
            
        elif isinstance(ev, FeedbackEvent):
             # This block might not be reached if we have a separate handle_feedback step,
             # but keeping it just in case or for logic reference.
             # Actually, since we defined handle_feedback separately, this elif is dead code
             # if the workflow engine routes FeedbackEvent to handle_feedback.
             # But let's leave it clean or remove it?
             # The separate handle_feedback step is better.
             pass
        
        if self.attempts > self.max_attempts:
            return StopEvent(result=get_text("Agent_Workflow", "max_attempts_reached", lang))

        response = await self.llm.achat([ChatMessage(role="user", content=prompt)])
        joke = str(response.message.content)
        
        st.info(get_text("Agent_Workflow", "generated_joke", lang).format(joke))
        return ReviewEvent(joke=joke)
        
    # We need a separate step for FeedbackEvent to loop back to generate_joke?
    # Actually, in LlamaIndex Workflow, one step can consume multiple event types if typed as Union.
    # But to be safe and fix the error, let's split or use Union explicitly.
    
    @step
    async def handle_feedback(self, ctx: Context, ev: FeedbackEvent) -> Union[ReviewEvent, StopEvent]:
        # This step handles the feedback loop, essentially doing the same generation logic
        # but triggered by FeedbackEvent.
        # To avoid code duplication, we can call a helper, or just keep logic here.
        
        self.attempts += 1
        current_topic = self.topic
        lang = st.session_state.get("lang", "zh")
        
        if self.attempts > self.max_attempts:
            return StopEvent(result=get_text("Agent_Workflow", "max_attempts_reached", lang))
            
        prompt = get_text("Agent_Workflow", "prompt_improve", lang).format(current_topic, ev.original_joke, ev.feedback)
        
        st.write(get_text("Agent_Workflow", "generator_improve", lang).format(self.attempts))
        
        response = await self.llm.achat([ChatMessage(role="user", content=prompt)])
        joke = str(response.message.content)
        
        st.info(get_text("Agent_Workflow", "generated_joke", lang).format(joke))
        return ReviewEvent(joke=joke)

    @step
    async def review_joke(self, ctx: Context, ev: ReviewEvent) -> Union[FeedbackEvent, StopEvent]:
        lang = st.session_state.get("lang", "zh")
        st.write(get_text("Agent_Workflow", "critic_reviewing", lang).format(self.attempts))
        
        prompt = get_text("Agent_Workflow", "prompt_review", lang).format(ev.joke)
        
        response = await self.llm.achat([ChatMessage(role="user", content=prompt)])
        review = str(response.message.content)
        
        # Parse score
        import re
        score_match = re.search(r"SCORE:\s*(\d+)", review)
        score = int(score_match.group(1)) if score_match else 5
        
        st.warning(get_text("Agent_Workflow", "critic_review_output", lang).format(review))
        
        if score > 7:
            st.success(get_text("Agent_Workflow", "success_msg", lang).format(score))
            return StopEvent(result=ev.joke)
        else:
            st.error(get_text("Agent_Workflow", "reject_msg", lang).format(score))
            return FeedbackEvent(feedback=review, original_joke=ev.joke)

# -----------------------------------------------------------------------------
# 3. Execution Helper
# -----------------------------------------------------------------------------
def run_workflow_safe(topic: str):
    async def _run():
        api_key, base_url = init_rag_env()
        llm = OpenAILike(
            model="deepseek-ai/DeepSeek-V3", 
            api_key=api_key, 
            api_base=base_url,
            temperature=0.7, # Higher temp for creativity
            is_chat_model=True
        )
        
        workflow = JokeWorkflow(llm=llm, verbose=True, timeout=120)
        return await workflow.run(topic=topic)

    return asyncio.run(_run())

# -----------------------------------------------------------------------------
# 4. UI
# -----------------------------------------------------------------------------
topic = st.text_input(get_text("Agent_Workflow", "topic_input", lang), "AI Programmers")

if st.button(get_text("Agent_Workflow", "start_btn", lang)):
    with st.spinner(get_text("Agent_Workflow", "running", lang)):
        try:
            final_result = run_workflow_safe(topic)
            st.markdown(get_text("Agent_Workflow", "final_result", lang))
            st.markdown(final_result)
        except Exception as e:
            st.error(get_text("Agent_Workflow", "error", lang).format(e))
            import traceback
            st.code(traceback.format_exc())
