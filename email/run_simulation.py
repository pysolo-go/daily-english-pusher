import sys
import os
import logging
import requests
import time
from PIL import Image

# Ensure we can import from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from email_sender import send_email

# Configure logging
logging.basicConfig(level=logging.INFO)

def download_image(url, save_dir="images"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    filename = os.path.join(save_dir, "simulation_real_photo.jpg")
    
    try:
        logging.info(f"Downloading simulation image from {url}...")
        response = requests.get(url, stream=True, timeout=20)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            logging.info(f"Downloaded to {filename}")
            return filename
    except Exception as e:
        logging.error(f"Failed to download image {url}: {e}")
    return None

def resize_image_for_email(input_path, max_width=300):
    """
    Physically resize the image to a max width, saving over the original file.
    This ensures that even if email clients ignore CSS, the image is small.
    """
    try:
        with Image.open(input_path) as img:
            original_width, original_height = img.size
            if original_width > max_width:
                ratio = max_width / original_width
                new_height = int(original_height * ratio)
                # Resize using high-quality resampling
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                img.save(input_path) # Overwrite
                logging.info(f"Physically resized image {input_path} from {original_width} to {max_width}px")
                return True
            else:
                logging.info(f"Image {input_path} is already small enough ({original_width}px)")
                return True
    except Exception as e:
        logging.error(f"Failed to resize image {input_path}: {e}")
        return False

def run_simulation():
    logging.info("Starting simulation run with REAL photo...")
    
    # 1. Download a REAL high-res photo (Unsplash)
    # This is a large landscape photo (originally > 1000px wide)
    real_photo_url = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"
    local_path = download_image(real_photo_url)
    
    if not local_path:
        logging.error("Failed to download simulation image.")
        return

    # 2. Physically resize it (Simulating main.py logic)
    resize_image_for_email(local_path, max_width=300)
    
    # 3. Construct Email Body (Simulating main.py logic)
    subject = "推特监控仿真: 真实图片渲染测试 (Simulation)"
    
    email_body = ""
    email_body += f"<h1>推特监控仿真 (Simulation)</h1>"
    email_body += f"<p>检测时间: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>"
    email_body += "<p>由于 RSSHub 服务器当前不稳定，这是一封<b>仿真邮件</b>，使用了一张真实的风景照片来验证图片修复效果。</p>"
    email_body += "<hr>"
    
    inline_images_list = []
    
    # Simulate a tweet
    author = "SimulationBot"
    text = "这是一张原本很大的风景照片 (原始宽度 1000px)。如果修复成功，它应该被限制在 300px 宽，且清晰可见。"
    
    email_body += f"<div style='margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee;'>"
    email_body += f"<h2 style='margin-bottom: 10px; color: #1da1f2;'>{author}</h2>"
    email_body += f"<p style='font-size: 16px; line-height: 1.5;'>{text}</p>"
    
    cid = "img_sim_1"
    inline_images_list.append({
        "path": local_path,
        "cid": cid
    })
    
    # Triple Lock Sizing (Container + HTML + CSS)
    email_body += f"""
    <div style="max-width: 300px; margin-top: 5px;">
        <img src="cid:{cid}" width="300" style="width: 300px; max-width: 100%; height: auto; border-radius: 8px; display: block; border: 1px solid #eee;">
    </div><br>
    """
    
    email_body += f"<p><a href='#' style='color: #888; text-decoration: none;'>🔗 查看原推 (模拟)</a></p>"
    email_body += "</div>"
    
    # 4. Send Email via QQ
    logging.info("Sending simulation email via QQ...")
    success = send_email(subject, email_body, attachments=None, inline_images=inline_images_list, provider='qq')
    
    if success:
        logging.info("Simulation email sent successfully!")
    else:
        logging.error("Failed to send simulation email.")

if __name__ == "__main__":
    run_simulation()
