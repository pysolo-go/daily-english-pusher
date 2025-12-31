import os
import shutil
from pathlib import Path
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from rag_utils import init_rag_env, setup_llama_index

# 1. 环境初始化
api_key, base_url = init_rag_env()

# === 关键点 1：设置切片大小 (Chunking) ===
# 默认是 1024，这里我们故意设小一点 (256)，模拟处理长文档时的精细切分
# chunk_overlap=20 表示切片之间有 20 个字的重叠，防止上下文断裂
Settings.chunk_size = 256
Settings.chunk_overlap = 20

setup_llama_index(api_key, base_url)

def main():
    print("\n=== RAG 进阶版 (ChromaDB + Custom Chunking) ===")
    
    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent.parent
    pdf_dir = root_dir / "pdf"
    
    # ChromaDB 的持久化目录
    CHROMA_DB_DIR = current_dir / "chroma_db"

    # === 关键点 2：初始化 ChromaDB ===
    # ephemeral=False 表示我们要持久化到硬盘
    db = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
    
    # 创建一个集合 (Collection)，相当于 SQL 里的 Table
    # get_or_create 避免重复创建报错
    chroma_collection = db.get_or_create_collection("invoice_collection")
    
    # 把 Chroma 包装成 LlamaIndex 能用的 VectorStore
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    # 创建 StorageContext，告诉 LlamaIndex：“存向量的时候，请用 vector_store (即 Chroma)”
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 检查是否已有数据（简单判断：如果 collection 里有东西，就不重新读 PDF 了）
    if chroma_collection.count() > 0:
        print(f"发现 ChromaDB 中已有 {chroma_collection.count()} 条向量数据。")
        print("直接加载索引...")
        # 从 vector_store 加载索引
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            storage_context=storage_context
        )
    else:
        print("ChromaDB 为空，开始读取 PDF 并写入...")
        try:
            reader = SimpleDirectoryReader(
                input_dir=str(pdf_dir), 
                required_exts=[".pdf"],
                recursive=False
            )
            documents = reader.load_data()
            print(f"成功加载文档对象数: {len(documents)}")
            
            # 构建索引并写入 Chroma
            # show_progress=True 可以看到进度条
            index = VectorStoreIndex.from_documents(
                documents, 
                storage_context=storage_context,
                show_progress=True
            )
            print("索引构建完成并已写入 ChromaDB！")
            
        except Exception as e:
            print(f"处理失败: {e}")
            return

    # === 验证切片效果 ===
    # 我们查一个细节问题，看看能不能精准定位到某个小切片
    query_engine = index.as_query_engine(similarity_top_k=3)
    
    q = "Spring (SG) Pte. Ltd. 的详细地址和邮编是多少？"
    print(f"\n问题: {q}")
    response = query_engine.query(q)
    print(f"回答: {response}")
    
    # 打印出系统到底参考了哪些切片 (Source Nodes)
    print("\n--- 参考的切片 (Source Nodes) ---")
    for i, node in enumerate(response.source_nodes):
        # 打印前 100 个字
        content_preview = node.node.get_content().replace('\n', ' ')[:100]
        print(f"[{i+1}] Score: {node.score:.4f} | Content: {content_preview}...")

if __name__ == "__main__":
    main()
