import streamlit as st
import sys
import os

# Add parent directory to path to import localization
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from localization import init_lang, get_text, lang_selector, render_sidebar

# Initialize
st.set_page_config(page_title="PEFT & LoRA Concepts", page_icon="🧠", layout="wide")
init_lang()
render_sidebar()
lang_selector()

lang = st.session_state.lang

# Title
st.title(get_text("PEFT_Concepts", "title", lang))

# Tabs
tab1, tab2, tab3 = st.tabs([
    get_text("PEFT_Concepts", "tab_concepts", lang),
    get_text("PEFT_Concepts", "tab_lora", lang),
    get_text("PEFT_Concepts", "tab_data", lang)
])

# Tab 1: Full vs PEFT (Renamed to Beginner Guide)
with tab1:
    st.header(get_text("PEFT_Concepts", "tab_concepts", lang))

    # --- Section 1: Why Fine-tune? ---
    st.subheader(get_text("PEFT_Concepts", "why_title", lang))
    st.write(get_text("PEFT_Concepts", "why_desc", lang))
    
    col_why1, col_why2, col_why3 = st.columns(3)
    with col_why1:
        st.info(get_text("PEFT_Concepts", "use_case_1", lang))
    with col_why2:
        st.warning(get_text("PEFT_Concepts", "use_case_2", lang))
    with col_why3:
        st.success(get_text("PEFT_Concepts", "use_case_3", lang))
    
    st.markdown("---")

    # --- Section 2: Comparison ---
    st.subheader(get_text("PEFT_Concepts", "rag_vs_ft_title", lang))
    
    # Use a nice dataframe-like layout or just columns
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"#### {get_text('PEFT_Concepts', 'comp_prompt', lang)}")
        st.caption(get_text("PEFT_Concepts", "comp_prompt_desc", lang))
    with c2:
        st.markdown(f"#### {get_text('PEFT_Concepts', 'comp_rag', lang)}")
        st.caption(get_text("PEFT_Concepts", "comp_rag_desc", lang))
    with c3:
        st.markdown(f"#### {get_text('PEFT_Concepts', 'comp_ft', lang)}")
        st.caption(get_text("PEFT_Concepts", "comp_ft_desc", lang))
        
    st.markdown("---")

    # --- Section 3: Lifecycle ---
    st.subheader(get_text("PEFT_Concepts", "lifecycle_title", lang))
    
    st.graphviz_chart(f'''
        digraph {{
            rankdir=LR;
            node [shape=box, style="filled,rounded", fontname="Helvetica"];
            
            S1 [label="{get_text('PEFT_Concepts', 'step_1', lang)}\\n{get_text('PEFT_Concepts', 'step_1_desc', lang)}", fillcolor="#e3f2fd"];
            S2 [label="{get_text('PEFT_Concepts', 'step_2', lang)}\\n{get_text('PEFT_Concepts', 'step_2_desc', lang)}", fillcolor="#f3e5f5"];
            S3 [label="{get_text('PEFT_Concepts', 'step_3', lang)}\\n{get_text('PEFT_Concepts', 'step_3_desc', lang)}", fillcolor="#fff3e0"];
            S4 [label="{get_text('PEFT_Concepts', 'step_4', lang)}\\n{get_text('PEFT_Concepts', 'step_4_desc', lang)}", fillcolor="#e8f5e9"];
            
            S1 -> S2 -> S3 -> S4;
        }}
    ''')

    st.markdown("---")
    
    # --- Section 4: Technical Deep Dive (Original Content) ---
    st.markdown("### Technical: Full Fine-tuning vs PEFT")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(get_text("PEFT_Concepts", "concept_full_title", lang))
        st.info(get_text("PEFT_Concepts", "concept_full_desc", lang))
        
        # Use graphviz for guaranteed rendering
        st.graphviz_chart(f'''
            digraph {{
                rankdir=TD;
                node [shape=box, style="filled,rounded", fontname="Helvetica"];
                
                Data [label="{get_text('PEFT_Concepts', 'diag_train_data', lang)}", fillcolor="#e1f5fe"];
                PreTrained [label="{get_text('PEFT_Concepts', 'diag_pretrained', lang)}", fillcolor="#fce4ec"];
                NewModel [label="{get_text('PEFT_Concepts', 'diag_new_model', lang)}", fillcolor="#fce4ec"];
                
                Data -> PreTrained [label="{get_text('PEFT_Concepts', 'diag_update_all', lang)}"];
                PreTrained -> NewModel;
            }}
        ''')

    with col2:
        st.subheader(get_text("PEFT_Concepts", "concept_peft_title", lang))
        st.success(get_text("PEFT_Concepts", "concept_peft_desc", lang))
        
        st.graphviz_chart(f'''
            digraph {{
                rankdir=TD;
                node [shape=box, style="filled,rounded", fontname="Helvetica"];
                
                Data [label="{get_text('PEFT_Concepts', 'diag_train_data', lang)}", fillcolor="#e1f5fe"];
                PreTrained [label="{get_text('PEFT_Concepts', 'diag_pretrained_frozen', lang)}", fillcolor="#eeeeee", fontcolor="#999999"];
                Adapter [label="{get_text('PEFT_Concepts', 'diag_adapter', lang)}", fillcolor="#fff9c4"];
                Output [label="{get_text('PEFT_Concepts', 'diag_output', lang)}", shape=oval];
                
                Data -> Adapter [label="{get_text('PEFT_Concepts', 'diag_update_adapter', lang)}"];
                PreTrained -> Output [style=dashed];
                Adapter -> Output;
            }}
        ''')

    st.markdown("---")
    st.subheader(get_text("PEFT_Concepts", "analogy", lang))
    st.markdown(get_text("PEFT_Concepts", "analogy_text", lang))

# Tab 2: LoRA Deep Dive
with tab2:
    st.header(get_text("PEFT_Concepts", "tab_lora", lang))
    
    st.markdown(f"### {get_text('PEFT_Concepts', 'lora_desc', lang)}")
    
    st.latex(r"W_{tuned} = W_0 + \Delta W = W_0 + B \cdot A")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.markdown("#### Matrix Dimensions")
        st.latex(r"W_0 \in \mathbb{R}^{d \times d}")
        st.latex(r"B \in \mathbb{R}^{d \times r}, \quad A \in \mathbb{R}^{r \times d}")
        st.latex(r"r \ll d")
        st.caption("r is the 'rank' (e.g., 8, 16, 64). d is hidden size (e.g., 4096).")
        
    with col_b:
        st.markdown(f"#### {get_text('PEFT_Concepts', 'params_saved', lang)}")
        st.metric(label="Original Parameters (d*d)", value="16,777,216", delta="100% (Reference)")
        st.metric(label="LoRA Parameters (2*d*r)", value="65,536", delta="-99.6% (Rank=8)")
    
    st.warning(get_text("PEFT_Concepts", "qlora_note", lang))

# Tab 3: Data Construction
with tab3:
    st.header(get_text("PEFT_Concepts", "tab_data", lang))
    
    st.subheader(get_text("PEFT_Concepts", "data_step1", lang))
    st.markdown(get_text("PEFT_Concepts", "data_step1_desc", lang))
    
    st.code("""
# Python Data Cleaning Example
import re

def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML
    text = re.sub(r'\s+', ' ', text)     # Normalize whitespace
    return text.strip()
    """, language="python")

    st.subheader(get_text("PEFT_Concepts", "data_step2", lang))
    st.markdown(get_text("PEFT_Concepts", "data_step2_desc", lang))
    
    st.markdown(f"### {get_text('PEFT_Concepts', 'good_bad_example', lang)}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.error(get_text("PEFT_Concepts", "bad_label", lang))
        st.markdown("""
        **User**: Help.
        
        **Assistant**: Yes.
        
        *(Too short, no context, model learns nothing)*
        """)
        
        st.markdown("---")
        
        st.markdown("""
        **User**: Write a poem.
        
        **Assistant**: Roses are red, violets are blue.
        
        *(Too generic, cliche)*
        """)
        
    with c2:
        st.success(get_text("PEFT_Concepts", "good_label", lang))
        st.markdown("""
        **User**: My computer is running slow and making a loud noise. What should I do?
        
        **Assistant**: A loud noise combined with slow performance often indicates an overheating issue or a failing fan. Here are 3 steps to check:
        1. Check for dust in the vents.
        2. Listen if the fan is spinning efficiently.
        3. Check Task Manager for high CPU usage.
        
        *(Specific, structured, helpful)*
        """)

    st.markdown("---")
    if st.button(get_text("PEFT_Concepts", "goto_page7", lang), type="primary"):
        st.switch_page("pages/7_Finetune_Data_Prep.py")
