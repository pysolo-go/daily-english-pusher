from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import whisper
import os
import tempfile
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import shutil
import collections
from pydub import AudioSegment

# Load env
root_dir = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(root_dir / ".env")

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Whisper Model (Global)
print("Loading Whisper model...")
try:
    # 'base' or 'small' is recommended for real-time on CPU
    model = whisper.load_model("base")
    print("Whisper model loaded.")
except Exception as e:
    print(f"Failed to load Whisper model: {e}")
    model = None

# LLM Config
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
BASE_URL = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
MODEL_NAME = "deepseek-ai/DeepSeek-V3"

if SILICONFLOW_API_KEY:
    client = OpenAI(api_key=SILICONFLOW_API_KEY, base_url=BASE_URL)
    print(f"Using SiliconFlow: {MODEL_NAME}")
else:
    client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
    MODEL_NAME = "qwen2.5:1.5b"
    print(f"Using Ollama (Local): {MODEL_NAME}")

# --- Rolling Buffer Logic ---
# Store last N seconds of audio to provide context
MAX_BUFFER_MS = 6000 # Keep last 6 seconds
audio_buffer = AudioSegment.empty()

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    global audio_buffer
    
    if not model:
         return {"error": "Whisper model not loaded"}

    try:
        # 1. Read uploaded chunk (WebM)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_chunk:
            shutil.copyfileobj(file.file, temp_chunk)
            temp_chunk_path = temp_chunk.name
        
        # 2. Convert chunk to PyDub AudioSegment and Append to Buffer
        try:
            # Note: Requires ffmpeg installed
            new_segment = AudioSegment.from_file(temp_chunk_path, format="webm")
            audio_buffer += new_segment
            
            # Trim buffer to keep only recent context
            if len(audio_buffer) > MAX_BUFFER_MS:
                audio_buffer = audio_buffer[-MAX_BUFFER_MS:]
                
        except Exception as audio_err:
            print(f"Audio processing error: {audio_err}")
            # Fallback: Just use the chunk if conversion fails
            pass
        finally:
            if os.path.exists(temp_chunk_path):
                os.remove(temp_chunk_path)

        # 3. Export buffer to temp file for Whisper
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_buffer_file:
            # Export as WAV (Whisper likes WAV/MP3)
            audio_buffer.export(temp_buffer_file.name, format="wav")
            temp_buffer_path = temp_buffer_file.name

        # 4. Transcribe the BUFFERED audio
        # fp16=False for CPU compatibility
        result = model.transcribe(
            temp_buffer_path, 
            fp16=False, 
            language="en",
            no_speech_threshold=0.6, # Filter silence
            logprob_threshold=-1.0
        )
        original_text = result["text"].strip()
        
        # Clean up
        if os.path.exists(temp_buffer_path):
            os.remove(temp_buffer_path)
        
        if not original_text or len(original_text) < 2:
            return {"original": "...", "translated": "..."}

        # 5. Translate with LLM
        # Optimize prompt for partial sentence translation
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a real-time subtitle translator. Translate the English text to Chinese. The input is a continuous audio stream segment. Output ONLY the translation. Keep it concise."},
                    {"role": "user", "content": original_text}
                ],
                temperature=0.3,
                max_tokens=60
            )
            translated_text = response.choices[0].message.content.strip()
        except Exception as llm_error:
            print(f"LLM Error: {llm_error}")
            translated_text = "..."

        return {
            "original": original_text,
            "translated": translated_text
        }

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
