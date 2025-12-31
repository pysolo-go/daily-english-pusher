import sys
import os
from pathlib import Path

# Add parent directory to sys.path to access sibling modules
# Current: ai_learn/street_english_app/main.py
# Target: ai_learn/langchain_basics
current_dir = Path(__file__).resolve().parent
ai_learn_dir = current_dir.parent
sys.path.append(str(ai_learn_dir))

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Import LangChain tools
from langchain_basics.langchain_utils import init_langchain_env
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI
try:
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
    llm = None

# Models
class SearchQuery(BaseModel):
    query: str

class SearchResponse(BaseModel):
    answer: str

# API Endpoints
@app.post("/api/search", response_model=SearchResponse)
async def search_endpoint(request: SearchQuery):
    if not llm:
        raise HTTPException(status_code=503, detail="AI Service unavailable")
    
    try:
        # Define prompt for Street English context
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
        raise HTTPException(status_code=500, detail=str(e))

# Mount Static Files (Must be last to not override API)
app.mount("/", StaticFiles(directory=str(current_dir / "static"), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8085)
