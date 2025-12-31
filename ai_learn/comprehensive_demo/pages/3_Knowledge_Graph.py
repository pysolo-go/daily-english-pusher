import streamlit as st
import sys
from pathlib import Path
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# Add project root
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(root_dir))

# Import modules
from ai_learn.rag_basics.rag_utils import init_rag_env, setup_llama_index
from llama_index.core import Document, PropertyGraphIndex
from llama_index.core.graph_stores import SimplePropertyGraphStore
from ai_learn.comprehensive_demo.localization import init_lang, get_text, lang_selector, render_sidebar

# Init Language
init_lang()
lang = st.session_state.lang

st.set_page_config(page_title=get_text("Knowledge_Graph", "page_title", lang), page_icon="🕸️", layout="wide")

# Language Selector
lang_selector()

# Render Sidebar
render_sidebar()

st.header(get_text("Knowledge_Graph", "header", lang))

# Init Logic
@st.cache_resource
def initialize_graph_env():
    api_key, base_url = init_rag_env()
    setup_llama_index(api_key, base_url)
    return api_key

initialize_graph_env()

st.header(get_text("Knowledge_Graph", "header", lang))

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(get_text("Knowledge_Graph", "text_input", lang))
    default_text = """
    伊隆·马斯克 (Elon Musk) 是特斯拉 (Tesla) 的 CEO。
    特斯拉总部位于美国德克萨斯州奥斯汀 (Austin, Texas)。
    马斯克也是 SpaceX 的创始人，该公司设计火箭 (Rockets)。
    SpaceX 与 NASA 有合作关系。
    史蒂夫·乔布斯 (Steve Jobs) 是苹果公司 (Apple) 的联合创始人。
    苹果公司与谷歌 (Google) 存在竞争关系。
    """
    text_input = st.text_area(get_text("Knowledge_Graph", "input_label", lang), value=default_text, height=200)
    
    if st.button(get_text("Knowledge_Graph", "generate_btn", lang)):
        with st.spinner(get_text("Knowledge_Graph", "generating", lang)):
            documents = [Document(text=text_input)]
            
            # Build Graph
            index = PropertyGraphIndex.from_documents(
                documents,
                property_graph_store=SimplePropertyGraphStore(),
                show_progress=True
            )
            st.session_state.graph_index = index
            
            # Extract to NetworkX for visualization
            g = nx.Graph()
            graph_store = index.property_graph_store
            
            # Safe extraction logic (copied from 1_simple_graph.py)
            if hasattr(graph_store, 'graph') and hasattr(graph_store.graph, 'get_triplets'):
                 triplets = graph_store.graph.get_triplets()
            else:
                 triplets = graph_store.get_triplets(entity_names=None)
            
            for t in triplets:
                def get_node_label(node):
                    if hasattr(node, 'name'): return node.name
                    if hasattr(node, 'id'): return node.id
                    if hasattr(node, 'label'): return node.label
                    return str(node)
                    
                src = get_node_label(t[0])
                rel = str(t[1])
                if hasattr(t[1], 'label'): rel = t[1].label
                dst = get_node_label(t[2])
                
                g.add_node(src, title=getattr(t[0], 'label', "Entity"))
                g.add_node(dst, title=getattr(t[2], 'label', "Entity"))
                g.add_edge(src, dst, label=rel)
            
            # Save HTML
            net = Network(notebook=False, height="500px", width="100%", cdn_resources='in_line')
            net.from_nx(g)
            html_path = Path("temp_graph.html")
            net.save_graph(str(html_path))
            
            # Read HTML content
            with open(html_path, 'r', encoding='utf-8') as f:
                st.session_state.graph_html = f.read()
            
            st.success(get_text("Knowledge_Graph", "success_msg", lang).format(len(triplets)))

with col2:
    st.subheader(get_text("Knowledge_Graph", "graph_query", lang))
    if "graph_index" in st.session_state:
        query = st.text_input(get_text("Knowledge_Graph", "query_placeholder", lang), value=get_text("Knowledge_Graph", "query_default", lang))
        if st.button(get_text("Knowledge_Graph", "query_btn", lang)):
            with st.spinner(get_text("Knowledge_Graph", "reasoning", lang)):
                query_engine = st.session_state.graph_index.as_query_engine(include_text=True)
                response = query_engine.query(query)
                st.markdown(get_text("Knowledge_Graph", "answer", lang))
                st.info(str(response))

st.divider()

# Full width visualization
st.subheader(get_text("Knowledge_Graph", "visualization", lang))
if "graph_html" in st.session_state:
    components.html(st.session_state.graph_html, height=520, scrolling=True)
else:
    st.info(get_text("Knowledge_Graph", "viz_placeholder", lang))
