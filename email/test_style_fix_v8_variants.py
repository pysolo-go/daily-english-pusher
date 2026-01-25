
import logging
import os
import time
from PIL import Image
from email_sender import send_email

# Configure logging
logging.basicConfig(level=logging.INFO)

def resize_image(input_path, output_path, width):
    """
    Resize image to specific width, maintaining aspect ratio.
    """
    try:
        with Image.open(input_path) as img:
            original_width, original_height = img.size
            ratio = width / original_width
            new_height = int(original_height * ratio)
            img = img.resize((width, new_height), Image.Resampling.LANCZOS)
            img.save(output_path)
            return True
    except Exception as e:
        print(f"Failed to resize image: {e}")
        return False

def send_style_fix_v8_variants():
    subject = "样式修复测试 V8: 对照组测试 (Variants)"
    
    # Ensure images directory exists
    if not os.path.exists("images"):
        os.makedirs("images")
        
    # Download a test image
    test_img_url = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
    original_img_path = "images/test_github_logo_original.png"
    img_100_path = "images/test_github_logo_100.png"
    img_300_path = "images/test_github_logo_300.png"
    
    # Ensure we have the image
    if not os.path.exists(original_img_path):
        try:
             os.system(f"curl -o {original_img_path} {test_img_url}")
        except Exception as e:
             print(f"Failed to download: {e}")

    # Create variants
    if os.path.exists(original_img_path):
        resize_image(original_img_path, img_100_path, width=100)
        resize_image(original_img_path, img_300_path, width=300)
    else:
        print("Original image not found.")
        return

    # Prepare Inline Images List
    inline_images_list = []
    
    # Variant 1: Physical 100px, No attributes
    inline_images_list.append({"path": img_100_path, "cid": "img_100_raw"})
    
    # Variant 2: Physical 300px, HTML width=100
    inline_images_list.append({"path": img_300_path, "cid": "img_300_html"})
    
    # Variant 3: Physical 300px, CSS width=100px
    inline_images_list.append({"path": img_300_path, "cid": "img_300_css"})

    email_body = ""
    email_body += f"<h1>推特监控汇总 (V8 对照组)</h1>"
    email_body += f"<p>检测时间: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>"
    email_body += "<p style='color: red; font-weight: bold;'>请观察以下三张图片的显示情况：</p>"
    email_body += "<hr>"
    
    # Section 1
    email_body += "<h3>1. 物理 100px (无任何样式)</h3>"
    email_body += "<p>这张图片原本只有 100px 宽，没有添加任何 width 属性。如果它显示很大，说明邮件客户端强制放大了它。</p>"
    email_body += "<div><img src='cid:img_100_raw'></div>"
    email_body += "<hr>"

    # Section 2
    email_body += "<h3>2. 物理 300px (HTML 属性限制 100)</h3>"
    email_body += "<p>这张图片原本 300px，使用了 width='100' 属性。</p>"
    email_body += "<div><img src='cid:img_300_html' width='100'></div>"
    email_body += "<hr>"

    # Section 3
    email_body += "<h3>3. 物理 300px (CSS 样式限制 100px)</h3>"
    email_body += "<p>这张图片原本 300px，使用了 style='width: 100px'。</p>"
    email_body += "<div><img src='cid:img_300_css' style='width: 100px;'></div>"
    email_body += "<hr>"
    
    email_body += "<p>如果三张图都是问号，请告诉我「全是问号」。</p>"
    email_body += "<p>如果某张图特别大，请告诉我「第X张很大」。</p>"

    # Send using FORCE QQ
    print(f"Sending email V8 variants via QQ...")
    success = send_email(subject, email_body, attachments=None, inline_images=inline_images_list, provider='qq')
    if success:
        print("Test email V8 (Variants) sent successfully!")
    else:
        print("Failed to send test email V8.")

if __name__ == "__main__":
    send_style_fix_v8_variants()
