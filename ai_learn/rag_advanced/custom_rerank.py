import os
import requests
import json
from typing import List, Optional, Any
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore, QueryBundle
from pydantic import Field, PrivateAttr

class SiliconFlowRerank(BaseNodePostprocessor):
    """
    Custom Reranker using SiliconFlow API.
    Model: BAAI/bge-reranker-v2-m3
    """
    model: str = Field(description="Reranker model name")
    top_n: int = Field(description="Number of nodes to return")
    api_key: str = Field(description="SiliconFlow API Key")
    base_url: str = Field(description="Base URL for the API")

    def __init__(
        self,
        model: str = "BAAI/bge-reranker-v2-m3",
        top_n: int = 3,
        api_key: Optional[str] = None,
        base_url: str = "https://api.siliconflow.cn/v1",
        **kwargs: Any,
    ):
        super().__init__(
            model=model,
            top_n=top_n,
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url=base_url or os.getenv("OPENAI_BASE_URL"),
            **kwargs
        )

    def _postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        if not nodes:
            return []
        
        # Prepare inputs for API
        query_str = query_bundle.query_str
        documents = [node.node.get_content() for node in nodes]
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "query": query_str,
            "documents": documents,
            "top_n": self.top_n,
            "return_documents": False # We only need indices and scores
        }
        
        # Call Rerank API
        # Note: SiliconFlow Rerank endpoint might differ slightly, assuming standard format
        # If /v1/rerank exists
        api_url = f"{self.base_url}/rerank"
        # Fix: base_url in env often includes /v1, so we need to handle that
        if self.base_url.endswith("/v1"):
             api_url = f"{self.base_url}/rerank"
        else:
             api_url = f"{self.base_url}/v1/rerank"

        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            results = response.json().get("results", [])
            
            # Map back to nodes
            new_nodes = []
            for res in results:
                index = res["index"]
                score = res["relevance_score"]
                
                node = nodes[index]
                node.score = score # Update score
                new_nodes.append(node)
                
            return new_nodes

        except Exception as e:
            print(f"Warning: Rerank failed, returning original nodes. Error: {e}")
            return nodes[:self.top_n]
