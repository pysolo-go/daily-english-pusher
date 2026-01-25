import config
from email_sender import send_email
from twitter_monitor import check_for_new_tweets
import os
import logging
import html

# Configure logging to show INFO logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test():
    print("--- 开始集成测试 ---")
    
    # 1. 检查配置
    # 简单的检查，看是否包含默认值或者为空
    if not config.QQ_EMAIL or "your_qq_email" in config.QQ_EMAIL:
        print("❌ 错误: .env 文件尚未配置。请修改 QQ_EMAIL 和 QQ_EMAIL_PASSWORD。")
        return

    # 2. 测试推特抓取
    print("\n[1/2] 正在尝试从 Nitter 抓取最新推文...")
    
    # Select the first user for testing (Trump)
    test_user = config.TWITTER_USERS[0]
    print(f"Testing user: {test_user}")
    
    try:
        # 为了测试，我们临时删除 tweet_monitor_state.json 以便模拟第一次运行
        # 或者我们只删除该用户的记录
        state_file = "tweet_monitor_state.json"
        if os.path.exists(state_file):
            import json
            try:
                with open(state_file, "r") as f:
                    data = json.load(f)
                if test_user in data:
                    del data[test_user]
                    with open(state_file, "w") as f:
                        json.dump(data, f)
            except:
                pass
            
        tweets = check_for_new_tweets(test_user)
        
        if tweets:
            latest_tweet = tweets[0]
            print(f"✅ 抓取成功！")
            print(f"   ID: {latest_tweet['id']}")
            print(f"   内容 (完整): {latest_tweet['text']}")
            print(f"   链接: {latest_tweet['link']}")
            print(f"   图片数: {len(latest_tweet.get('images', []))}")
            if latest_tweet.get('images'):
                print(f"   图片列表: {latest_tweet['images']}")
        else:
            print("⚠️ 警告: 未抓取到推文。可能是 Nitter 实例暂时不可用或网络问题。")
            latest_tweet = None
    except Exception as e:
        print(f"❌ 抓取出错: {e}")
        latest_tweet = None

    # 3. 测试邮件发送
    print("\n[2/2] 正在尝试发送测试邮件...")
    
    # Use a single HTML string for the body to avoid list rendering issues in yagmail
    email_html = ""
    # Collect local image paths for inline/attachment
    attachments = []
    
    if latest_tweet:
        author = latest_tweet.get('author', test_user)
        subject = f"Trae AI 工作流测试 - 成功抓取 ({author})"
        email_html += "<h1>测试成功：成功抓取到推文</h1>"
        email_html += f"<h2>来自: {author}</h2>"
        email_html += "<h3>推文内容：</h3>"
        
        # Ensure text is properly encoded/decoded if necessary, but yagmail handles utf-8
        # ESCAPE HTML CHARACTERS to prevent rendering issues
        text_content = html.escape(latest_tweet['text'])
        # Replace newlines with <br> for better formatting
        text_content = text_content.replace("\n", "<br>")
        
        email_html += f"<p style='font-size: 16px; line-height: 1.5;'>{text_content}</p>"
        
        link = latest_tweet['link']
        email_html += f"<p><a href='{link}' style='color: #1a0dab;'>查看原推链接</a></p>"
        
        if latest_tweet.get('images'):
            email_html += f"<p>（包含 {len(latest_tweet['images'])} 张图片）</p>"
            
            # If we have local images, add them to attachments
            if latest_tweet.get('local_images'):
                attachments.extend(latest_tweet['local_images'])
                email_html += "<p><b>图片附件预览（如未显示请查看附件栏）：</b></p>"
                # Note: For inline images in yagmail with list contents, it's automatic.
                # With HTML string, we rely on client showing attachments or simple inline logic.
                # yagmail's 'contents' parameter handles paths as inline images if they are in the list.
                # So we will pass [email_html, img_path1, img_path2...] to send_email.
            else:
                  # Fallback to remote links if download failed
                  # Use wsrv.nl as a reverse proxy to help load images in China/QQ Mail
                  for img_url in latest_tweet['images']:
                       proxy_url = f"https://wsrv.nl/?url={img_url}"
                       email_html += f"<div style='margin-bottom: 10px;'><img src='{proxy_url}' style='max-width: 100%; border-radius: 8px;'><br><a href='{img_url}'>查看原图</a></div>"
    else:
        subject = "Trae AI 工作流测试 - 抓取失败"
        email_html += "<h1>测试部分失败：未抓取到推文</h1>"
        email_html += "<p>邮件发送功能正常，但未能从 Nitter 抓取到推文。</p>"
        email_html += "<p>可能原因：</p>"
        email_html += "<ul>"
        email_html += "<li>当前配置的 RSSHub 实例均不可访问（网络超时或被封锁）。</li>"
        email_html += "<li>目标用户最近没有发推。</li>"
        email_html += "<li><b>如果你在中国大陆，请务必在 .env 文件中配置 PROXY_URL（例如 http://127.0.0.1:7890）。</b></li>"
        email_html += "</ul>"
        email_html += "<p>请尝试稍后重试，或在 twitter_monitor.py 中更新 RSSHUB_INSTANCES 列表。</p>"

    # Print the HTML content for debugging
    print("\n--- DEBUG: Generated Email HTML ---")
    print(email_html)
    print("-----------------------------------\n")

    try:
        # Prepare contents list
        contents = [email_html]
        # Add local images to contents to make them inline/attachments
        if attachments:
            contents.extend(attachments)
            
        success = send_email(subject, contents)
        if success:
            print(f"✅ 邮件发送成功！请检查收件箱: {config.RECEIVER_EMAIL}")
        else:
            print("❌ 邮件发送失败。请检查授权码（非密码）是否正确，以及是否开启了 POP3/SMTP 服务。")
    except Exception as e:
        print(f"❌ 发送过程出错: {e}")

if __name__ == "__main__":
    test()
