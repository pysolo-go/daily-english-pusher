import time
import schedule
import logging
import config
from twitter_monitor import check_for_new_tweets, download_image
from email_sender import send_email
from PIL import Image
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

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

def job():
    logging.info("Starting batch check for all users...")
    
    # Store all found tweets across all users
    all_new_tweets = []
    
    for user in config.TWITTER_USERS:
        logging.info(f"Checking for new tweets from: {user}...")
        try:
            new_tweets = check_for_new_tweets(user)
            
            if not new_tweets:
                logging.info(f"No new tweets found for {user}.")
            else:
                logging.info(f"Found {len(new_tweets)} new tweets for {user}.")
                
                # Add author info if missing and collect
                for tweet in new_tweets:
                    tweet["author"] = tweet.get("author", user)
                    
                    # PROCESS IMAGES: Download and Resize immediately if not already done
                    # (check_for_new_tweets might have downloaded them, but we need to ensure resize)
                    if tweet.get("local_images"):
                        for local_path in tweet["local_images"]:
                            if os.path.exists(local_path):
                                resize_image_for_email(local_path, max_width=300)
                    
                    all_new_tweets.append(tweet)
        
        except Exception as e:
            logging.error(f"An error occurred while checking {user}: {e}")
            
        # Sleep briefly between users to avoid rate limiting
        time.sleep(2)
    
    # After checking all users, send one summary email if there are new tweets
    if all_new_tweets:
        logging.info(f"Preparing summary email for {len(all_new_tweets)} total new tweets.")
        
        # Sort by ID (approx time) descending
        all_new_tweets.sort(key=lambda x: int(x["id"]) if x["id"].isdigit() else x["id"], reverse=True)
        
        # Prepare email content
        subject = f"推特监控汇总: 发现 {len(all_new_tweets)} 条新消息"
        
        email_body = ""
        email_body += f"<h1>推特监控汇总 ({len(all_new_tweets)} 条)</h1>"
        email_body += f"<p>检测时间: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>"
        email_body += "<hr>"
        
        inline_images_list = []
        image_counter = 0

        for i, tweet in enumerate(all_new_tweets):
            author = tweet["author"]
            email_body += f"<div style='margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee;'>"
            email_body += f"<h2 style='margin-bottom: 10px; color: #1da1f2;'>{author}</h2>"
            email_body += f"<p style='font-size: 16px; line-height: 1.5;'>{tweet['text']}</p>"
            
            # Images (Use local images as inline attachments via CID)
            # This is the most robust way: no proxy reliance, no broken links.
            if tweet.get("local_images"):
                email_body += "<div style='margin-top: 10px;'>" 
                for local_path in tweet["local_images"]:
                    if os.path.exists(local_path):
                        image_counter += 1
                        cid = f"img_{image_counter}"
                        inline_images_list.append({
                            "path": local_path,
                            "cid": cid
                        })
                        
                        # Triple Lock Sizing (Container + HTML + CSS)
                        # Plus the image itself is physically resized to 300px max.
                        email_body += f"""
                        <div style="max-width: 300px; margin-top: 5px;">
                            <img src="cid:{cid}" width="300" style="width: 300px; max-width: 100%; height: auto; border-radius: 8px; display: block; border: 1px solid #eee;">
                        </div><br>
                        """
            
            # Fallback to remote images if local download failed but remote exists
            elif tweet.get("images"):
                 email_body += "<div style='margin-top: 10px; max-width: 300px;'>" 
                 for img_url in tweet["images"]:
                     # Fallback to simple proxy or original URL
                     proxy_url = f"https://wsrv.nl/?url={img_url}"
                     email_body += f"<img src='{proxy_url}' width='300' style='width: 300px; max-width: 100%; height: auto; border-radius: 8px; margin-top: 5px; display: block; border: 1px solid #eee;'><br>"
                 email_body += "</div>"


            
            email_body += f"<p><a href='{tweet['link']}' style='color: #888; text-decoration: none;'>🔗 查看原推</a></p>"
            email_body += "</div>"
        
        # Send digest email (with inline images)
        # Switch back to Resend as primary provider per user request
        success = send_email(subject, email_body, attachments=None, inline_images=inline_images_list, provider='resend')
        
        if success:
            logging.info("Summary email sent successfully.")
        else:
            logging.error("Failed to send summary email.")
    else:
        logging.info("No new tweets found in this cycle.")

    logging.info("Batch check completed.")

def main():
    logging.info(f"Starting Twitter Monitor for {len(config.TWITTER_USERS)} users.")
    logging.info(f"Users: {', '.join(config.TWITTER_USERS)}")
    logging.info(f"Check interval: {config.CHECK_INTERVAL} seconds")
    
    # Run once immediately
    job()
    
    # Schedule subsequent runs
    schedule.every(config.CHECK_INTERVAL).seconds.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
