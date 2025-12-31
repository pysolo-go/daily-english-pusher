import sys
from pathlib import Path

# Add project root to sys.path
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent.parent
sys.path.append(str(root_dir))

from ai_learn.rag_basics.rag_utils import init_rag_env, setup_llama_index
from ai_learn.rag_advanced.custom_rerank import SiliconFlowRerank

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

# Constants
CHROMA_DB_DIR = root_dir / "ai_learn/rag_basics/chroma_db"
COLLECTION_NAME = "invoice_collection"

def main():
    # 1. Initialize
    api_key, base_url = init_rag_env()
    setup_llama_index(api_key, base_url)
    
    # 2. Connect to ChromaDB (Reuse existing data)
    print(f"Connecting to ChromaDB at: {CHROMA_DB_DIR}")
    db = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
    chroma_collection = db.get_or_create_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # 3. Load Index
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context
    )
    
    # 4. Compare Basic vs Advanced
    query_str = "Spring (SG) Pte. Ltd. 的详细地址在哪里？"
    print(f"\n❓ Query: {query_str}")
    
    # --- A. Basic Retrieval (Top 5) ---
    print("\n--- [Basic RAG] Top 5 (Based on Vector Similarity) ---")
    base_retriever = index.as_retriever(similarity_top_k=5)
    base_nodes = base_retriever.retrieve(query_str)
    
    for i, node in enumerate(base_nodes):
        print(f"[{i+1}] Score: {node.score:.4f} | Content: {node.node.get_content()[:50]}...")

    # --- B. Advanced Retrieval (Rerank Top 2) ---
    print("\n--- [Advanced RAG] Reranked Top 2 (Vector Top 10 -> Rerank -> Top 2) ---")
    
    # Initialize Reranker
    reranker = SiliconFlowRerank(
        model="BAAI/bge-reranker-v2-m3",
        top_n=2,
        api_key=api_key,
        base_url=base_url
    )
    
    # Create Query Engine with Reranker
    # Strategy: Fetch more candidates first (similarity_top_k=10), then rerank
    query_engine = index.as_query_engine(
        similarity_top_k=10,
        node_postprocessors=[reranker]
    )
    
    response = query_engine.query(query_str)
    
    print(f"🎉 Final Answer: {response}")
    print("\n--- Reranked Source Nodes ---")
    for i, node in enumerate(response.source_nodes):
        print(f"[{i+1}] Score: {node.score:.4f} | Content: {node.node.get_content()[:50]}...")

if __name__ == "__main__":
    main()
