import os
from pathlib import Path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from rag_utils import init_rag_env, setup_llama_index

# 1. 环境初始化
api_key, base_url = init_rag_env()
setup_llama_index(api_key, base_url)

def main():
    print("\n=== RAG Hello World Demo (Refactored) ===")
    
    # 2. 加载数据
    current_dir = Path(__file__).resolve().parent
    data_dir = current_dir / "data"
    print(f"正在读取数据目录: {data_dir}")
    
    reader = SimpleDirectoryReader(input_dir=str(data_dir))
    documents = reader.load_data()
    print(f"成功加载文档数: {len(documents)}")

    # 3. 构建索引
    print("正在构建向量索引...")
    try:
        index = VectorStoreIndex.from_documents(documents)
        print("索引构建完成！")
    except Exception as e:
        print(f"索引构建失败: {e}")
        return

    # 4. 创建查询引擎
    query_engine = index.as_query_engine()

    # 5. 提问
    questions = [
        "加班餐费报销的标准是什么？",
        "如果不去公司上班有什么条件？",
        "我入职3年了，有多少年假？"
    ]

    print("\n--- 开始问答 ---\n")
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
