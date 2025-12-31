import requests
import time

# 定义服务器地址 (默认 FastAPI 跑在 8000 端口)
BASE_URL = "http://127.0.0.1:8000"

def call_root():
    print("\n--- 1. 测试根目录 (GET /) ---")
    try:
        resp = requests.get(f"{BASE_URL}/")
        print(f"状态码: {resp.status_code}")
        print(f"结果: {resp.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败！请确保服务器已经启动 (uvicorn learn_fastapi_server:app --reload)")

def call_get_user():
    print("\n--- 2. 测试获取用户 (GET /users/{id}) ---")
    user_id = 888
    try:
        resp = requests.get(f"{BASE_URL}/users/{user_id}")
        print(f"结果: {resp.json()}")
    except Exception as e:
        print(f"出错: {e}")

def call_chat_ai():
    print("\n--- 3. 测试 AI 对话 (POST /chat) ---")
    payload = {
        "user_name": "Solo",
        "question": "FastAPI 难学吗？",
        "model": "deepseek-v2"
    }
    print(f"发送数据: {payload}")
    
    try:
        resp = requests.post(f"{BASE_URL}/chat", json=payload)
        if resp.status_code == 200:
            print("✅ 成功！服务器返回:")
            print(resp.json())
        else:
            print(f"❌ 失败: {resp.text}")
            
    except Exception as e:
        print(f"出错: {e}")

def call_error_case():
    print("\n--- 4. 测试错误数据 (验证 Pydantic 功能) ---")
    # 故意发一个缺少 'question' 字段的请求
    bad_payload = {
        "user_name": "Bad User"
    }
    try:
        resp = requests.post(f"{BASE_URL}/chat", json=bad_payload)
        print(f"状态码: {resp.status_code} (预期是 422 Unprocessable Entity)")
        print("错误详情:", resp.json())
    except Exception as e:
        print(f"出错: {e}")

if __name__ == "__main__":
    # 等待几秒让服务器启动 (如果是一起运行的话)
    time.sleep(1) 
    call_root()
    call_get_user()
    call_chat_ai()
    call_error_case()
