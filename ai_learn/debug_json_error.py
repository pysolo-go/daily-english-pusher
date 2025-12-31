import requests

url = "http://127.0.0.1:8000/chat"

print("--- 场景复现：JSON 语法错误 ---")

# 错误示范：这是一个“坏掉”的 JSON 字符串
# 常见原因 1：值写了一半
bad_json_string_1 = '{"user_name": "Solo", "question": }' 

# 常见原因 2：末尾多了逗号 (最常见！)
bad_json_string_2 = """
{
    "user_name": "Solo",
    "question": "可以吗？",
}
"""

# 常见原因 3：用了单引号 (JSON 必须用双引号)
bad_json_string_3 = "{'user_name': 'Solo'}"

print(f"正在发送损坏的数据: {bad_json_string_1}")

# 注意：这里我们要模拟发送原始字符串，所以用 data=...
# 正常开发我们用 json=...，库会自动帮我们处理好格式
response = requests.post(url, data=bad_json_string_1)

print(f"\n状态码: {response.status_code}")
print("错误详情:")
print(response.text)
