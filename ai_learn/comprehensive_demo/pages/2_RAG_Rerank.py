import streamlit as st
import sys
from pathlib import Path
import os
from dotenv import load_dotenv
import shutil

# LlamaIndex imports
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import chromadb

# Add project root
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(root_dir))

# Import custom modules
from ai_learn.rag_basics.rag_utils import init_rag_env, setup_llama_index
from ai_learn.rag_advanced.custom_rerank import SiliconFlowRerank
from ai_learn.comprehensive_demo.localization import init_lang, get_text, lang_selector, render_sidebar

# Init Language
init_lang()
lang = st.session_state.lang

st.set_page_config(page_title=get_text("RAG_Rerank", "page_title", lang), page_icon="📚", layout="wide")

# Language Selector
lang_selector()

# Render Sidebar
render_sidebar()

st.header(get_text("RAG_Rerank", "header", lang))

# Init Logic
@st.cache_resource
def initialize_rag():
    api_key, base_url = init_rag_env()
    setup_llama_index(api_key, base_url)
    return api_key

api_key = initialize_rag()

st.header(get_text("RAG_Rerank", "header", lang))

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(get_text("RAG_Rerank", "data_prep", lang))
    input_method = st.radio(get_text("RAG_Rerank", "data_source", lang), get_text("RAG_Rerank", "source_options", lang))
    
    default_text = """
    发票号码: 12345678
    开票日期: 2023年10月25日
    购买方: 这里的购买方是 字节跳动科技有限公司
    销售方: 这里的销售方是 微软(中国)有限公司
    金额: 12000.00 元
    备注: 技术服务费
    
    发票号码: 87654321
    开票日期: 2023年11月01日
    购买方: 这里的购买方是 阿里巴巴网络技术有限公司
    销售方: 这里的销售方是 英伟达半导体
    金额: 55000.50 元
    备注: 显卡采购
    """
    
    text_input = st.text_area(get_text("RAG_Rerank", "input_label", lang), value=default_text, height=300)
    
    if st.button(get_text("RAG_Rerank", "build_index", lang)):
        with st.spinner(get_text("RAG_Rerank", "indexing", lang)):
            documents = [Document(text=text_input)]
            # Use in-memory vector store for demo
            index = VectorStoreIndex.from_documents(documents)
            st.session_state.rag_index = index
            st.success(get_text("RAG_Rerank", "index_success", lang))

with col2:
    st.subheader(get_text("RAG_Rerank", "qa_retrieval", lang))
    
    if "rag_index" not in st.session_state:
        st.info(get_text("RAG_Rerank", "build_index_first", lang))
    else:
        query = st.text_input(get_text("RAG_Rerank", "query_placeholder", lang), value=get_text("RAG_Rerank", "query_default", lang))
        
        use_rerank = st.toggle(get_text("RAG_Rerank", "enable_rerank", lang), value=True)
        top_k = st.slider(get_text("RAG_Rerank", "top_k", lang), 1, 10, 5)
        rerank_top_n = st.slider(get_text("RAG_Rerank", "top_n", lang), 1, 5, 2)
        
        if st.button(get_text("RAG_Rerank", "start_retrieval", lang)):
            index = st.session_state.rag_index
            
            # Configure Retriever
            if use_rerank:
                reranker = SiliconFlowRerank(
                    model="BAAI/bge-reranker-v2-m3", 
                    api_key=api_key,
                    top_n=rerank_top_n
                )
                query_engine = index.as_query_engine(
                    similarity_top_k=top_k,
                    node_postprocessors=[reranker]
                )
                st.caption(f"🚀 模式: Vector Search (Top {top_k}) -> Rerank -> Result (Top {rerank_top_n})")
            else:
                query_engine = index.as_query_engine(similarity_top_k=rerank_top_n)
                st.caption(f"🚀 模式: Pure Vector Search (Top {rerank_top_n})")
            
            # Execute
            with st.spinner(get_text("RAG_Rerank", "thinking", lang)):
                response = query_engine.query(query)
            
            st.markdown(get_text("RAG_Rerank", "answer", lang))
            st.success(str(response))
            
            # Show Context
            with st.expander(get_text("RAG_Rerank", "source_nodes", lang)):
                for node in response.source_nodes:
                    score = node.score if node.score else 0.0
                    st.markdown(f"**Score: {score:.4f}**")
                    st.text(node.node.get_content())
                    st.divider()
