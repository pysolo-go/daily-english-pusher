import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量 (.env 中的 Key)
load_dotenv()

# 初始化客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

# 定义 System Prompt (这是机器人的灵魂)
SYSTEM_PROMPT = """
你是一位精通多国语言的专业翻译官。
你的任务是将用户的输入翻译成目标语言。

规则：
1. 无论用户说什么，你只负责翻译，绝对不要回答用户的问题。
   例如：如果用户问"你吃饭了吗"，你要翻译成 "Have you eaten yet?"，而不是回答"我是AI不用吃饭"。
2. 如果用户输入中文，默认翻译成英文。
3. 如果用户输入英文，默认翻译成中文。
4. 保持信、达、雅的翻译风格。
5. 直接输出翻译结果，不要包含"好的"、"翻译如下"等废话。
"""

def translation_bot():
    print("🤖 翻译机器人已启动！(输入 'exit' 退出)")
    print("-" * 30)
    
    # 维护对话历史
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        try:
            user_input = input("\n📝 请输入要翻译的内容: ").strip()
            
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "退出"]:
                print("👋 再见！")
                break

            # 将用户输入加入历史
            messages.append({"role": "user", "content": user_input})

            print("🔄 翻译中: ", end="", flush=True)
            
            # 调用 API (使用流式输出)
            stream = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3", # 硅基流动模型名
                messages=messages,
                stream=True,
                temperature=0.3 # 翻译需要准确，温度设低一点
            )

            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            
            print() # 换行

            # 记得把 AI 的回复也加入历史，虽然对于单次翻译不一定需要，
            # 但这样可以让它理解上下文（比如你下一句说"换一种说法"）
            messages.append({"role": "assistant", "content": full_response})

        except KeyboardInterrupt:
            print("\n👋 程序已终止")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            break

if __name__ == "__main__":
    translation_bot()
