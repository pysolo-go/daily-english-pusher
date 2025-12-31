import subprocess
import os
import time

def test_audio_gen():
    text = "This is a test sentence."
    output_dir = "."
    base_name = f"test_audio"
    temp_path = os.path.join(output_dir, f"{base_name}.aiff")
    final_path = os.path.join(output_dir, f"{base_name}.mp3")
    
    print("Generating AIFF...")
    subprocess.run(["say", "-o", temp_path, text], check=True)
    
    print("Converting to MP3...")
    subprocess.run(["ffmpeg", "-y", "-i", temp_path, "-codec:a", "libmp3lame", "-qscale:a", "2", final_path], 
                   check=True)
    
    if os.path.exists(final_path):
        size = os.path.getsize(final_path)
        print(f"MP3 created. Size: {size} bytes")
    else:
        print("MP3 not found.")

    if os.path.exists(temp_path):
        os.remove(temp_path)

if __name__ == "__main__":
    test_audio_gen()