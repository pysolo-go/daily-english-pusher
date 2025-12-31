import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

def summary_bot():
    print("📑 长文总结助手 (Summarizer)")
    print("-" * 30)
    
    # 模拟一篇长文章 (比如新闻、报告)
    long_text = """
    北京时间2023年10月... (省略1000字)...
    SpaceX 星舰发射成功，标志着人类移民火星迈出了重要一步。
    本次发射测试了33台猛禽发动机的同步点火能力。
    尽管助推器在分离后发生爆炸，但飞船成功进入了预定轨道。
    马斯克表示，这是一次巨大的成功，为下一次测试收集了宝贵数据。
    NASA 局长也发推文表示祝贺。
    ...
    """
    
    print("🔄 正在阅读长文并总结...")

    try:
        stream = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {
                    "role": "system", 
                    "content": """
                    请将用户输入的文章总结为 3 个要点。
                    要求：
                    1. 语言自然流畅，符合中文口语习惯。
                    2. 使用完整的句子结构，不要省略主谓宾。
                    3. 拒绝生硬的翻译腔和机器压缩感。
                    4. 每个要点控制在 25 个字以内。
                    """
                },
                {"role": "user", "content": long_text}
            ],
            stream=True
        )
        
        print("\n🤖 总结结果:\n")
        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print()

    except Exception as e:
        print(f"❌ 总结失败: {e}")

if __name__ == "__main__":
    summary_bot()
