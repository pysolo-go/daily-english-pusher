import os
import json
import smtplib
import pandas as pd
import re
from email.utils import make_msgid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from dotenv import load_dotenv
from openai import OpenAI
try:
    import resend
except ImportError:
    resend = None

def send_email(subject, body_html):
    # Check if we should use Resend API
    resend_api_key = os.getenv("RESEND_API_KEY")
    if resend_api_key and resend:
        return send_email_via_resend(subject, body_html, resend_api_key)

    # Check for placeholder values or missing values
    if not all([SMTP_SERVER, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]) or "example.com" in SENDER_EMAIL:
        print("\n[Warning] Email configuration incomplete or using placeholders.")
        print("Please edit .env to set your real SENDER_EMAIL, SENDER_PASSWORD, etc.")
        print(f"Preview saved to: {DEBUG_PREVIEW_FILE}")
        return False

    msg = MIMEMultipart('alternative')
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = Header(subject, 'utf-8')

    msg.attach(MIMEText(body_html, 'html', 'utf-8'))

    try:
        print(f"Connecting to SMTP server: {SMTP_SERVER}:{SMTP_PORT}...")
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
        
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email via {SMTP_SERVER}:{SMTP_PORT}. Error: {e}")
        return False

def send_email_via_resend(subject, body_html, api_key):
    print("Sending email via Resend API...")
    resend.api_key = api_key
    
    sender = os.getenv("SENDER_EMAIL", "onboarding@resend.dev")
    receiver = os.getenv("RECEIVER_EMAIL")
    
    params = {
        "from": sender,
        "to": [receiver],
        "subject": subject,
        "html": body_html,
    }

    try:
        email = resend.Emails.send(params)
        print(f"Email sent successfully via Resend! ID: {email.get('id')}")
        return True
    except Exception as e:
        print(f"Failed to send email via Resend API. Error: {e}")
        return False



# Load environment variables
load_dotenv("/Users/solo/Desktop/work/trae.ai/ai/.env", override=True)

# Configuration
# Use relative paths for portability (GitHub Actions vs Local)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "vocabulary.csv")
PROGRESS_FILE = os.path.join(BASE_DIR, "email_progress.json")
DEBUG_PREVIEW_FILE = os.path.join(BASE_DIR, "latest_email_preview.html")
BATCH_SIZE = 20

# Email Config
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# OpenAI Config
# Try to determine a good model based on the base URL, or default to a safe bet
BASE_URL = os.getenv("OPENAI_BASE_URL", "")
if "siliconflow" in BASE_URL:
    MODEL_NAME = "deepseek-ai/DeepSeek-V2.5" # Common good model on SiliconFlow
elif "deepseek" in BASE_URL:
    MODEL_NAME = "deepseek-chat"
else:
    MODEL_NAME = "gpt-3.5-turbo"

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=BASE_URL
)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {"last_index": 0}

def save_progress(index):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({"last_index": index}, f)

def generate_batch_content(batch_data):
    """
    Batch generate sentences and translations for a list of words.
    batch_data: list of dicts [{'word': '...', 'meaning': '...'}, ...]
    """
    words_prompt = ""
    for item in batch_data:
        words_prompt += f"- {item['word']}: {item['meaning']}\n"

    prompt = f"""
    I will provide a list of English words with their meanings.
    For EACH word, please create a simple English sentence using that word, and provide a Chinese translation of that sentence.
    
    Return the result as a valid JSON list of objects. 
    The JSON should NOT be wrapped in markdown code blocks (no ```json).
    
    Input Words:
    {words_prompt}
    
    Output JSON Format:
    [
        {{"word": "the word", "sentence": "The English sentence.", "translation": "句子的中文翻译"}}
    ]
    """
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful English teacher. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"} if "gpt" in MODEL_NAME or "deepseek" in MODEL_NAME else None
        )
        content = response.choices[0].message.content.strip()
        
        # Clean up potential markdown wrappers if the model ignores instruction
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        # Handle case where result might be wrapped in a key like "words": [...]
        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                # Try to find the list
                for key in data:
                    if isinstance(data[key], list):
                        return data[key]
                return []
        except json.JSONDecodeError:
            print("Failed to decode JSON from LLM response.")
            print("Raw content:", content)
            return []
            
    except Exception as e:
        print(f"Error generating batch content: {e}")
        return []




def main():
    # Load Data
    df = pd.read_csv(CSV_PATH)
    
    # Get Progress
    progress = load_progress()
    start_idx = progress["last_index"]
    end_idx = start_idx + BATCH_SIZE
    
    # Check if we are done
    if start_idx >= len(df):
        print("All words have been processed!")
        return

    # Get Batch
    batch = df.iloc[start_idx:end_idx]
    
    # Prepare data for batch generation
    batch_input = []
    for i, row in batch.iterrows():
        batch_input.append({
            'word': row['word'],
            'meaning': row['meaning'],
            'pos': row['pos'],
            'index': i
        })
    
    print(f"Processing words {start_idx+1} to {min(end_idx, len(df))} using model {MODEL_NAME}...")
    
    # 1. Generate Text Content in Batch
    print("Generating sentences and translations (Batch)...")
    generated_results = generate_batch_content(batch_input)
    
    # Create a lookup dictionary for generated results (normalize keys to lowercase for matching)
    results_map = {}
    for item in generated_results:
        if 'word' in item:
            results_map[item['word'].lower()] = item
            
    # 2. Assemble Email Content
    print("Assembling email content...")
    email_content = []
    
    for i, row in batch.iterrows():
        word = row['word']
        meaning = row['meaning']
        pos = row['pos']
        
        # Retrieve generated data
        gen_data = results_map.get(word.lower(), {})
        sentence = gen_data.get('sentence', "Sentence generation failed.")
        translation = gen_data.get('translation', "Translation generation failed.")
        
        # Bold the word in the sentence
        if sentence:
            sentence_html = re.sub(f"({re.escape(word)})", r"<b>\1</b>", sentence, flags=re.IGNORECASE)
        else:
            sentence_html = ""

        item_html = f"""
        <div style="margin-bottom: 20px; font-family: sans-serif;">
            <div style="font-size: 18px; font-weight: bold; color: #2c3e50;">{i+1}. {word}</div>
            <div style="color: #7f8c8d; font-size: 14px; margin-bottom: 4px;">{pos} {meaning}</div>
            <div style="font-size: 16px; margin-bottom: 4px;">{sentence_html}</div>
            <div style="color: #95a5a6; font-size: 14px;">{translation}</div>
        </div>
        <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
        """
        email_content.append(item_html)

    # Final Email Body
    full_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">Daily Vocabulary ({start_idx+1}-{min(end_idx, len(df))})</h2>
        {''.join(email_content)}
        <p style="font-size: 12px; color: #999; margin-top: 30px; text-align: center;">
            Generated by Trae AI Street English App<br>
        </p>
    </body>
    </html>
    """
    
    # Save preview for debugging/user verification
    with open(DEBUG_PREVIEW_FILE, "w") as f:
        f.write(full_body)
    
    # Send Email
    subject = f"Daily Vocabulary: Words {start_idx+1}-{min(end_idx, len(df))}"
    if send_email(subject, full_body):
        # Update Progress only if sent successfully
        save_progress(end_idx)
    else:
        print("Email sending skipped or failed. Progress NOT updated.")
        print(f"You can view the generated content in: {DEBUG_PREVIEW_FILE}")

if __name__ == "__main__":
    main()
