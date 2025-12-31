import os
from pathlib import Path
from dotenv import load_dotenv

def init_langchain_env():
    """Initialize environment variables for LangChain."""
    current_dir = Path(__file__).resolve().parent
    # .env is in the root directory (two levels up from langchain_basics)
    root_dir = current_dir.parent.parent
    env_path = root_dir / '.env'

    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded environment from: {env_path}")
    
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")

    if not api_key:
        print("Error: OPENAI_API_KEY is not set.")
        exit(1)
    
    # LangChain automatically picks up OPENAI_API_KEY, but we return them just in case
    # For custom endpoints (like SiliconFlow), we need to pass base_url explicitly
    return api_key, base_url
