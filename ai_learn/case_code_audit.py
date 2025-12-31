import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

def code_audit_bot():
    print("🐛 代码审计专家 (Bug Fixer)")
    print("-" * 30)
    
    # 模拟一段有 Bug 的代码
    buggy_code = """
    def calculate_average(numbers):
        total = 0
        for n in numbers:
            total += n
        return total / 0  # 这里有个除以零的错误
    """
    
    print(f"待审计代码:\n{buggy_code}")
    print("-" * 30)
    print("🔄 正在分析并修复...")

    try:
        stream = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {
                    "role": "system", 
                    "content": """
                    你是一位资深的 Python 架构师。
                    请分析用户提供的代码，找出 Bug，并给出修复后的代码。
                    
                    输出格式要求：
                    1. 先简述错误原因。
                    2. 然后使用 Markdown 代码块输出修复后的代码。
                    """
                },
                {"role": "user", "content": buggy_code}
            ],
            stream=True
        )
        
        print("\n🤖 AI 审计报告:\n")
        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print()

    except Exception as e:
        print(f"❌ 分析失败: {e}")

if __name__ == "__main__":
    code_audit_bot()
