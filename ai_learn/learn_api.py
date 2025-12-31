import requests
import json

# ==========================================
# 什么是 API？(Application Programming Interface)
# ==========================================
# 想象你去餐厅吃饭：
# 1. 你 (客户端/Client)：想吃红烧肉。
# 2. 服务员 (API)：拿着菜单，记下你的菜名，传给后厨。
# 3. 后厨 (服务器/Server)：做好菜。
# 4. 服务员 (API)：把菜端给你。
#
# 你不需要知道后厨怎么切肉、怎么炒菜，你只需要通过“服务员”这个接口点菜即可。
# 在编程中，API 就是那个“服务员”。

def demo_get_request():
    """
    演示 1: GET 请求 (向服务器“拿”数据)
    场景：查看用户信息、获取天气、下载网页
    """
    print("\n--- 1. GET 请求演示 (查菜单) ---")
    
    # 这是一个免费的测试 API，专门用来模拟数据
    url = "https://jsonplaceholder.typicode.com/users/1"
    
    print(f"正在呼叫服务员 (请求 URL): {url}")
    
    # 发送请求
    response = requests.get(url)
    
    # 检查状态码 (200 表示成功，404 表示找不到，500 表示后厨炸了)
    print(f"服务员回应代码 (Status Code): {response.status_code}")
    
    if response.status_code == 200:
        # 解析返回的 JSON 数据
        data = response.json()
        print("拿到数据了 (Response Body):")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print(f"用户姓名: {data['name']}")
        print(f"用户邮箱: {data['email']}")
    else:
        print("请求失败")

def demo_post_request():
    """
    演示 2: POST 请求 (向服务器“提交”数据)
    场景：注册账号、提交表单、发送聊天消息给 AI
    """
    print("\n--- 2. POST 请求演示 (写订单) ---")
    
    url = "https://jsonplaceholder.typicode.com/posts"
    
    # 我们要发给服务器的数据 (Payload)
    my_data = {
        "title": "学习 AI API",
        "body": "API 其实很简单，就是发数据和收数据。",
        "userId": 1
    }
    
    print(f"正在提交数据: {my_data}")
    
    # 发送 POST 请求
    response = requests.post(url, json=my_data)
    
    print(f"状态码: {response.status_code} (201 通常表示创建成功)")
    print("服务器返回结果:", response.json())

def demo_ai_api_concept():
    """
    演示 3: AI API 是怎么回事？
    """
    print("\n--- 3. AI API 原理揭秘 ---")
    print("当你调用 ChatGPT 或 DeepSeek 时，本质上也是发了一个 HTTP 请求。")
    
    # 伪代码演示 (因为我们没有真实的 API Key，所以这里展示逻辑)
    fake_code = """
    import requests

    url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",  # 你的身份证
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": "你好，API 是什么？"}
        ]
    }
    
    # 这就是 AI 调用的本质：一个 POST 请求
    response = requests.post(url, headers=headers, json=data)
    print(response.json()['choices'][0]['message']['content'])
    """
    print(fake_code)
    print("👉 现在的 SDK (如 openai 库) 只是把上面这段代码封装好了，让你写起来更简单。")

if __name__ == "__main__":
    demo_get_request()
    demo_post_request()
    demo_ai_api_concept()
