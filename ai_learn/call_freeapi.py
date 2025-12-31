import requests
import json

# 1. 设置基础 URL
# 这是 FreeAPI 的官方公开测试地址
BASE_URL = "https://api.freeapi.app/api/v1"

def get_random_joke():
    """
    演示 1: 获取一条随机笑话 (不需要登录)
    """
    print("\n--- 1. 获取随机笑话 ---")
    endpoint = "/public/randomjokes/joke/random"
    url = BASE_URL + endpoint
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # FreeAPI 的数据通常包裹在 'data' 字段里
            joke_content = data['data']['content']
            print(f"😂 笑话来了: {joke_content}")
        else:
            print(f"获取失败: {response.status_code}")
    except Exception as e:
        print(f"出错了: {e}")

def get_random_user():
    """
    演示 2: 获取一个随机用户信息 (模拟数据)
    """
    print("\n--- 2. 获取随机用户 ---")
    endpoint = "/public/randomusers/user/random"
    url = BASE_URL + endpoint
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            user = data['data']
            name = f"{user['name']['first']} {user['name']['last']}"
            city = user['location']['city']
            print(f"👤 找到用户: {name}")
            print(f"📍 来自: {city}")
        else:
            print(f"获取失败: {response.status_code}")
    except Exception as e:
        print(f"出错了: {e}")

def get_random_product():
    """
    演示 3: 获取电商商品 (不需要登录)
    """
    print("\n--- 3. 逛逛电商商品 ---")
    endpoint = "/public/randomproducts/product/random"
    url = BASE_URL + endpoint
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            product = data['data']
            print(f"📦 商品: {product['title']}")
            print(f"💰 价格: ${product['price']}")
            print(f"📝 描述: {product['description'][:50]}...") # 只显示前50个字
        else:
            print(f"获取失败: {response.status_code}")
    except Exception as e:
        print(f"出错了: {e}")

if __name__ == "__main__":
    print(f"正在连接 FreeAPI ({BASE_URL})...")
    get_random_joke()
    get_random_user()
    get_random_product()
