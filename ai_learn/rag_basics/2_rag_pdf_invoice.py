import os
from pathlib import Path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from rag_utils import init_rag_env, setup_llama_index

# 1. 环境初始化
api_key, base_url = init_rag_env()
setup_llama_index(api_key, base_url)

def main():
    print("\n=== RAG 发票助手 (持久化版) ===")
    
    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent.parent
    
    # 定义持久化存储目录
    PERSIST_DIR = current_dir / "storage"
    pdf_dir = root_dir / "pdf"

    # 2. 检查是否存在本地索引
    if PERSIST_DIR.exists():
        print(f"发现本地索引: {PERSIST_DIR}")
        print("正在直接加载索引（无需重新读取PDF，不消耗Embedding额度）...")
        storage_context = StorageContext.from_defaults(persist_dir=str(PERSIST_DIR))
        index = load_index_from_storage(storage_context)
        print("索引加载成功！")
    else:
        print("未发现本地索引，开始初始化...")
        print(f"正在读取 PDF 目录: {pdf_dir}")
        
        try:
            reader = SimpleDirectoryReader(
                input_dir=str(pdf_dir), 
                required_exts=[".pdf"],
                recursive=False
            )
            documents = reader.load_data()
            print(f"成功加载文档对象数: {len(documents)}")
            
            if not documents:
                print("未找到 PDF 文件。")
                return

            # 构建索引
            print("正在构建向量索引...")
            index = VectorStoreIndex.from_documents(documents)
            print("索引构建完成！")
            
            # 保存索引到本地
            print(f"正在保存索引到: {PERSIST_DIR}")
            index.storage_context.persist(persist_dir=str(PERSIST_DIR))
            print("索引已保存！下次运行将直接加载。")

        except Exception as e:
            print(f"处理失败: {e}")
            return

    # 3. 创建查询引擎
    # 动态设置 k 为文档总数（注意：如果是从 storage 加载的，我们需要先获取 docstore 的大小，或者直接设一个较大的数）
    # 这里为了演示方便，我们硬编码为 10，或者你可以尝试从 index.docstore 获取
    query_engine = index.as_query_engine(similarity_top_k=10)
    print("查询引擎就绪！")
    
    questions = [
        "请总结这些发票的主要内容（购买方、销售方、金额）。",
        "最大的发票金额是多少？是谁开具的？",
        "有没有发票号码是 123456 的？如果有，金额是多少？"
    ]

    print("\n--- 开始分析发票 ---\n")
    for q in questions:
        print(f"问题: {q}")
        try:
            response = query_engine.query(q)
            print(f"回答: {response}")
        except Exception as e:
            print(f"查询失败: {e}")
        print("-" * 30)

if __name__ == "__main__":
    main()
