# 2025 AI 全栈工程师 / 超级个体 学习路线图 (终极优化版)

> **规划说明**：本路线图基于 [AGIClass 知识体系](https://agiclass.feishu.cn/docx/Z3Aed6qXboiF8gxGuaccNHxanOc) 进行深度优化与前沿扩展。
> 
> **核心理念**：**“应用驱动，原理补全”**。不建议从枯燥的数学公式开始，而是先学会用（Prompt/API），再学会造（RAG/Agent），最后学会调（Fine-tuning/Training）。
> **适用人群**：希望从零成为具备工程落地能力的 AI 全栈开发者。

---

## 阶段一：基石构建 —— 掌握 AI 时代的“新语言”
**目标**：能够熟练使用主流 LLM，理解 Prompt 本质，完成简单的 API 开发。

### 1.1 基础工具准备
- **Python 进阶**：不仅是语法，重点掌握 `asyncio` (并发)、`FastAPI` (接口)、`Pydantic` (数据校验，Agent 开发必备)。
- **环境管理**：Conda/Venv，以及 **Docker** (部署必备)。
- **Git/GitHub**：代码版本管理与开源协作。

### 1.2 大模型基础与 Prompt Engineering (提示工程)
- **核心概念**：Token、Context Window、Temperature、Top-P。
- **提示词方法论**：
  - IC-Learning (In-Context Learning)
  - CoT (Chain of Thought) 思维链
  - ToT (Tree of Thoughts)
  - **结构化提示词** (LangGPT 范式 / CO-STAR 框架)
- **实战项目**：
  - 编写一个“代码审计专家”或“雅思口语教练”的 System Prompt。
  - 使用 DeepSeek-R1 / ChatGPT-4o 对比不同提示词的效果。

### 1.3 API 开发入门
- **主流接口**：OpenAI SDK (行业标准)、DeepSeek API (高性价比)、Anthropic (Claude)。
- **封装技巧**：流式输出 (Streaming)、简单的对话历史管理。

---

## 阶段二：构建外脑 —— RAG (检索增强生成)
**目标**：解决大模型“幻觉”与“知识滞后”问题，搭建企业级知识库。
*这是目前 B 端落地最广泛的技术方向。*

### 2.1 RAG 核心架构
- **ETL 流程**：文档加载 (PDF/Markdown) -> 切片 (Chunking) -> 向量化 (Embedding)。
- **向量数据库**：
  - 入门：ChromaDB, FAISS (本地)。
  - 进阶：Pinecone, Milvus, Weaviate (生产级)。
- **检索算法**：
  - 关键词检索 (BM25) vs 向量检索 (Dense Retrieval)。
  - **混合检索 (Hybrid Search)**：Rerank (重排序) 模型的使用 (如 BGE-Reranker)。

### 2.2 开发框架 (已掌握 LlamaIndex/LangChain 基础)
- **LangChain**：由于其复杂性，建议仅作为学习组件库。
- **LlamaIndex**：**强烈推荐**，专为数据与 RAG 设计，架构更清晰。

### 2.3 进阶 RAG (GraphRAG) (正在进行 - 已完成基础图谱构建)
- **知识图谱结合**：使用 Neo4j 构建 GraphRAG，解决跨文档推理问题。
- **实战项目**：
  - 开发一个“个人财报分析助手”：上传 PDF 财报，精准回答财务数据。

---

## 阶段三：赋予手脚 —— Agent (智能体) 与 Workflow
**目标**：让 AI 不仅能“说”，还能“做”。
*这是 2024-2025 最前沿的方向，从 Chat 到 Action 的跨越。*

### 3.1 Agent 核心范式
- **ReAct**：Reasoning + Acting 循环。
- **Tool Use (Function Calling)**：让大模型调用计算器、搜索、数据库、API。
- **Planning**：任务拆解与自我反思 (Reflection)。

### 3.2 编排框架
- **LangGraph** (Python)：基于图论的 Agent 编排，目前最灵活的生产级选择。
- **Dify / Coze** (低代码)：快速原型搭建，理解 Agent 工作流逻辑 (Workflow) 的最佳入口。
- **CrewAI / AutoGen**：多智能体协作 (Multi-Agent) 框架。

### 3.3 实战项目
- **全自动研报生成器**：
  1. 搜索 Agent：联网搜集信息。
  2. 阅读 Agent：总结网页内容。
  3. 写作 Agent：整合生成文章。
  4. 审核 Agent：检查事实错误。

---

## Phase 4: Privatization and Customization — Fine-tuning and Open Source Models
Target: Surpass general LLMs in vertical domains, master model privatization.

### 4.1 Open Source Model Ecosystem (Done ✅)
- **Ollama**: God tool for beginners, run LLMs with one command.
  - Action: Install Ollama and pull `qwen2.5:1.5b`.
  - Action: Integrate Local Model into `Basic_Chat`.
- **LM Studio**: Visual local runner (Optional).
- **Hugging Face**: The GitHub of AI models.

### 4.2 微调技术 (PEFT)
- **全量微调 vs 参数高效微调**。
- **LoRA / QLoRA**：低成本微调的核心技术。
- **数据集构建**：如何清洗数据、构造指令微调 (Instruction Tuning) 数据对。

### 4.3 模型量化与推理加速
- **量化**：GGUF 格式, AWQ, GPTQ (让 70B 模型跑在消费级显卡上)。
- **推理引擎**：vLLM (吞吐量霸主), TensorRT-LLM。

---

## 阶段五：多模态与 AIGC (扩展技能)
**目标**：处理图像、音频、视频数据。

- **视觉理解 (VLM)**：LLaVA, GPT-4v, Qwen-VL。
- **图像生成**：Stable Diffusion WebUI / ComfyUI (节点式工作流，强烈推荐)。
- **音频处理**：Whisper (语音转文字), CosyVoice / ChatTTS (文字转语音)。

---

## 阶段六：工程化与 MLOps (迈向资深)
**目标**：将 Demo 变为高可用、可监控的生产级应用。

- **评估 (Evaluation)**：
  - **Ragas**：评估 RAG 的检索准确率与生成质量。
  - **LLM-as-a-Judge**：用强模型评测弱模型。
- **监控与追踪**：LangSmith, LangFuse (记录每一次 Token 消耗与延迟)。
- **安全与风控**：Prompt Injection 防御，内容合规检测。

---

## 学习路径推荐表

| 阶段 | 核心关键词 | 推荐项目/动作 | 预计耗时 |
| :--- | :--- | :--- | :--- |
| **入门** | Python, API, Prompt | 搭建一个翻译 Bot，部署到飞书/微信 | 2 周 |
| **进阶** | RAG, LlamaIndex, Vector DB | 搭建“个人知识库”，支持 PDF 问答 | 3-4 周 |
| **高阶** | Agent, LangGraph, Tools | 开发“自动联网调研助手” | 4 周 |
| **专家** | Fine-tuning, vLLM, Eval | 微调一个“法律/医疗咨询专属模型” | 长期 |

## 推荐资源库

- **课程**：Andrew Ng (DeepLearning.AI) 系列课程（特别是 Agent 和 RAG 专题）。
- **资讯**：Hugging Face Daily Papers, ArXiv, 机器之心。
- **代码**：阅读 LangChain 和 LlamaIndex 的官方文档与源码（比任何教程都新）。
