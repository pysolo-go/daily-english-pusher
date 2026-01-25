
import logging
import os
import time
from PIL import Image
from email_sender import send_email

# Configure logging
logging.basicConfig(level=logging.INFO)

def resize_image(input_path, output_path, max_width=300):
    """
    Resize image to max_width, maintaining aspect ratio.
    """
    try:
        with Image.open(input_path) as img:
            original_width, original_height = img.size
            if original_width > max_width:
                ratio = max_width / original_width
                new_height = int(original_height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                print(f"Resized image from {original_width}x{original_height} to {max_width}x{new_height}")
            else:
                print(f"Image width {original_width} is smaller than {max_width}, skipping resize.")
            
            img.save(output_path)
            return True
    except Exception as e:
        print(f"Failed to resize image: {e}")
        return False

def send_style_fix_v7_qq_only():
    subject = "样式修复测试 V7: 物理压缩 + 强制QQ通道"
    
    # Ensure images directory exists
    if not os.path.exists("images"):
        os.makedirs("images")
        
    # Download a test image (Large one)
    test_img_url = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
    original_img_path = "images/test_github_logo_original.png"
    resized_img_path = "images/test_github_logo_300.png"
    
    # Ensure we have the image
    if not os.path.exists(original_img_path):
        try:
             print(f"Downloading test image from {test_img_url}...")
             os.system(f"curl -o {original_img_path} {test_img_url}")
        except Exception as e:
             print(f"Failed to download: {e}")

    # Perform Physical Resize (Reuse logic)
    if os.path.exists(original_img_path):
        resize_image(original_img_path, resized_img_path, max_width=300)
    else:
        print("Original image not found, cannot resize.")
        return

    # Mock Data using RESIZED LOCAL IMAGE
    tweets = [
        {
            "author": "System Test V7 (QQ Only)",
            "text": "This email was sent via QQ Mail (bypassing Resend). It uses physically resized images (300px) and CID embedding. If this works, the issue might be Resend-specific.",
            "images": [test_img_url], 
            "local_images": [resized_img_path], 
            "link": "https://twitter.com/test/status/v7"
        }
    ]
    
    email_body = ""
    email_body += f"<h1>推特监控汇总 (V7 QQ通道)</h1>"
    email_body += f"<p>检测时间: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>"
    email_body += "<hr>"
    
    inline_images_list = []
    image_counter = 0
    
    for i, tweet in enumerate(tweets):
        author = tweet["author"]
        email_body += f"<div style='margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee;'>"
        email_body += f"<h2 style='margin-bottom: 10px; color: #1da1f2;'>{author}</h2>"
        email_body += f"<p style='font-size: 16px; line-height: 1.5;'>{tweet['text']}</p>"
        
        # Images (Use local images as inline attachments via CID)
        if tweet.get("local_images"):
            for local_path in tweet["local_images"]:
                if os.path.exists(local_path):
                    image_counter += 1
                    cid = f"img_{image_counter}"
                    inline_images_list.append({
                        "path": local_path,
                        "cid": cid
                    })
                    
                    # Simple HTML: The image is already small physically.
                    # Add width="300" for good measure
                    email_body += f"""
                    <div style="margin-top: 10px;">
                        <img src="cid:{cid}" width="300" style="border-radius: 8px; border: 1px solid #eee;">
                    </div><br>
                    """
        
        email_body += f"<p><a href='{tweet['link']}' style='color: #888; text-decoration: none;'>🔗 查看原推</a></p>"
        email_body += "</div>"
    
    # Send using FORCE QQ
    print(f"Sending email with {len(inline_images_list)} inline images via QQ...")
    success = send_email(subject, email_body, attachments=None, inline_images=inline_images_list, provider='qq')
    if success:
        print("Test email V7 (QQ Only) sent successfully!")
    else:
        print("Failed to send test email V7.")

if __name__ == "__main__":
    send_style_fix_v7_qq_only()
