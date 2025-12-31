import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

# 核心：定义输出格式 (JSON Schema)
# 这是一个"简历提取器"，我们希望 AI 把乱七八糟的文本整理成标准格式
SCHEMA = {
    "type": "json_object",
    "schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "候选人姓名"},
            "email": {"type": "string", "description": "邮箱地址"},
            "skills": {
                "type": "array", 
                "items": {"type": "string"},
                "description": "技能列表，如 Python, Java"
            },
            "years_of_experience": {"type": "integer", "description": "工作年限"}
        },
        "required": ["name", "skills", "years_of_experience"]
    }
}

def extract_resume():
    print("📄 简历结构化提取器 (JSON Mode)")
    print("-" * 30)
    
    # 模拟一段非结构化的简历文本
    raw_text = """
    我是张三，有5年 Python 开发经验。
    之前在字节跳动工作，擅长 Django 和 FastAPI。
    可以通过 zhangsan@example.com 联系我。
    平时喜欢打篮球。
    """
    
    print(f"原始文本:\n{raw_text}")
    print("-" * 30)
    print("🔄 正在提取关键信息...")

    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {
                    "role": "system", 
                    "content": "你是一个数据提取助手。请从用户输入中提取简历信息，并以 JSON 格式返回。"
                },
                {"role": "user", "content": raw_text}
            ],
            # 关键点：告诉模型返回 JSON
            response_format={"type": "json_object"}, 
            temperature=0.1 # 越低越准
        )
        
        json_str = response.choices[0].message.content
        
        # 解析 JSON
        data = json.loads(json_str)
        
        print("\n✅ 提取结果 (Python Dict):")
        print(f"姓名: {data.get('name')}")
        print(f"年限: {data.get('years_of_experience')} 年")
        print(f"技能: {', '.join(data.get('skills', []))}")
        print(f"邮箱: {data.get('email')}")
        
    except Exception as e:
        print(f"❌ 提取失败: {e}")

if __name__ == "__main__":
    extract_resume()
