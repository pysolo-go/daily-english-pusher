import os
import time
from dotenv import load_dotenv
from openai import OpenAI

# 1. 加载环境变量
# 这行代码会自动寻找当前目录下的 .env 文件，并加载里面的变量
# 如果找不到 .env，它会什么都不做（所以记得创建 .env！）
load_dotenv()

# 2. 初始化客户端
# OpenAI SDK 是目前行业的“通用标准”。
# 无论是 OpenAI, DeepSeek, Moonshot (Kimi), 还是本地的 Ollama/vLLM，
# 只要支持 "OpenAI Compatible" 协议，都可以用这个 SDK 调用。
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

if not api_key:
    print("⚠️ 警告: 未检测到 OPENAI_API_KEY 环境变量。")
    print("请复制 .env.example 为 .env 并填入你的 Key。")
    # 为了演示不报错，我们给个假的，实际调用会失败
    api_key = "sk-demo-key"

client = OpenAI(
    api_key=api_key,
    base_url=base_url  # 如果不填，默认是 https://api.openai.com/v1
)

def demo_simple_chat():
    """
    演示 1: 最基础的对话 (一次性等待结果)
    """
    print("\n--- 1. 简单对话 (非流式) ---")
    print("正在思考中 (等待完整回复)...")
    
    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",  # 硅基流动的模型名称通常是 组织/模型名
            messages=[
                {"role": "system", "content": "你是一个幽默的脱口秀演员。"},
                {"role": "user", "content": "讲个关于程序员的笑话。"}
            ]
        )
        # 获取完整内容
        content = response.choices[0].message.content
        print(f"🤖 AI: {content}")
        
    except Exception as e:
        print(f"❌ 调用失败 (可能是 Key 无效): {e}")

def demo_stream_chat():
    """
    演示 2: 流式输出 (Streaming)
    这是提升用户体验的关键！不用等 AI 写完几百字才显示，而是写一个字显示一个字。
    """
    print("\n--- 2. 流式对话 (Streaming) ---")
    print("🤖 AI: ", end="", flush=True)
    
    try:
        stream = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {"role": "user", "content": "请用 50 个字解释什么是 API。"}
            ],
            stream=True  # <--- 关键参数
        )
        
        # 逐块接收数据
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                time.sleep(0.05)  # 模拟打字机效果 (实际不需要 sleep)
        print() # 换行
        
    except Exception as e:
        print(f"\n❌ 流式调用失败: {e}")

def demo_chat_with_history():
    """
    演示 3: 带记忆的对话 (Session Management)
    API 本身是“无状态”的 (Stateless)，它记不住你上一句说了什么。
    如果要实现连续对话，我们需要自己维护一个 messages 列表，
    每次把之前的对话历史都发给它。
    """
    print("\n--- 3. 带记忆的连续对话 (输入 'exit' 退出) ---")
    
    # 初始化对话历史 (通常包含 System Prompt)
    messages = [
        {"role": "system", "content": "你是一个有用的 AI 助手。"}
    ]
    
    while True:
        user_input = input("\n👤 你: ")
        if user_input.lower() in ["exit", "quit", "退出"]:
            break
            
        # 1. 把用户的话加入历史
        messages.append({"role": "user", "content": user_input})
        
        try:
            print("🤖 AI: ", end="", flush=True)
            full_response = ""
            
            # 2. 把整个历史发给 API
            stream = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3",
                messages=messages, # <--- 重点：发送完整历史
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            
            # 3. 把 AI 的回答也加入历史 (这样下一轮它就知道了)
            messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            print(f"\n❌ 出错: {e}")
            break

if __name__ == "__main__":
    # 提示：如果没有真实 Key，运行这些会报错。
    # 这是正常的，重点是理解代码逻辑。
    print(">>> 开始演示 LLM API 调用 <<<")
    print(f"当前配置 Base URL: {client.base_url}")
    
    # 只要 Key 是无效的，这里肯定会报错，我们捕获一下不让程序崩掉
    # 建议去 .env 填入真实的 Key (比如 DeepSeek 的) 来体验
    demo_simple_chat()
    demo_stream_chat()
    demo_chat_with_history()
