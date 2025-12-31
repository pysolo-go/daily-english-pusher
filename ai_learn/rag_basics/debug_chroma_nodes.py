import chromadb
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from rag_utils import init_rag_env, setup_llama_index
from pathlib import Path

# 1. 环境初始化
api_key, base_url = init_rag_env()
setup_llama_index(api_key, base_url)

def main():
    print("\n=== 查看 ChromaDB 切片详情 ===")
    
    current_dir = Path(__file__).resolve().parent
    CHROMA_DB_DIR = current_dir / "chroma_db"
    
    # 连接已有的 ChromaDB
    db = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
    chroma_collection = db.get_or_create_collection("invoice_collection")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # 加载索引
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        storage_context=storage_context
    )
    
    # 创建查询引擎
    query_engine = index.as_query_engine(similarity_top_k=3)
    
    q = "Spring (SG) Pte. Ltd. 的详细地址和邮编是多少？"
    print(f"\n重现问题: {q}")
    
    # 执行查询
    response = query_engine.query(q)
    
    print("\n" + "="*50)
    print("检索到的源切片 (Source Nodes) 完整内容")
    print("="*50)
    
    for i, node in enumerate(response.source_nodes):
        print(f"\n>>> 切片 #{i+1} (相似度得分: {node.score:.4f})")
        print(f"来源文件: {node.metadata.get('file_name', 'Unknown')}")
        print("-" * 30)
        # 打印完整文本
        print(node.node.get_content())
        print("-" * 30)

if __name__ == "__main__":
    main()
