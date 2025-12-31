import streamlit as st
import sys
import os
import tempfile
import whisper
from moviepy.editor import VideoFileClip
from openai import OpenAI
import time

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from localization import init_lang, get_text, lang_selector, render_sidebar

# Initialize
st.set_page_config(page_title="AI Video Translator", page_icon="🎬", layout="wide")
init_lang()
render_sidebar()
lang_selector()

lang = st.session_state.lang

st.title(get_text("Video_Subtitle", "title", lang))
st.info(get_text("Video_Subtitle", "description", lang))

# --- Helpers ---
def format_timestamp(seconds):
    """Convert seconds to VTT timestamp format (00:00:00.000)."""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"

def generate_vtt(segments):
    """Generate WebVTT content from segments."""
    vtt = "WEBVTT\n\n"
    for seg in segments:
        start = format_timestamp(seg['start'])
        end = format_timestamp(seg['end'])
        text = seg['text']
        trans = seg.get('translated_text', '')
        
        # Dual subtitle format
        content = f"{text}\n{trans}" if trans else text
        
        vtt += f"{start} --> {end}\n{content}\n\n"
    return vtt

def translate_text(text, client, model):
    """Translate text using LLM."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional subtitle translator. Translate the following English text to Chinese. Be concise. Only output the translation."},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error: {str(e)}]"

# --- Main Logic ---

# Check API Configuration
api_key = os.getenv("SILICONFLOW_API_KEY") or st.session_state.get("api_key")
base_url = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
model_name = "deepseek-ai/DeepSeek-V3" # Default

# Try to get from session state if Basic Chat was used
if "provider" in st.session_state and st.session_state.provider == "SiliconFlow (Cloud)":
    api_key = os.getenv("SILICONFLOW_API_KEY")
elif "provider" in st.session_state and st.session_state.provider == "Ollama (Local)":
    api_key = "ollama"
    base_url = "http://localhost:11434/v1"
    model_name = st.session_state.get("model_name", "qwen2.5:1.5b")

if not api_key:
    st.warning(get_text("Video_Subtitle", "error_no_model", lang))
    st.stop()

client = OpenAI(api_key=api_key, base_url=base_url)

# File Uploader
uploaded_file = st.file_uploader(get_text("Video_Subtitle", "upload_label", lang), type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save uploaded file to temp
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    video_path = tfile.name
    
    # Show video preview
    st.video(video_path)
    
    if st.button(get_text("Video_Subtitle", "process_btn", lang), type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Extract Audio
            status_text.text(get_text("Video_Subtitle", "processing_step1", lang))
            audio_path = video_path.replace(".mp4", ".wav")
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path, logger=None)
            progress_bar.progress(20)
            
            # Step 2: ASR (Whisper)
            status_text.text(get_text("Video_Subtitle", "model_loading", lang))
            # Load model (cached)
            @st.cache_resource
            def load_whisper():
                return whisper.load_model("base")
            
            model = load_whisper()
            
            status_text.text(get_text("Video_Subtitle", "processing_step2", lang))
            result = model.transcribe(audio_path)
            segments = result["segments"]
            progress_bar.progress(50)
            
            # Step 3: Translate
            status_text.text(get_text("Video_Subtitle", "processing_step3", lang))
            total_segs = len(segments)
            for i, seg in enumerate(segments):
                # Update progress
                status_text.text(get_text("Video_Subtitle", "processing_step3_progress", lang).format(i+1, total_segs))
                
                # Call LLM
                trans = translate_text(seg["text"], client, model_name)
                seg["translated_text"] = trans
                
                # Update bar
                current_progress = 50 + int((i / total_segs) * 40)
                progress_bar.progress(current_progress)
            
            # Step 4: Generate VTT
            vtt_content = generate_vtt(segments)
            progress_bar.progress(100)
            status_text.success(get_text("Video_Subtitle", "success", lang))
            
            # Display Result
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader("Result Video")
                # Reload video with subtitles
                st.video(video_path, subtitles=vtt_content)
            
            with col2:
                st.subheader("Subtitle File")
                st.download_button(
                    label=get_text("Video_Subtitle", "download_vtt", lang),
                    data=vtt_content,
                    file_name="subtitles.vtt",
                    mime="text/vtt"
                )
                
                with st.expander("View Raw VTT"):
                    st.text(vtt_content)

        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            # Cleanup
            if os.path.exists(audio_path):
                os.remove(audio_path)
