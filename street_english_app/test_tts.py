import pyttsx3
import os

print("Initializing engine...")
engine = pyttsx3.init()
print("Engine initialized.")

text = "Hello, this is a test."
filename = "test_audio.mp3"

print(f"Saving to {filename}...")
try:
    engine.save_to_file(text, filename)
    print("Command queued.")
    engine.runAndWait()
    print("Execution finished.")

    if os.path.exists(filename):
        print(f"File created: {filename}, size: {os.path.getsize(filename)} bytes")
    else:
        print("File not found.")
except Exception as e:
    print(f"Error: {e}")
