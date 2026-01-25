import time
import schedule
import logging
import config
from twitter_monitor import check_for_new_tweets, download_image
from email_sender import send_email
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
        
        for i, tweet in enumerate(all_new_tweets):
            author = tweet["author"]
            email_body += f"<div style='margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee;'>"
            email_body += f"<h2 style='margin-bottom: 10px; color: #1da1f2;'>{author}</h2>"
            email_body += f"<p style='font-size: 16px; line-height: 1.5;'>{tweet['text']}</p>"
            
            # Images (Inline via Proxy)
            if tweet.get("images"):
                email_body += "<div style='margin-top: 10px;'>"
                for img_url in tweet["images"]:
                    proxy_url = f"https://wsrv.nl/?url={img_url}"
                    email_body += f"<img src='{proxy_url}' style='max-width: 100%; border-radius: 8px; margin-top: 5px; display: block;'><br>"
                email_body += "</div>"
            
            email_body += f"<p><a href='{tweet['link']}' style='color: #888; text-decoration: none;'>🔗 查看原推</a></p>"
            email_body += "</div>"
        
        # Send digest email (No attachments to ensure stability)
        success = send_email(subject, email_body, attachments=None)
        
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
