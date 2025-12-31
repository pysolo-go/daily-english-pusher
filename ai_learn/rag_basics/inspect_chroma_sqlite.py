import sqlite3
from pathlib import Path

def main():
    print("\n=== 查看 ChromaDB SQLite 元数据 ===")
    
    current_dir = Path(__file__).resolve().parent
    # 定位到 chroma.sqlite3 文件
    db_path = current_dir / "chroma_db" / "chroma.sqlite3"
    
    if not db_path.exists():
        print(f"错误: 未找到数据库文件 {db_path}")
        return

    print(f"正在连接数据库: {db_path}\n")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. 查看有哪些 Collection
        print("--- Collections (集合) ---")
        cursor.execute("SELECT id, name, dimension FROM collections")
        collections = cursor.fetchall()
        for col in collections:
            print(f"ID: {col[0]}")
            print(f"Name: {col[1]}")
            print(f"Dimension: {col[2]} (向量维度)")
            print("-" * 30)

        # 2. 查看 Embeddings 表结构
        print("\n--- Embeddings 表结构 ---")
        cursor.execute("PRAGMA table_info(embeddings)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"Column: {col[1]} (Type: {col[2]})")

        # 3. 尝试查询数据
        print("\n--- 数据预览 ---")
        # 通常新版 Chroma 把 id, segment_id, embedding (blob) 放在这里
        # 文本内容可能不在 embeddings 表，而是在 embeddings_queue 或者被移除了（只存向量）
        # 但 Metadata 肯定在 embedding_metadata 表
        
        # 查 embeddings 表
        cursor.execute("SELECT id, segment_id FROM embeddings LIMIT 3")
        rows = cursor.fetchall()
        for row in rows:
            print(f"Embedding ID: {row[0]}")
            print(f"Segment ID: {row[1]}")
            
            # 查 Metadata
            # metadata_key, string_value, int_value, float_value
            cursor.execute(f"SELECT key, string_value FROM embedding_metadata WHERE id = '{row[0]}'")
            metas = cursor.fetchall()
            meta_dict = {m[0]: m[1] for m in metas}
            print(f"Metadata: {meta_dict}")
            print("-" * 30)

    except Exception as e:
        print(f"读取失败: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
