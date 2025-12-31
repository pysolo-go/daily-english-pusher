# AI 学习知识库总结 (Knowledge Summary)

本文档对截至目前的学习内容进行系统性总结，涵盖 RAG 基础、进阶技术、知识图谱以及应用开发框架。

---

## 一、 基础架构与框架 (Frameworks & Architecture)

### 1.1 LlamaIndex
*   **定位**：以数据为中心的 RAG 框架，擅长数据连接、索引构建和查询。
*   **核心组件**：
    *   `SimpleDirectoryReader`: 数据加载器。
    *   `VectorStoreIndex`: 向量索引构建器。
    *   `StorageContext`: 管理底层存储（向量库、文档存储）。
    *   `QueryEngine`: 查询接口，支持后处理 (Postprocessing)。
*   **应用场景**：大多数 RAG 任务的首选框架。

### 1.2 LangChain
*   **定位**：应用编排框架，强调组件的组合与流控制。
*   **核心概念**：
    *   **LCEL (LangChain Expression Language)**: 声明式链式调用 (`prompt | model | parser`)。
*   **学习状态**：了解了基本的 Chain 结构，目前主要专注于 LlamaIndex。

### 1.3 Streamlit
*   **定位**：面向数据科学与 AI 的快速 Web UI 构建工具。
*   **关键特性**：
    *   `st.session_state`: 维护对话历史等状态。
    *   `st.chat_message` / `st.chat_input`: 预置的聊天组件。
    *   `st.write_stream`: 支持流式输出渲染。
*   **成果**：构建了一个包含对话与翻译功能的 Web 应用。

---

## 二、 RAG 核心技术 (Retrieval-Augmented Generation)

### 2.1 基础 RAG (Vector Search)
*   **流程**：
    1.  **ETL**: 加载文档 -> 文本切块 (Chunking) -> 向量嵌入 (Embedding)。
    2.  **存储**: 使用向量数据库 (ChromaDB) 持久化存储向量与元数据。
    3.  **检索**: 基于余弦相似度 (Cosine Similarity) 查找 Top-K 相关片段。
    4.  **生成**: 将片段填入 Prompt，让 LLM 生成回答。
*   **局限**: 仅基于语义相似度，容易受关键词干扰，难以处理复杂推理。

### 2.2 进阶 RAG：重排序 (Rerank)
*   **原理**：引入“粗排 + 精排”的两阶段检索机制。
    *   **第一阶段 (Retrieve)**: 快速检索出 Top-50 个宽泛结果。
    *   **第二阶段 (Rerank)**: 使用专门的 Rerank 模型 (如 BGE-Reranker-v2-m3) 对这 50 个结果进行逐一打分。
*   **效果**：显著提升检索准确率（在发票细节测试中从 0.44 提升至 0.97）。
*   **代码模式**：LlamaIndex `NodePostprocessor`。

### 2.3 进阶 RAG：知识图谱 (Graph RAG)
*   **核心价值**：解决**多跳推理 (Multi-hop Reasoning)** 和**全局理解**问题。
*   **工作原理**：
    *   **实体提取**: 使用 LLM 从文本中提取“实体 (Entities)”和“关系 (Relations)”。
    *   **结构化存储**: 存入图数据库（目前使用内存版 `SimplePropertyGraphStore`）。
    *   **检索**: 结合图遍历 (Traversal) 与 向量检索。
*   **成果**：
    *   实现了从文本自动构建图谱。
    *   解决了 `net::ERR_CONNECTION_CLOSED` 问题，实现了离线 HTML 可视化。
    *   演示了通过中间节点 (SpaceX) 推理出马斯克与 NASA 的关系。

---

## 三、 向量数据库深入 (Vector Database)

### ChromaDB
*   **结构**：
    *   基于 SQLite (`chroma.sqlite3`) 存储元数据。
    *   使用 HNSW 算法文件存储向量索引。
*   **操作**：
    *   可以读取 Source Nodes 完整内容。
    *   理解了其底层表结构 (`embeddings`, `embedding_metadata`)。

---

## 四、 关键代码资产 (Code Assets)

| 模块 | 文件路径 | 说明 |
| :--- | :--- | :--- |
| **基础 RAG** | `ai_learn/rag_basics/1_rag_hello_world.py` | 最简 RAG 实现 |
| **ChromaDB** | `ai_learn/rag_basics/debug_chroma_nodes.py` | 查看向量库底层数据 |
| **Rerank** | `ai_learn/rag_advanced/1_rag_with_rerank.py` | 带重排序的高级检索 |
| **Graph RAG** | `ai_learn/graph_rag/1_simple_graph.py` | 知识图谱构建与可视化 |
| **Web UI** | `ai_learn/streamlit_demo/app.py` | Streamlit 聊天应用 |

---

## 五、 下一步计划 (Next Steps)

*   [ ] **Graph RAG 进阶**: 尝试 Neo4j 持久化存储，处理更大规模数据。
*   [ ] **Agent 开发 (Stage 3)**: 进入智能体阶段，学习 Tool Use 和 Workflow。
*   [ ] **综合实战**: 将 RAG、Graph 和 UI 整合到一个完整的“个人知识库助手”中。
