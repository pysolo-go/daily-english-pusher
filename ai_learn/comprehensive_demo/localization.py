
import streamlit as st

TRANSLATIONS = {
    "Home": {
        "page_title": {"en": "AI Learning Hub", "zh": "AI 全栈学习驾驶舱"},
        "title": {"en": "🚀 AI Full Stack Learning Platform", "zh": "🚀 AI 全栈学习综合演练平台"},
        "welcome": {
            "en": """
### Welcome to your AI Learning Cockpit!

Here integrates the core technologies you have learned so far. You can choose different modules in the left sidebar to practice:

*   **🤖 Basic Chat**: Experience basic LLM chat and Prompt engineering.
*   **📚 RAG + Rerank**: Experience the RAG pipeline and compare the effect of Rerank.
*   **🕸️ Knowledge Graph**: Extract entity relationships from text and visualize them.
*   **🧩 Agent Basics**: Experience ReAct pattern, let AI use tools (Math, Weather, Wikipedia).
*   **🔄 Agent Workflow**: Experience event-driven workflows (Generator-Critic Loop) for self-reflection.
*   **🤝 Multi-Agent**: Experience collaboration between Researcher and Writer agents.
*   **🛠️ Finetune Data**: Prepare JSONL dataset for model training.
*   **🧠 PEFT/LoRA**: Learn the concepts behind efficient fine-tuning.

---
#### Current Status
*   **Environment**: Mac OS
*   **Model Provider**: SiliconFlow (DeepSeek/Qwen)
*   **Frameworks**: LlamaIndex, Streamlit
""",
            "zh": """
### 欢迎来到你的 AI 学习驾驶舱！

这里集成了你目前学到的核心技术，可以在左侧导航栏选择不同的模块进行练习：

*   **🤖 基础对话 (Basic Chat)**: 体验最基础的 LLM 对话与 Prompt 效果。
*   **📚 增强检索 (RAG + Rerank)**: 体验 RAG 流程，并对比开启/关闭 "重排序 (Rerank)" 的效果差异。
*   **🕸️ 知识图谱 (Knowledge Graph)**: 输入文本，自动提取实体关系并可视化，体验多跳推理。
*   **🧩 智能体基础 (Agent Basics)**: 体验 ReAct 模式，让 AI 学会使用工具 (天气、数学、维基百科)。
*   **🔄 智能体工作流 (Agent Workflow)**: 体验事件驱动的工作流 (Generator-Critic Loop)，让 AI 具备反思与自我修正能力。
*   **🤝 多智能体协作 (Multi-Agent)**: 体验研究员 (Researcher) 与作家 (Writer) 的协作流程。
*   **🛠️ 微调数据准备 (Finetune Data)**: 准备 JSONL 格式的训练数据。
*   **🧠 PEFT/LoRA 原理**: 学习高效微调的核心概念。

---
#### 当前状态
*   **Environment**: Mac OS
*   **Model Provider**: SiliconFlow (DeepSeek/Qwen)
*   **Frameworks**: LlamaIndex, Streamlit
"""
        },
        "sidebar_tip": {"en": "Please select a demo page above to start!", "zh": "请在上方选择一个演示页面 (Pages) 开始练习！"}
    },
    "Basic_Chat": {
        "page_title": {"en": "Basic Chat", "zh": "基础对话"},
        "header": {"en": "🤖 Basic Chat & Translator", "zh": "🤖 基础对话 & 翻译助手"},
        "model_config": {"en": "Model Configuration", "zh": "模型配置"},
        "provider_select": {"en": "Model Provider", "zh": "模型服务商"},
        "model_select": {"en": "Model Name", "zh": "模型名称"},
        "temperature": {"en": "Temperature (Creativity)", "zh": "Temperature (创造力)"},
        "system_prompt": {"en": "System Prompt (Persona)", "zh": "System Prompt (人设)"},
        "system_prompt_default": {
            "en": "You are a helpful AI assistant. Answer in the language of the user's question.", 
            "zh": "你是一个有用的 AI 助手。请用用户提问的语言回答。"
        },
        "input_placeholder": {"en": "Enter your question...", "zh": "请输入你的问题..."},
    },
    "RAG_Rerank": {
        "page_title": {"en": "RAG + Rerank", "zh": "RAG + Rerank"},
        "header": {"en": "📚 RAG Enhanced Retrieval (Rerank Comparison)", "zh": "📚 RAG 增强检索 (Rerank 对比)"},
        "data_prep": {"en": "1. Data Preparation", "zh": "1. 数据准备"},
        "data_source": {"en": "Select Data Source", "zh": "选择数据来源"},
        "source_options": {"en": ["Use Sample Text", "Upload File (Coming Soon)"], "zh": ["使用示例文本", "上传文件 (暂未开放)"]},
        "input_label": {"en": "Input Text for Retrieval", "zh": "输入需要检索的文本"},
        "build_index": {"en": "🔄 Build/Rebuild Index", "zh": "🔄 构建/重建 索引"},
        "indexing": {"en": "Slicing and Vectorizing...", "zh": "正在切片并向量化..."},
        "index_success": {"en": "Index Built Successfully!", "zh": "索引构建完成！"},
        "qa_retrieval": {"en": "2. Q&A and Retrieval", "zh": "2. 提问与检索"},
        "build_index_first": {"en": "👈 Please build index on the left first", "zh": "👈 请先在左侧构建索引"},
        "query_placeholder": {"en": "Enter your question", "zh": "请输入问题"},
        "query_default": {"en": "What is the invoice amount for ByteDance?", "zh": "购买方是字节跳动的发票金额是多少？"},
        "enable_rerank": {"en": "Enable Rerank", "zh": "启用重排序 (Rerank)"},
        "top_k": {"en": "Initial Retrieval (Top K)", "zh": "初筛数量 (Top K)"},
        "top_n": {"en": "Rerank Retention (Top N)", "zh": "重排后保留 (Top N)"},
        "start_retrieval": {"en": "🔍 Start Retrieval", "zh": "🔍 开始检索"},
        "thinking": {"en": "AI Thinking...", "zh": "AI 思考中..."},
        "answer": {"en": "### 🤖 Answer", "zh": "### 🤖 回答"},
        "source_nodes": {"en": "View Source Nodes", "zh": "查看 AI 检索到的参考片段 (Source Nodes)"},
    },
    "Knowledge_Graph": {
        "page_title": {"en": "Knowledge Graph", "zh": "知识图谱"},
        "header": {"en": "🕸️ Knowledge Graph Construction & Visualization", "zh": "🕸️ 知识图谱构建与可视化"},
        "text_input": {"en": "1. Text Input", "zh": "1. 文本输入"},
        "input_label": {"en": "Input Text (Supports Chinese)", "zh": "输入文本 (支持中文)"},
        "generate_btn": {"en": "🚀 Generate Graph", "zh": "🚀 生成图谱"},
        "generating": {"en": "Analyzing Entity Relationships (may take seconds)...", "zh": "正在分析实体关系 (这可能需要几十秒)..."},
        "success_msg": {"en": "Graph Constructed! Found {} relationships.", "zh": "图谱构建完成！发现 {} 条关系。"},
        "graph_query": {"en": "2. Graph Query", "zh": "2. 图谱查询"},
        "query_placeholder": {"en": "Ask the Graph", "zh": "向图谱提问"},
        "query_default": {"en": "What is the relationship between Elon Musk and NASA?", "zh": "伊隆·马斯克和 NASA 有什么关系？"},
        "query_btn": {"en": "🔍 Query", "zh": "🔍 查询"},
        "reasoning": {"en": "Reasoning...", "zh": "推理中..."},
        "answer": {"en": "### 🤖 Answer", "zh": "### 🤖 回答"},
        "visualization": {"en": "3. Visualization", "zh": "3. 可视化展示"},
        "viz_placeholder": {"en": "Graph will be displayed here after generation", "zh": "生成图谱后在此处显示"},
    },
    "Agent_Basics": {
        "page_title": {"en": "Agent Basics", "zh": "智能体基础"},
        "title": {"en": "🤖 Agent Basics: ReAct Pattern", "zh": "🤖 智能体基础: ReAct 模式"},
        "description": {
            "en": """
This module demonstrates a basic **ReAct (Reasoning + Acting)** Agent.
The Agent has access to **4 tools**, showing how agents can interact with different systems:

1. `multiply(a, b)`: **Math** (Logic)
2. `get_weather(city)`: **Real-time API** (External Data via wttr.in)
3. `search_wikipedia(query)`: **Knowledge** (Encyclopedia via Wikipedia)
4. `get_system_time()`: **System State** (Local environment)

The Agent will **reason** about your query and **decide** which tool(s) to call.
""",
            "zh": """
本模块演示了一个基础的 **ReAct (Reasoning + Acting)** 智能体。
该智能体可以使用 **4 个工具**，展示了 AI 如何与不同系统交互：

1. `multiply(a, b)`: **数学计算** (逻辑能力)
2. `get_weather(city)`: **实时天气** (外部数据，通过 wttr.in)
3. `search_wikipedia(query)`: **维基百科** (知识库)
4. `get_system_time()`: **系统时间** (本地环境状态)

智能体会对你的问题进行 **推理**，并 **决定** 调用哪些工具。
"""
        },
        "history_logs": {"en": "🔍 Historical Logs", "zh": "🔍 历史日志"},
        "input_placeholder": {"en": "Try: 'Weather in Tokyo?', 'Who is Elon Musk?', 'Time now?', '25*4?'", "zh": "尝试输入：'东京天气如何？'，'谁是马斯克？'，'现在几点？'，'25乘以4等于多少？'"},
        "reasoning_logs": {"en": "🔍 Reasoning & Tool Logs", "zh": "🔍 推理与工具调用日志"},
        "no_logs": {"en": "No internal logs captured.", "zh": "未捕获到内部日志。"}
    },
    "Agent_Workflow": {
        "page_title": {"en": "Agent Workflow", "zh": "智能体工作流"},
        "title": {"en": "🔄 Agent Workflow: Reflection Loop", "zh": "🔄 智能体工作流: 反思循环"},
        "description": {
            "en": """
This module demonstrates **LlamaIndex Workflows** (Event-Driven Architecture).
Unlike a simple linear chain, a Workflow can have **loops**, **branches**, and **state**.

**The Scenario: Joke Creator & Critic**
1.  **Creator**: Writes a joke about a topic.
2.  **Critic**: Reviews the joke and gives a score (1-10) and feedback.
3.  **Decision**: 
    -   If Score > 7: ✅ Success!
    -   If Score <= 7: ❌ Reject, send feedback back to Creator to improve.
""",
            "zh": """
本模块演示了 **LlamaIndex Workflows** (事件驱动架构)。
与简单的线性链不同，工作流可以包含 **循环**、**分支** 和 **状态**。

**场景：笑话创作者与评论家**
1.  **创作者 (Creator)**: 围绕主题创作一个笑话。
2.  **评论家 (Critic)**: 评审笑话并给出评分 (1-10) 和反馈。
3.  **决策**: 
    -   如果评分 > 7: ✅ 成功！
    -   如果评分 <= 7: ❌ 拒绝，将反馈发回给创作者进行改进。
"""
        },
        "topic_input": {"en": "Enter a topic for the joke:", "zh": "输入笑话的主题："},
        "start_btn": {"en": "Start Workflow", "zh": "开始工作流"},
        "running": {"en": "Running Workflow...", "zh": "正在运行工作流..."},
        "final_result": {"en": "### 🏁 Final Result", "zh": "### 🏁 最终结果"},
        "error": {"en": "Workflow Error: {}", "zh": "工作流错误: {}"},
        "generator_attempt": {"en": "**Attempt {} (Generator)**: Generating joke about '{}'...", "zh": "**尝试 {} (生成器)**: 正在生成关于 '{}' 的笑话..."},
        "generated_joke": {"en": "🃏 **Generated Joke**: {}", "zh": "🃏 **生成的笑话**: {}"},
        "max_attempts_reached": {"en": "Maximum attempts reached. The critic is too tough!", "zh": "达到最大尝试次数。评论家太严格了！"},
        "generator_improve": {"en": "**Attempt {} (Generator)**: Improving joke based on feedback...", "zh": "**尝试 {} (生成器)**: 根据反馈改进笑话..."},
        "critic_reviewing": {"en": "**Attempt {} (Critic)**: Reviewing...", "zh": "**尝试 {} (评论家)**: 正在评审..."},
        "critic_review_output": {"en": "🧐 **Critic Review**: {}", "zh": "🧐 **评论家评审**: {}"},
        "success_msg": {"en": "🎉 **Success!** Score {}/10 is good enough.", "zh": "🎉 **成功！** 得分 {}/10 足够好了。"},
        "reject_msg": {"en": "❌ **Rejected!** Score {}/10 is too low. Retrying...", "zh": "❌ **拒绝！** 得分 {}/10 太低。重试中..."},
        "prompt_gen": {"en": "Tell me a short, funny joke about {}.", "zh": "给我讲一个关于 {} 的简短有趣的笑话。"},
        "prompt_improve": {
            "en": "The previous joke about {} was rejected.\nPrevious Joke: {}\nCritic Feedback: {}\nPlease write a BETTER, funnier joke considering the feedback.",
            "zh": "关于 {} 的上一个笑话被拒绝了。\n上一个笑话: {}\n评论家反馈: {}\n请根据反馈写一个更好、更有趣的笑话。"
        },
        "prompt_review": {
            "en": "Rate this joke on a scale of 1 to 10 (integer only) and give brief feedback.\nJoke: {}\nFormat: SCORE: <number>\nFEEDBACK: <text>",
            "zh": "请对这个笑话进行评分（1到10分，仅整数）并给出简短反馈。\n笑话: {}\n格式: SCORE: <数字>\nFEEDBACK: <文本>"
        }
    },
    "Multi_Agent": {
        "page_title": {"en": "Multi-Agent Collaboration", "zh": "多智能体协作"},
        "title": {"en": "🤝 Multi-Agent Collaboration: Research & Write", "zh": "🤝 多智能体协作: 研究与写作"},
        "description": {
            "en": """
This module demonstrates **Sequential Multi-Agent Collaboration**.
Instead of one generalist AI, we use two specialist Agents working in a pipeline:

1.  **Researcher Agent**: 
    -   Role: Information gatherer.
    -   Task: Searches for facts about the topic.
    -   Output: A detailed, factual report.
2.  **Writer Agent**: 
    -   Role: Content creator.
    -   Task: Takes the Researcher's report and writes a blog post.
    -   Output: An engaging article.

**Why?** This separation of concerns reduces hallucinations and improves content quality.
""",
            "zh": """
本模块演示了 **顺序多智能体协作 (Sequential Multi-Agent Collaboration)**。
我们不再使用一个通用的 AI，而是让两个专才智能体像流水线一样工作：

1.  **研究员 (Researcher)**:
    -   角色: 信息收集者。
    -   任务: 针对主题搜集事实。
    -   输出: 一份详实的事实报告。
2.  **作家 (Writer)**:
    -   角色: 内容创作者。
    -   任务: 根据研究员的报告撰写博客文章。
    -   输出: 一篇引人入胜的文章。

**为什么？** 这种职责分离 (Separation of Concerns) 能有效减少幻觉，并提高内容质量。
"""
        },
        "topic_label": {"en": "Enter a Topic", "zh": "输入一个主题"},
        "topic_placeholder": {"en": "e.g., The Future of Quantum Computing, How to bake a cake", "zh": "例如：量子计算的未来，如何烤蛋糕"},
        "start_btn": {"en": "🚀 Start Collaboration", "zh": "🚀 开始协作"},
        "warning_topic": {"en": "Please enter a topic first.", "zh": "请先输入一个主题。"},
        "step_research": {"en": "🕵️‍♂️ Researcher is working...", "zh": "🕵️‍♂️ 研究员正在工作..."},
        "step_write": {"en": "✍️ Writer is working...", "zh": "✍️ 作家正在工作..."},
        "done": {"en": "✅ Collaboration Finished!", "zh": "✅ 协作完成！"},
        "final_result": {"en": "### 📝 Final Article", "zh": "### 📝 最终文章"},
        "error": {"en": "Error occurred: {}", "zh": "发生错误: {}"}
    },
    "Finetune_Data": {
        "page_title": {"en": "Finetune Data Prep", "zh": "微调数据准备"},
        "title": {"en": "🛠️ Fine-tuning Dataset Builder", "zh": "🛠️ 微调数据集构建器"},
        "description": {
            "en": """
**Phase 4.2: Fine-tuning Data Preparation**

To train a specialized model (e.g., a "Legal Assistant" or "Medical Expert"), you cannot just use raw text.
You need to teach the model **how to answer** by providing examples in a specific format (JSONL).

**Format Structure:**
- **System**: The persona (e.g., "You are a lawyer").
- **User**: The question/instruction.
- **Assistant**: The ideal answer you want the model to learn.

Use this tool to build your first dataset!
""",
            "zh": """
**阶段 4.2: 微调数据准备 (Data Preparation)**

要训练一个专用模型（例如“法律助手”或“医疗专家”），不能只给它看原始文档。
你需要通过提供特定格式 (JSONL) 的问答对，教模型 **“该怎么回答”**。

**核心结构：**
- **System (人设)**: 模型的身份（如“你是一名律师”）。
- **User (指令)**: 用户的问题或指令。
- **Assistant (回答)**: 你希望模型学习的“标准答案”。

使用此工具来构建你的第一个微调数据集！
"""
        },
        "system_label": {"en": "System Prompt", "zh": "System Prompt (人设)"},
        "user_label": {"en": "User Instruction", "zh": "User Instruction (用户指令)"},
        "assistant_label": {"en": "Assistant Response (Standard Answer)", "zh": "Assistant Response (标准答案)"},
        "add_btn": {"en": "➕ Add to Dataset", "zh": "➕ 添加到数据集"},
        "preview_header": {"en": "📊 Dataset Preview (JSONL)", "zh": "📊 数据集预览 (JSONL)"},
        "download_btn": {"en": "📥 Download .jsonl", "zh": "📥 下载 .jsonl 文件"},
        "clear_btn": {"en": "🗑️ Clear Dataset", "zh": "🗑️ 清空数据集"},
        "success_add": {"en": "Added 1 record!", "zh": "已添加 1 条数据！"},
        
        # Enhanced Data Prep Content
        "tab_editor": {"en": "📝 Data Editor", "zh": "📝 数据编辑器"},
        "tab_guide": {"en": "📚 Concept Guide", "zh": "📚 概念指南"},
        "template_label": {"en": "Load Template", "zh": "加载模板"},
        "template_none": {"en": "None (Custom)", "zh": "无 (自定义)"},
        "template_chat": {"en": "General Chat", "zh": "通用对话"},
        "template_code": {"en": "Code Generation", "zh": "代码生成"},
        "template_medical": {"en": "Medical Consultation", "zh": "医疗咨询"},
        "guide_title": {"en": "Understanding Instruction Tuning Data", "zh": "理解指令微调数据"},
        "guide_intro": {
            "en": "To fine-tune an LLM, we need to show it examples of **how to follow instructions**.",
            "zh": "为了微调 LLM，我们需要给它展示 **“如何遵循指令”** 的示例。"
        },
        "guide_structure_title": {"en": "The Structure (JSONL)", "zh": "核心结构 (JSONL)"},
        "guide_structure_desc": {
            "en": "Each line in the file is a separate training example. It usually contains 3 roles:",
            "zh": "文件中的每一行都是一个独立的训练样本。通常包含 3 个角色："
        },
        "role_system": {"en": "**System**: Sets the behavior/persona.", "zh": "**System (系统)**: 设定模型的行为或人设。"},
        "role_user": {"en": "**User**: The input/prompt.", "zh": "**User (用户)**: 用户的输入或指令。"},
        "role_assistant": {"en": "**Assistant**: The ideal output you want the model to learn.", "zh": "**Assistant (助手)**: 你希望模型学习的理想输出（标准答案）。"},
        "quality_title": {"en": "Quality Checklist", "zh": "高质量数据清单"},
        "checklist_1": {"en": "✅ **Diversity**: Don't just repeat the same pattern.", "zh": "✅ **多样性**: 不要重复同一种句式或问题。"},
        "checklist_2": {"en": "✅ **Correctness**: The 'Assistant' answer must be 100% correct.", "zh": "✅ **准确性**: Assistant 的回答必须是 100% 正确的（因为模型会模仿它）。"},
        "checklist_3": {"en": "✅ **Completeness**: Avoid short, lazy answers if you want detailed outputs.", "zh": "✅ **完整性**: 如果你想要详细的回答，不要提供简短、敷衍的样本。"}
    },
    "PEFT_Concepts": {
        "page_title": {"en": "PEFT & LoRA Concepts", "zh": "微调技术原理 (PEFT/LoRA)"},
        "title": {"en": "🧠 Fine-tuning & LoRA: Under the Hood", "zh": "🧠 微调与 LoRA：技术揭秘"},
        "tab_concepts": {"en": "Full vs PEFT", "zh": "全量微调 vs PEFT"},
        "tab_lora": {"en": "LoRA Principle", "zh": "LoRA 核心原理"},
        "tab_data": {"en": "Data Construction Guide", "zh": "数据构建指南"},
        
        # Tab 1: Concepts
        "concept_full_title": {"en": "Full Fine-tuning (FFT)", "zh": "全量微调 (Full Fine-tuning)"},
        "concept_full_desc": {
            "en": "Updates **ALL** parameters of the model. Expensive and slow.", 
            "zh": "更新模型的所有参数。成本高，速度慢，显存需求极大。"
        },
        "concept_peft_title": {"en": "Parameter-Efficient Fine-tuning (PEFT)", "zh": "参数高效微调 (PEFT)"},
        "concept_peft_desc": {
            "en": "Updates only a **small subset** of parameters (or adds adapters). Fast and cheap.", 
            "zh": "仅更新极少量的参数（或添加适配器）。速度快，成本低，甚至能在消费级显卡上运行。"
        },
        "analogy": {"en": "💡 Analogy", "zh": "💡 通俗类比"},
        "analogy_text": {
            "en": "**FFT**: Rewriting the entire textbook to add a new chapter.\n**PEFT**: Adding a sticky note or a bookmark to the existing book.",
            "zh": "**全量微调**: 为了增加一章新内容，把整本教科书重新抄写一遍。\n**PEFT**: 在书里夹一张便利贴或书签，只写新内容。"
        },

        # Tab 2: LoRA
        "lora_title": {"en": "LoRA: Low-Rank Adaptation", "zh": "LoRA: 低秩自适应"},
        "lora_desc": {
            "en": "LoRA freezes the pre-trained weights $W_0$ and injects trainable rank decomposition matrices $A$ and $B$.",
            "zh": "LoRA 冻结预训练权重 $W_0$，并注入可训练的低秩分解矩阵 $A$ 和 $B$。"
        },
        "formula": {"en": "Formula", "zh": "核心公式"},
        "params_saved": {"en": "Parameters Reduced", "zh": "参数量减少"},
        "qlora_note": {"en": "QLoRA = 4-bit Quantization + LoRA (Even less memory!)", "zh": "QLoRA = 4-bit 量化 + LoRA (显存占用更低！)"},

        # Tab 3: Data
        "data_title": {"en": "How to Construct Instruction Data", "zh": "如何构建指令微调数据"},
        "data_step1": {"en": "1. Data Cleaning", "zh": "1. 数据清洗"},
        "data_step1_desc": {"en": "Remove noise, HTML tags, duplicate punctuation.", "zh": "去除噪声、HTML标签、重复标点、乱码等。"},
        "data_step2": {"en": "2. Instruction Formatting", "zh": "2. 构造指令 (Instruction)"},
        "data_step2_desc": {"en": "Transform raw text into QA pairs or Task-Response pairs.", "zh": "将原始文本转化为“问答对”或“任务-响应”对。"},
        "good_bad_example": {"en": "Good vs Bad Examples", "zh": "优质 vs 劣质 示例"},
        "bad_label": {"en": "❌ Bad", "zh": "❌ 劣质"},
        "good_label": {"en": "✅ Good", "zh": "✅ 优质"},
        "goto_page7": {"en": "👉 Go to Data Prep Tool", "zh": "👉 前往数据准备工具实战"},

        # Diagram Translations
        "diag_train_data": {"en": "Training Data", "zh": "训练数据"},
        "diag_pretrained": {"en": "Pre-trained Model\\n(10B Params)", "zh": "预训练模型\\n(100亿参数)"},
        "diag_new_model": {"en": "New Model\\n(10B Params)", "zh": "新模型\\n(100亿参数)"},
        "diag_update_all": {"en": "Update ALL Weights", "zh": "更新所有权重"},
        
        "diag_pretrained_frozen": {"en": "Pre-trained Model\\n(Frozen)", "zh": "预训练模型\\n(已冻结)"},
        "diag_adapter": {"en": "Adapter / LoRA\\n(10M Params)", "zh": "适配器 / LoRA\\n(1000万参数)"},
        "diag_output": {"en": "Final Output", "zh": "最终输出"},
        "diag_update_adapter": {"en": "Update ONLY Adapter", "zh": "仅更新适配器"},

        # New Beginner Content
        "why_title": {"en": "Why Fine-tune?", "zh": "为什么需要微调？"},
        "why_desc": {"en": "General models (like GPT-4) are smart, but specialized models are better at:", "zh": "通用模型 (如 GPT-4) 虽然聪明，但在以下场景，微调后的专用模型更强："},
        "use_case_1": {"en": "🏥 **Domain Knowledge**: Medical, Legal, Finance.", "zh": "🏥 **注入领域知识**: 医疗、法律、金融等垂直领域的专业术语。"},
        "use_case_2": {"en": "🎭 **Style & Tone**: Roleplay, Speaking like a specific person.", "zh": "🎭 **调整语气风格**: 角色扮演 (如“猫娘”、“高情商客服”)、模仿特定文风。"},
        "use_case_3": {"en": "📋 **Format Control**: Strict JSON/SQL output.", "zh": "📋 **固定输出格式**: 强迫模型稳定输出 JSON、SQL 或特定代码格式，便于程序解析。"},
        
        "rag_vs_ft_title": {"en": "Fine-tuning vs RAG vs Prompting", "zh": "微调 vs RAG vs 提示词工程"},
        "comp_prompt": {"en": "🗣️ **Prompting**", "zh": "🗣️ **提示词 (Prompt)**"},
        "comp_prompt_desc": {"en": "Temporary instructions. Context window limit.", "zh": "临时的指令。像“对人说一句话”。缺点是记不住，且有长度限制。"},
        "comp_rag": {"en": "📚 **RAG (Retrieval)**", "zh": "📚 **RAG (检索增强)**"},
        "comp_rag_desc": {"en": "Open-book exam. Good for factual retrieval.", "zh": "像“开卷考试”。遇到问题先去翻书 (知识库)。适合企业文档问答。"},
        "comp_ft": {"en": "🧠 **Fine-tuning**", "zh": "🧠 **微调 (Fine-tuning)**"},
        "comp_ft_desc": {"en": "Internalizing knowledge. Muscle memory.", "zh": "像“专业进修”。把知识内化进大脑，形成肌肉记忆。适合学习特定的说话方式或复杂逻辑。"},

        "lifecycle_title": {"en": "The Fine-tuning Lifecycle", "zh": "微调全流程"},
        "step_1": {"en": "1. Data Prep", "zh": "1. 数据准备"},
        "step_1_desc": {"en": "QA Pairs (JSONL)", "zh": "准备问答对 (JSONL)"},
        "step_2": {"en": "2. Base Model", "zh": "2. 选基座模型"},
        "step_2_desc": {"en": "Qwen/Llama/DeepSeek", "zh": "Qwen/Llama/DeepSeek"},
        "step_3": {"en": "3. LoRA Train", "zh": "3. LoRA 训练"},
        "step_3_desc": {"en": "GPU Calculation", "zh": "GPU 显卡计算"},
        "step_4": {"en": "4. Merge/Serve", "zh": "4. 导出与使用"},
        "step_4_desc": {"en": "New Model", "zh": "获得新模型"}
    },
    "Video_Subtitle": {
        "page_title": {"en": "AI Video Translator", "zh": "AI 视频字幕翻译"},
        "title": {"en": "🎬 AI Video Subtitle Generator & Translator", "zh": "🎬 AI 视频双语字幕生成器"},
        "description": {
            "en": """
**Real-time video translation is hard, but Offline Batch Processing is standard.**

This tool demonstrates the full pipeline of **AI Video Localization**:
1.  **Extract Audio**: Get sound from video file.
2.  **ASR (Whisper)**: Speech-to-Text with high accuracy.
3.  **LLM Translation**: Translate subtitles segment by segment.
4.  **Synthesis**: Generate WebVTT subtitles and overlay on video.
""",
            "zh": """
**虽然Web端很难做到“边播边译”的实时流，但“离线处理”是工业界的标准方案。**

本工具演示了 **AI 视频本地化** 的全流程：
1.  **音频提取**: 从视频文件中分离音轨。
2.  **语音转写 (ASR)**: 使用 OpenAI Whisper 模型进行高精度语音识别。
3.  **LLM 翻译**: 将识别出的英文字幕逐句翻译成中文。
4.  **字幕合成**: 生成 WebVTT 双语字幕文件，并挂载到播放器。
"""
        },
        "upload_label": {"en": "Upload a Video (MP4/MOV)", "zh": "上传视频文件 (MP4/MOV/AVI)"},
        "process_btn": {"en": "🚀 Start Processing", "zh": "🚀 开始生成双语字幕"},
        "processing_step1": {"en": "1️⃣ Extracting Audio...", "zh": "1️⃣ 正在提取音频..."},
        "processing_step2": {"en": "2️⃣ Transcribing with Whisper (ASR)...", "zh": "2️⃣ 正在进行语音识别 (Whisper)..."},
        "processing_step3": {"en": "3️⃣ Translating with LLM...", "zh": "3️⃣ 正在调用大模型翻译..."},
        "processing_step3_progress": {"en": "Translating segment {}/{}...", "zh": "正在翻译第 {}/{} 句..."},
        "success": {"en": "✅ Done! Enjoy your video.", "zh": "✅ 处理完成！请观看下方视频。"},
        "download_vtt": {"en": "📥 Download Subtitles (.vtt)", "zh": "📥 下载字幕文件 (.vtt)"},
        "error_no_model": {"en": "Please configure LLM in 'Basic Chat' first!", "zh": "请先在 '基础对话' 页面配置模型 API！"},
        "model_loading": {"en": "Loading Whisper model (first time may take a while)...", "zh": "正在加载 Whisper 模型 (首次运行会自动下载，请耐心等待)..."}
    }
}

def get_text(page, key, lang="zh"):
    """
    Get translated text.
    :param page: Page key (e.g., "Home", "Basic_Chat")
    :param key: Text key
    :param lang: Language code ("en" or "zh")
    :return: Translated text
    """
    try:
        return TRANSLATIONS[page][key][lang]
    except KeyError:
        return f"MISSING TRANSLATION: {page}.{key}.{lang}"

def init_lang():
    """Initialize language state."""
    if "lang" not in st.session_state:
        st.session_state.lang = "zh"

def lang_selector():
    """Render language selector (Fixed Top-Right Dropdown)."""
    lang_options = {"中文": "zh", "English": "en"}
    
    # Inject CSS for fixed positioning and styling
    st.markdown(
        """
        <style>
        /* Target the specific selectbox container by assuming it's the first one in the main area */
        /* Since we render it first, we can target the first stSelectbox in the main container */
        
        div[data-testid="stSelectbox"] {
            /* We can't target just *this* one easily without a unique class, 
               but we can try targeting the one that is inside the container we are about to create?
               No, Streamlit flattens logic. 
               
               Strategy: Target the stSelectbox that is FIRST child of the FIRST VerticalBlock?
            */
        }
        
        /* 
           Robust Approach:
           Target the element by its proximity to the top of the page.
           But to be safe, we will assume this is the first selectbox.
        */
        
        div[data-testid="stSelectbox"]:nth-of-type(1) {
            position: fixed !important;
            top: 10px; /* Adjusted for taller box */
            right: 180px;
            width: 120px;
            z-index: 1000001;
        }

        /* Adjust the inner input box to be transparent and minimal */
        div[data-testid="stSelectbox"]:nth-of-type(1) > div > div {
            min-height: 40px; /* Increased height to accommodate descenders */
            height: 40px;
            background-color: transparent;
            border: none;
            color: inherit;
            overflow: visible; /* Ensure text isn't clipped */
        }
        
        /* Remove the focus outline/shadow to keep it clean */
        div[data-testid="stSelectbox"]:nth-of-type(1) > div > div:focus-within {
            box-shadow: none;
            border: 1px solid rgba(49, 51, 63, 0.2);
        }
        
        /* Adjust the dropdown text alignment and padding */
        div[data-testid="stSelectbox"]:nth-of-type(1) div[data-testid="stMarkdownContainer"] p {
            font-size: 0.9rem;
            font-weight: 500;
            white-space: nowrap;
            overflow: visible;
            line-height: 40px; /* Center text vertically */
            padding-bottom: 2px; /* Extra nudge for descenders */
        }

        /* Adjust the dropdown arrow container */
        div[data-testid="stSelectbox"]:nth-of-type(1) > div > div > div[role="button"] {
             line-height: 40px;
        }
        
        /* Hide the upper right decoration if it interferes */
        header[data-testid="stHeader"] {
            z-index: 1000000;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # Render the selectbox directly (no columns, to keep DOM simple)
    st.selectbox(
        "Language",
        options=list(lang_options.keys()),
        index=0 if st.session_state.get("lang", "zh") == "zh" else 1,
        key="lang_select",
        on_change=_update_lang,
        label_visibility="collapsed"
    )

def _update_lang():
    """Callback to update session state when language changes."""
    selected_label = st.session_state.lang_select
    lang_map = {"中文": "zh", "English": "en"}
    st.session_state.lang = lang_map[selected_label]


def render_sidebar():
    """
    Render custom sidebar with translated navigation.
    Hides the default Streamlit sidebar navigation.
    """
    lang = st.session_state.get("lang", "zh")
    
    # CSS to hide default sidebar nav
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    with st.sidebar:
        st.header(get_text("Home", "page_title", lang) if lang == "zh" else "Navigation")
        
        # Define pages
        pages = [
            {"page": "Home.py", "label": get_text("Home", "page_title", lang), "icon": "🏠"},
            {"page": "pages/1_Basic_Chat.py", "label": get_text("Basic_Chat", "page_title", lang), "icon": "🤖"},
            {"page": "pages/2_RAG_Rerank.py", "label": get_text("RAG_Rerank", "page_title", lang), "icon": "📚"},
            {"page": "pages/3_Knowledge_Graph.py", "label": get_text("Knowledge_Graph", "page_title", lang), "icon": "🕸️"},
            {"page": "pages/4_Agent_Basics.py", "label": get_text("Agent_Basics", "page_title", lang), "icon": "🧩"},
            {"page": "pages/5_Agent_Workflow.py", "label": get_text("Agent_Workflow", "page_title", lang), "icon": "🔄"},
            {"page": "pages/6_Multi_Agent_Collaboration.py", "label": get_text("Multi_Agent", "page_title", lang), "icon": "🤝"},
            {"page": "pages/7_Finetune_Data_Prep.py", "label": get_text("Finetune_Data", "page_title", lang), "icon": "🛠️"},
            {"page": "pages/8_PEFT_LoRA_Concepts.py", "label": get_text("PEFT_Concepts", "page_title", lang), "icon": "🧠"},
        ]
        
        for p in pages:
            st.page_link(p["page"], label=p["label"], icon=p["icon"])
