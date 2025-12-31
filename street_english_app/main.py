import sys
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

# Add ai_learn to sys.path
current_dir = Path(__file__).resolve().parent
ai_learn_path = current_dir.parent / "ai_learn"
sys.path.append(str(ai_learn_path))

# Initialize AI
llm = None
try:
    from langchain_basics.langchain_utils import init_langchain_env
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    api_key, base_url = init_langchain_env()
    llm = ChatOpenAI(
        model="Qwen/Qwen2.5-7B-Instruct", 
        openai_api_key=api_key,
        openai_api_base=base_url,
        temperature=0.7
    )
    print("AI Model initialized successfully.")
except Exception as e:
    print(f"Failed to initialize AI: {e}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchQuery(BaseModel):
    query: str

class SearchResponse(BaseModel):
    answer: str

@app.post("/api/search", response_model=SearchResponse)
async def search_endpoint(request: SearchQuery):
    if not llm:
        return SearchResponse(answer=f"AI 暂时不可用 (Mock): 您询问了 '{request.query}'。由于未配置 API Key 或依赖缺失，这是自动回复。")
    
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful 'Street English' tutor. "
                       "The user is looking at a webpage with street signs, tags, and shop names. "
                       "Answer their questions about English slang, street terminology, or translate phrases. "
                       "Keep answers concise, fun, and educational. "
                       "IMPORTANT: Always answer the user's questions in Chinese (中文). "
                       "Even if the user asks in English, explain the answer in Chinese."),
            ("user", "{text}")
        ])
        chain = prompt | llm | StrOutputParser()
        response_text = chain.invoke({"text": request.query})
        return SearchResponse(answer=response_text)
    except Exception as e:
        print(f"Error during AI generation: {e}")
        return SearchResponse(answer="抱歉，AI 遇到了一些问题，请稍后再试。")

@app.get("/")
async def read_index():
    return FileResponse('index.html')

app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
