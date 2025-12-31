import sys
import asyncio
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))

from ai_learn.rag_basics.rag_utils import init_rag_env
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai_like import OpenAILike

# 1. Define Tools (The "Hands" of the Agent)
def multiply(a: int, b: int) -> int:
    """Multiply two integers and returns the result integer"""
    print(f"🛠️ Tool Triggered: multiply({a}, {b})")
    return a * b

def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    print(f"🛠️ Tool Triggered: get_weather({city})")
    # Mock data
    weather_db = {
        "Beijing": "Sunny, 25°C",
        "Shanghai": "Rainy, 22°C",
        "New York": "Cloudy, 18°C"
    }
    return weather_db.get(city, "Unknown weather")

async def main():
    # 2. Init Environment
    api_key, base_url = init_rag_env()
    
    # We use a slightly different LLM setup for Agents to ensure better instruction following
    # DeepSeek V3 is good for this.
    llm = OpenAILike(
        model="deepseek-ai/DeepSeek-V3", 
        api_key=api_key, 
        api_base=base_url,
        temperature=0.1, # Lower temperature for more precise tool use
        is_chat_model=True
    )
    
    # 3. Wrap functions as Tools
    multiply_tool = FunctionTool.from_defaults(fn=multiply)
    weather_tool = FunctionTool.from_defaults(fn=get_weather)
    
    tools = [multiply_tool, weather_tool]
    
    # 4. Create the Agent (The "Brain")
    # In LlamaIndex 0.14.10+, ReActAgent is a Workflow.
    # We initialize it directly and use .run()
    
    agent = ReActAgent(tools=tools, llm=llm, verbose=True)
    
    # 5. Test
    print("🤖 Agent initialized (Workflow based)! Asking a complex question...")
    query = "What is the weather in Beijing? And if I multiply 25 by 4, what do I get?"
    print(f"❓ Query: {query}\n")
    
    # Workflow agents run asynchronously
    try:
        response = await agent.run(user_msg=query)
        print(f"\n✅ Final Response: {response}")
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")

if __name__ == "__main__":
    asyncio.run(main())
