import requests
import json

# 你的 API 地址
url = "http://127.0.0.1:8000/chat"

# 场景：故意犯错
# 我们的 API 要求必须有 "user_name" 和 "question"
# 这里我们故意只传 "user_name"，漏掉了 "question"
bad_data = {
    "user_name": "粗心的用户"
    # "question": "我忘了填问题"  <-- 缺失这个必填字段
}

print(f"正在发送错误数据: {bad_data}")
response = requests.post(url, json=bad_data)

print(f"\n--- 服务器回应 ---")
print(f"状态码: {response.status_code} (Unprocessable Entity)")

if response.status_code == 422:
    print("意思就是：'你的数据格式我看懂了(JSON是对的)，但里面的内容缺胳膊少腿，我没法处理'")
    
    print("\n--- 详细错误报告 (Pydantic 自动生成的) ---")
    error_detail = response.json()
    print(json.dumps(error_detail, indent=2, ensure_ascii=False))
    
    # 让我们以此来教用户怎么看错误
    first_error = error_detail['detail'][0]
    print("\n--- 错误解读 ---")
    print(f"哪里错了 (loc): {first_error['loc']}")
    print(f"什么错误 (msg): {first_error['msg']}")
    print(f"错误类型 (type): {first_error['type']}")
