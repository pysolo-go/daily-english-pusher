# 这个脚本展示了如何用代码来管理和生成高质量的 Prompt
# 这就是 "Prompt Engineering" 中的 "Engineering" (工程化) 部分

def basic_prompt(user_input):
    """基础 Prompt：直接拼接"""
    return f"请回答这个问题：{user_input}"

def few_shot_prompt(user_input):
    """Few-shot Prompt：通过示例增强效果"""
    template = """
你是一个情感分析助手。请判断以下评论的情感是正面、负面还是中性。

示例 1:
评论：这个手机电池太不耐用了！
情感：负面

示例 2:
评论：快递很快，包装也很精美。
情感：正面

示例 3:
评论：今天的午饭普普通通。
情感：中性

请分析以下评论：
评论：{input_text}
情感：
"""
    return template.format(input_text=user_input)

def cot_prompt(math_problem):
    """Chain of Thought (CoT)：思维链"""
    template = """
你是一个数学专家。请解决以下问题。
重要：不要直接给出答案，请使用 "Let's think step by step" 的格式，一步步写出你的推理过程。

问题：{problem}

推理过程：
"""
    return template.format(problem=math_problem)

def structured_prompt(role, topic):
    """结构化 Prompt：像写配置文件一样写 Prompt"""
    return f"""
# Role
你是一位世界级的 {role}。

# Goal
为用户生成一篇关于 "{topic}" 的深度文章。

# Constraints (约束)
- 字数：500字左右
- 风格：幽默风趣，多用比喻
- 格式：使用 Markdown，包含标题和加粗重点

# Workflow
1. 先列出文章大纲。
2. 逐步填充内容。
3. 最后生成一个金句作为结尾。

# Initialization
现在，请开始你的创作。
"""

if __name__ == "__main__":
    print("--- 1. Few-shot (少样本) 演示 ---")
    user_comment = "这衣服洗了一次就缩水了，真心无语。"
    print(few_shot_prompt(user_comment))
    
    print("\n" + "="*30 + "\n")
    
    print("--- 2. CoT (思维链) 演示 ---")
    problem = "小明有 5 个苹果，吃了 2 个。妈妈又给了他 3 个，爸爸拿走了 1 个。小明现在有几个？"
    print(cot_prompt(problem))
    
    print("\n" + "="*30 + "\n")
    
    print("--- 3. 结构化 Prompt 演示 ---")
    print(structured_prompt(role="科普作家", topic="量子纠缠"))
