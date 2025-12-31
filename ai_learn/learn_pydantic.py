from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

# 1. 定义数据模型
# 为什么在 AI 开发中这很重要？
# 当你要求 LLM (如 ChatGPT/DeepSeek) 返回 JSON 格式的数据时，
# Pydantic 可以定义这个 JSON 必须长什么样。
# 这就是 "Structured Output" (结构化输出) 的基础。

class Skill(BaseModel):
    name: str = Field(..., description="技能名称，如 Python, RAG")
    proficiency: int = Field(..., ge=1, le=10, description="熟练度 1-10")

class AI_Engineer(BaseModel):
    name: str = Field(..., description="工程师姓名")
    age: int = Field(..., gt=0, description="年龄，必须大于0")
    # Optional 表示该字段可以为空
    focus_area: Optional[str] = Field(None, description="专注领域，如 NLP, CV")
    # 嵌套模型：一个工程师有多个技能
    skills: List[Skill] = Field(default_factory=list, description="掌握的技能列表")

# 2. 模拟 LLM 返回的原始数据 (通常是不可靠的字典/JSON)
raw_data_success = {
    "name": "Solo",
    "age": 28,
    "focus_area": "Agentic Workflow",
    "skills": [
        {"name": "Python", "proficiency": 9},
        {"name": "Pydantic", "proficiency": 8},
        {"name": "Prompt Engineering", "proficiency": 10}
    ]
}

# 模拟一个脏数据 (LLM 经常会犯错，比如类型不对，或者漏字段)
raw_data_error = {
    "name": "Buggy AI",
    "age": "not a number", # 错误：类型不对
    "skills": [
        {"name": "Java", "proficiency": 100} # 错误：超过了 1-10 的范围
    ]
}

def demo_pydantic():
    print("--- 1. 成功解析演示 ---")
    try:
        # 实例化模型，Pydantic 会自动进行类型转换和校验
        engineer = AI_Engineer(**raw_data_success)
        print(f"✅ 解析成功: {engineer.name} 专注于 {engineer.focus_area}")
        print(f"   技能树: {[s.name for s in engineer.skills]}")
        
        # 导出为 JSON (这是传给前端或存储到数据库的格式)
        print(f"   JSON 输出: {engineer.model_dump_json()}")
    except ValidationError as e:
        print(e)

    print("\n--- 2. 错误捕获演示 (数据校验) ---")
    try:
        AI_Engineer(**raw_data_error)
    except ValidationError as e:
        print("❌ 捕获到数据错误！Pydantic 帮我们挡住了脏数据：")
        # e.json() 会告诉你是哪个字段错了，为什么错
        print(e.json(indent=2))

    print("\n--- 3. AI Agent 场景：生成 Schema ---")
    print("告诉 LLM 我们需要什么格式的数据 (Function Calling 基础):")
    # model_json_schema() 生成符合 JSON Schema 标准的定义
    # 这就是发送给 OpenAI/DeepSeek API 的 "tools" 定义
    import json
    print(json.dumps(AI_Engineer.model_json_schema(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    demo_pydantic()
