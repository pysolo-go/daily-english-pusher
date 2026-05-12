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
import eng_to_ipa as ipa
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
    # Use formataddr to set a display name while keeping the email address
    from email.utils import formataddr
    msg['From'] = formataddr(("Street English App", SENDER_EMAIL))
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
    
    # Force the onboarding sender as per user request to restore original look
    sender = "onboarding@resend.dev" 
    receiver = os.getenv("RECEIVER_EMAIL")
    
    # Add a personal name to the sender
    sender_with_name = f"IELTS <{sender}>"

    params = {
        "from": sender_with_name,
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
# Try to load from project root .env if it exists (for local development)
# In GitHub Actions, variables are injected directly via env context, so .env is not needed.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path, override=True)

# Configuration
# Use relative paths for portability (GitHub Actions vs Local)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "vocabulary.csv")
PROGRESS_FILE = os.path.join(BASE_DIR, "email_progress.json")
DEBUG_PREVIEW_FILE = os.path.join(BASE_DIR, "latest_email_preview.html")
BATCH_SIZE = 30  # Changed to 30 as requested

# Email Config
SMTP_SERVER = os.getenv("SMTP_SERVER", "")
smtp_port_str = os.getenv("SMTP_PORT")
if smtp_port_str and smtp_port_str.strip():
    SMTP_PORT = int(smtp_port_str)
else:
    SMTP_PORT = 465 # Default
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# OpenAI Config
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {"last_index": 0}

def save_progress(index):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({"last_index": index}, f)

def generate_phrases(words_list):
    if not API_KEY:
        print("Warning: OPENAI_API_KEY not found. Skipping phrase generation.")
        return []

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    prompt = f"""
    I have a list of {len(words_list)} English words. 
    I need you to generate EXACTLY 10 short, natural English phrases or sentences.
    Together, these 10 phrases MUST include as many of the provided words as possible. 
    Each phrase should be followed by its Chinese translation.
    
    Words: {', '.join(words_list)}
    
    Please output a valid JSON object containing a single key "phrases".
    The value of "phrases" must be an array of 10 objects.
    Each object must have:
    - "english": The English phrase/sentence
    - "chinese": The Chinese translation
    
    Output ONLY the JSON object, nothing else. No markdown formatting.
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {"role": "system", "content": "You are a helpful English teacher."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        print("Raw OpenAI response:", content)
        
        import re
        # Try to fix `{ { ... } }` invalid JSON to `[ { ... } ]`
        content = content.strip()
        if content.startswith('{{') and content.endswith('}}'):
            content = '[' + content[1:-1] + ']'
        elif content.startswith('{') and content.endswith('}') and 'english' in content and 'chinese' in content:
            # Check if it's `{ "english": ..., "chinese": ... }` -> `[{...}]`
            # Or if it's `{ {...}, {...} }`
            if re.search(r'\{\s*\{', content):
                content = '[' + content[1:-1] + ']'

        # Extract JSON array using regex
        import re
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if match:
            content = match.group(0)
            
        data = json.loads(content)
        if isinstance(data, dict):
            for key in data:
                if isinstance(data[key], list):
                    return data[key]
            return []
        return data

    except Exception as e:
        print(f"Error generating phrases: {e}")
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
    
    # Assemble Email Content
    print("Assembling email content...")
    email_content = []
    
    words_for_phrases = []

    for i, row in batch.iterrows():
        word = row['word']
        words_for_phrases.append(word)
        meaning = row['meaning']
        pos = row['pos']
        sentence = row.get('sentence', '')
        if pd.isna(sentence):
            sentence = ""
        
        sentence_meaning = row.get('sentence_meaning', '')
        if pd.isna(sentence_meaning):
            sentence_meaning = ""
        
        # Generate phonetic transcription
        try:
            phonetic = ipa.convert(word)
        except:
            phonetic = ""
        
        phonetic_html = f'<span style="font-weight: normal; font-size: 14px; color: #7f8c8d; margin-left: 8px;">/{phonetic}/</span>' if phonetic else ""

        item_html = f"""
        <div style="margin-bottom: 20px; font-family: sans-serif;">
            <div style="font-size: 18px; font-weight: bold; color: #2c3e50;">{i+1}. {word}{phonetic_html}</div>
            <div style="color: #7f8c8d; font-size: 14px; margin-bottom: 4px;">{pos} {meaning}</div>
            <div style="color: #34495e; font-size: 15px; margin-top: 6px; font-style: italic;">{sentence}</div>
            <div style="color: #95a5a6; font-size: 14px; margin-top: 2px;">{sentence_meaning}</div>
        </div>
        <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
        """
        email_content.append(item_html)

    # Generate 10 phrases
    print("Generating phrases...")
    phrases = generate_phrases(words_for_phrases)
    phrases_html = ""
    if phrases:
        phrases_html = """
        <div style="margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 8px; font-family: sans-serif;">
            <h3 style="color: #2c3e50; margin-top: 0; border-bottom: 1px solid #ddd; padding-bottom: 10px;">Context Phrases</h3>
            <ul style="padding-left: 20px; color: #34495e; font-size: 15px; line-height: 1.8;">
        """
        for p in phrases:
            eng = p.get('english', '')
            chi = p.get('chinese', '')
            phrases_html += f'<li style="margin-bottom: 10px;"><strong>{eng}</strong><br><span style="color: #7f8c8d; font-size: 14px;">{chi}</span></li>'
        phrases_html += "</ul></div>"

    # Final Email Body
    full_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">IELTS Daily Vocabulary ({start_idx+1}-{min(end_idx, len(df))})</h2>
        {''.join(email_content)}
        {phrases_html}
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
    subject = f"IELTS Daily Vocabulary: Words {start_idx+1}-{min(end_idx, len(df))}"
    if send_email(subject, full_body):
        # Update Progress only if sent successfully
        save_progress(end_idx)
    else:
        print("Email sending skipped or failed. Progress NOT updated.")
        print(f"You can view the generated content in: {DEBUG_PREVIEW_FILE}")
        # Exit with error code so GitHub Actions knows it failed
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()
