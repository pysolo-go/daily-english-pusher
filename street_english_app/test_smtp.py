import smtplib
import ssl
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/Users/solo/Desktop/work/trae.ai/ai/.env", override=True)

smtp_server = os.getenv("SMTP_SERVER")
port = int(os.getenv("SMTP_PORT", 465))
sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("SENDER_PASSWORD")

print(f"Server: {smtp_server}:{port}")
print(f"User: {sender_email}")
# print(f"Pass: {password}") # Don't print password

try:
    print(f"Connecting to {smtp_server}:{port}...")
    server = smtplib.SMTP_SSL(smtp_server, port)
    server.set_debuglevel(1)
    print("Connected!")
    server.login(sender_email, password)
    print("Logged in!")
    server.quit()
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
