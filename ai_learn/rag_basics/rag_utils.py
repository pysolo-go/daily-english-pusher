import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Any, List
import openai
from llama_index.core import Settings
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.llms.openai_like import OpenAILike

def init_rag_env():
    """初始化环境变量"""
    current_dir = Path(__file__).resolve().parent
    # 假设 .env 在项目根目录 (rag_basics 的两级父目录)
    root_dir = current_dir.parent.parent
    env_path = root_dir / '.env'

    if env_path.exists():
        load_dotenv(env_path)
        print(f"已加载环境变量: {env_path}")
    
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")

    if not api_key:
        print("Error: OPENAI_API_KEY 未设置")
        exit(1)
    
    return api_key, base_url

class SiliconFlowEmbedding(BaseEmbedding):
    """自定义 Embedding 类，适配 SiliconFlow 接口"""
    def __init__(
        self, 
        model_name: str = "BAAI/bge-m3",
        api_key: str = None,
        api_base: str = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(model_name=model_name, **kwargs)
        self._client = openai.OpenAI(api_key=api_key, base_url=api_base)

    def _get_query_embedding(self, query: str) -> List[float]:
        return self._get_embedding(query)

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        return self._get_embedding(text)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_embedding(text)

    def _get_embedding(self, text: str) -> List[float]:
        text = text.replace("\n", " ")
        return self._client.embeddings.create(
            input=[text], 
            model=self.model_name
        ).data[0].embedding

def setup_llama_index(api_key: str, base_url: str):
    """配置 LlamaIndex 的全局 Settings"""
    print(f"正在配置 LlamaIndex (Base URL: {base_url})...")
    
    # 1. 设置 LLM
    Settings.llm = OpenAILike(
        model="deepseek-ai/DeepSeek-V3", 
        api_key=api_key, 
        api_base=base_url,
        temperature=0.1,
        is_chat_model=True,
        context_window=32768
    )

    # 2. 设置 Embedding
    Settings.embed_model = SiliconFlowEmbedding(
        model_name="BAAI/bge-m3", 
        api_key=api_key, 
        api_base=base_url
    )
    print("LlamaIndex 配置完成！")
