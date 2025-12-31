import sys
from pathlib import Path
import networkx as nx
from pyvis.network import Network

# Add project root to sys.path
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent.parent
sys.path.append(str(root_dir))

from ai_learn.rag_basics.rag_utils import init_rag_env, setup_llama_index
from llama_index.core import Document, PropertyGraphIndex
from llama_index.core.graph_stores import SimplePropertyGraphStore

def main():
    # 1. Initialize
    api_key, base_url = init_rag_env()
    setup_llama_index(api_key, base_url)

    # 2. Prepare Text (More complex to show relationships)
    # 使用中文/双语文本，以便生成中文知识图谱
    text = """
    伊隆·马斯克 (Elon Musk) 是特斯拉 (Tesla) 的 CEO。
    特斯拉总部位于美国德克萨斯州奥斯汀 (Austin, Texas)。
    马斯克也是 SpaceX 的创始人，该公司设计火箭 (Rockets)。
    SpaceX 与 NASA 有合作关系。
    史蒂夫·乔布斯 (Steve Jobs) 是苹果公司 (Apple) 的联合创始人。
    苹果公司与谷歌 (Google) 存在竞争关系。
    """
    documents = [Document(text=text)]

    # 3. Build Knowledge Graph (PropertyGraphIndex)
    # This automatically uses the LLM to extract entities and relations
    print("🚀 正在从文本中提取知识图谱 (使用 LLM)...")
    print("🚀 Extracting Knowledge Graph from text (using LLM)...")
    
    # Using SimplePropertyGraphStore (In-Memory) for learning
    index = PropertyGraphIndex.from_documents(
        documents,
        property_graph_store=SimplePropertyGraphStore(),
        show_progress=True
    )
    
    print("✅ 知识图谱构建完成！ (Knowledge Graph Built!)")

    # 4. Visualize with Pyvis
    print("🎨 正在生成可视化图表... (Generating Visualization...)")
    
    # Get the underlying NetworkX graph
    # Note: PropertyGraphIndex stores data in a custom structure, we need to extract it to networkx
    # The store has a 'graph' attribute which is a networkx graph in SimplePropertyGraphStore?
    # Let's check the internal storage mechanism or iterate over triplets.
    
    # Newer LlamaIndex versions provide easier access.
    # We can query all triplets.
    
    g = nx.Graph()
    
    # Access the graph store directly
    graph_store = index.property_graph_store
    
    # Iterate over all relations (edges)
    # The get_triplets method might be available or we iterate
    # Let's try to use the retrieval interface to get everything
    
    # In recent versions, we can get the networkx graph directly if using SimplePropertyGraphStore?
    # Actually, let's iterate manually if needed, but PropertyGraphIndex is complex.
    # Let's try a simpler retrieval for visualization: get all nodes.
    
    # Fetch all triplets from the store
    # SimplePropertyGraphStore holds data in memory.
    
    # For visualization purposes, we'll extract data via `get_triplets` if available, 
    # or just inspect the `_graph` if it's exposed (it is in SimplePropertyGraphStore).
    
    # HACK: Accessing internal networkx graph for SimplePropertyGraphStore
    # If this fails in future versions, we need to use the public API.
    try:
        # LlamaIndex 0.10.x+
        # The store might maintain a networkx graph internally
        # But let's use a safe way: Retriever
        pass
    except:
        pass

    # Safe extraction loop
    # We will use the `get` method of the store
    # Note: In some versions, get_triplets(None) returns [], so we access the underlying graph directly
    # or use a catch-all method if available.
    
    # Method 1: Try to access the internal graph storage if get_triplets fails to return all
    if hasattr(graph_store, 'graph') and hasattr(graph_store.graph, 'get_triplets'):
         triplets = graph_store.graph.get_triplets()
    else:
         triplets = graph_store.get_triplets(entity_names=None) 
    
    print(f"DEBUG: 图数据库中发现 {len(triplets)} 个三元组 (Found {len(triplets)} triplets).")

    for t in triplets:
        # t is a tuple/list: [subject_node, relation, object_node]
        # Nodes are usually EntityNode or ChunkNode objects.
        # They should have 'name' or 'label' or 'text' or 'id'.
        
        # Safe access to node identifier
        def get_node_label(node):
            if hasattr(node, 'name'): return node.name
            if hasattr(node, 'id'): return node.id
            if hasattr(node, 'label'): return node.label
            return str(node)
            
        src = get_node_label(t[0])
        rel = str(t[1]) # Relation object or string
        dst = get_node_label(t[2])
        
        # Relation might be an object with label
        if hasattr(t[1], 'label'):
             rel = t[1].label
        
        g.add_node(src, title=getattr(t[0], 'label', "Entity"))
        g.add_node(dst, title=getattr(t[2], 'label', "Entity"))
        g.add_edge(src, dst, label=rel)
        print(f"  Found: {src} --[{rel}]--> {dst}")

    # 5. Save to HTML
    # cdn_resources='in_line' ensures all JS/CSS is embedded in the HTML, 
    # preventing network errors (like blocked CDNs)
    net = Network(notebook=False, height="750px", width="100%", cdn_resources='in_line')
    net.from_nx(g)
    
    output_file = current_dir / "graph_visualization.html"
    net.save_graph(str(output_file))
    print(f"✨ 可视化文件已保存至: {output_file}")
    print(f"👉 请在浏览器中打开此文件查看图谱！")

    # 6. Test Graph Retrieval
    print("\n❓ 测试图谱查询 (Testing Graph Query):")
    
    # 演示 1: 复杂的多跳推理 (Multi-hop Reasoning)
    # 文本中没有直接说 "马斯克和NASA" 的关系，需要通过 SpaceX 桥接
    query_str = "伊隆·马斯克和 NASA 有什么关系？请解释中间的关联。"
    print(f"\n🔎 提问: {query_str}")
    
    query_engine = index.as_query_engine(include_text=True) 
    response = query_engine.query(query_str)
    print(f"🤖 回答: {response}")

    # 演示 2: 查看 AI 到底检索到了什么 (Show Retrieved Context)
    print("\n🕵️‍♂️ AI 检索到的“脑图”线索 (Retrieved Graph Context):")
    retriever = index.as_retriever(similarity_top_k=5)
    nodes = retriever.retrieve(query_str)
    
    for i, node in enumerate(nodes):
        # 检查节点是否包含图谱关系信息
        content = node.get_content()
        print(f"--- 线索 {i+1} ---")
        print(content.strip())
        print("----------------")

    print("\n💡 总结：")
    print("普通搜索 (Vector) 只能找到包含关键词的句子。")
    print("图谱搜索 (Graph) 能把 '马斯克 -> SpaceX' 和 'SpaceX -> NASA' 拼接起来，即使这两句话隔得很远。")

if __name__ == "__main__":
    main()
