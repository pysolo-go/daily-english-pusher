from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# 1. 初始化应用
# 这就像你雇了一个“服务员总管”，他负责接单
app = FastAPI()

# 2. 定义数据模型 (用我们刚学的 Pydantic)
# 这是“菜单”，告诉顾客点菜的格式
class AI_Request(BaseModel):
    user_name: str
    question: str
    model: Optional[str] = "gpt-3.5"

class AI_Response(BaseModel):
    answer: str
    tokens_used: int

# 3. 定义 API 接口 (路由)

@app.get("/")
async def root():
    """
    最简单的 GET 接口
    访问 http://localhost:8000/ 就会触发这个函数
    """
    return {"message": "欢迎来到我的 AI API 服务站！"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """
    带参数的 GET 接口
    访问 http://localhost:8000/users/123
    FastAPI 会自动把 "123" 变成整数传给 user_id
    """
    return {"user_id": user_id, "role": "VIP 客户"}

@app.post("/chat", response_model=AI_Response)
async def chat_with_ai(request: AI_Request):
    """
    POST 接口：模拟 AI 对话
    FastAPI 会自动：
    1. 读取请求体 JSON
    2. 验证是否符合 AI_Request 格式 (Pydantic 立功了！)
    3. 如果格式不对，自动返回 422 错误
    """
    print(f"收到来自 {request.user_name} 的提问: {request.question}")
    
    # 模拟 AI 处理逻辑
    fake_answer = f"AI ({request.model}) 听到了你的问题：'{request.question}'。但我只是个模拟程序，所以我只能复读机。"
    
    return AI_Response(answer=fake_answer, tokens_used=15)

# 怎么运行？
# 在终端输入: uvicorn learn_fastapi_server:app --reload
