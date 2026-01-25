import requests
from lxml import etree, html
import logging
import os
import re

import config

# RSSHub instances
RSSHUB_INSTANCES = [
    "https://rsshub.pseudoyu.com",
    "https://rsshub.app",
    "https://rsshub.feeded.xyz",
    "https://rsshub.moeyy.cn",
    "https://rss.shab.fun",
    "https://rsshub.ktachibana.party",
]

import json

LAST_TWEET_FILE = "tweet_monitor_state.json"

def get_last_seen_id(username):
    """
    Get the last seen tweet ID for a specific user.
    """
    if os.path.exists(LAST_TWEET_FILE):
        try:
            with open(LAST_TWEET_FILE, "r") as f:
                data = json.load(f)
                return data.get(username)
        except Exception as e:
            logging.error(f"Error reading state file: {e}")
            return None
    return None

def save_last_seen_id(username, tweet_id):
    """
    Save the last seen tweet ID for a specific user.
    """
    data = {}
    if os.path.exists(LAST_TWEET_FILE):
        try:
            with open(LAST_TWEET_FILE, "r") as f:
                data = json.load(f)
        except Exception as e:
            logging.error(f"Error reading state file for update: {e}")
    
    data[username] = tweet_id
    
    try:
        with open(LAST_TWEET_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving state file: {e}")

def download_image(url, save_dir="images"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    filename = os.path.join(save_dir, url.split("/")[-1])
    if "?" in filename:
        filename = filename.split("?")[0]
    
    proxies = {}
    if config.PROXY_URL:
        proxies = {
            "http": config.PROXY_URL,
            "https": config.PROXY_URL
        }

    try:
        response = requests.get(url, stream=True, timeout=10, proxies=proxies)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return filename
    except Exception as e:
        logging.error(f"Failed to download image {url}: {e}")
    return None

def clean_html_content(html_content):
    """
    Parses HTML content and extracts text while preserving line breaks.
    Replaces <br>, <p>, <div> tags with newlines.
    """
    if not html_content:
        return ""
    
    try:
        # Replace common block/break tags with a placeholder
        # This is a simple regex approach, can be improved with lxml
        content = html_content.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
        content = content.replace("</p>", "\n\n").replace("</div>", "\n")
        
        # Parse with lxml to strip tags
        tree = html.fromstring(content)
        text = tree.text_content()
        
        # Clean up excessive newlines
        lines = [line.strip() for line in text.split('\n')]
        # Filter out empty lines but keep single empty lines for paragraph breaks
        cleaned_lines = []
        for line in lines:
            if line:
                cleaned_lines.append(line)
            elif cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")
                
        return "\n".join(cleaned_lines).strip()
    except Exception as e:
        logging.warning(f"Error cleaning HTML content: {e}")
        return html_content

def check_for_new_tweets(username="realDonaldTrump"):
    """
    Checks for new tweets using RSSHub.
    Returns a list of new tweets (dict with text, images, id).
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    proxies = {}
    if config.PROXY_URL:
        proxies = {
            "http": config.PROXY_URL,
            "https": config.PROXY_URL
        }

    for instance in RSSHUB_INSTANCES:
        url = f"{instance}/twitter/user/{username}"
        logging.info(f"Checking RSSHub: {url}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=30, proxies=proxies)
            
            if response.status_code == 200:
                # Check if response is valid XML
                try:
                    root = etree.fromstring(response.content)
                except Exception as e:
                    logging.warning(f"Failed to parse XML from {instance}: {e}")
                    continue

                items = root.xpath("//item")
                if not items:
                    logging.warning(f"No items found in RSS from {instance}")
                    continue
                
                # Extract Channel Title (Author Name)
                try:
                    channel_title = root.xpath("//channel/title/text()")
                    author_name = channel_title[0] if channel_title else username
                    # Clean up common suffixes in RSSHub/Nitter
                    author_name = author_name.replace(" / Twitter", "").replace(" / X", "")
                except Exception:
                    author_name = username
                
                logging.info(f"Found {len(items)} items in RSS feed. Author: {author_name}")
                
                # Debug: print first item raw content (Uncomment for deep debugging)
                # if items:
                #     try:
                #         logging.info("--- DEBUG: First Item Raw Content ---")
                #         # etree.tostring returns bytes, decode to string
                #         logging.info(etree.tostring(items[0], pretty_print=True).decode('utf-8', errors='ignore'))
                #         logging.info("-------------------------------------")
                #     except Exception as e:
                #         logging.error(f"Failed to print debug info: {e}")

                found_tweets = []
                
                for i, item in enumerate(items[:10]): # Check top 10
                    try:
                        title = item.xpath("title/text()")[0] if item.xpath("title/text()") else ""
                        link = item.xpath("link/text()")[0] if item.xpath("link/text()") else ""
                        description = item.xpath("description/text()")[0] if item.xpath("description/text()") else ""
                        guid = item.xpath("guid/text()")[0] if item.xpath("guid/text()") else link
                        
                        logging.info(f"DEBUG Item {i}: title='{title}', link='{link}'")
                        logging.info(f"DEBUG Item {i} description raw length: {len(description)}")
                        
                        # Extract ID
                        # RSSHub link format usually: https://twitter.com/user/status/123...
                        tweet_id = None
                        if "/status/" in link:
                            tweet_id = link.split("/status/")[1].split("?")[0]
                        elif "/status/" in guid:
                            tweet_id = guid.split("/status/")[1].split("?")[0]
                        
                        if not tweet_id:
                            continue

                        # Extract images from description HTML
                        images = []
                        local_images = []
                        if description:
                            desc_tree = html.fromstring(description)
                            img_srcs = desc_tree.xpath("//img/@src")
                            for src in img_srcs:
                                # RSSHub sometimes proxies images, sometimes uses original
                                # Filter out emojis (often from twemoji)
                                if "twemoji" in src or "emoji" in src:
                                    continue
                                images.append(src)
                                
                                # Download image
                                local_path = download_image(src)
                                if local_path:
                                    local_images.append(local_path)
                                
                        # Clean up title/text (remove HTML tags if any, though title is usually plain text)
                        # RSSHub title often contains the tweet text
                        # But sometimes title is truncated. Description usually has full HTML content.
                        
                        full_text = title
                        
                        if description:
                            try:
                                # Use new cleaning function
                                desc_text = clean_html_content(description)
                                # If description text is longer than title, or title ends with ..., use description text
                                if len(desc_text) > len(title) or title.endswith("..."):
                                    full_text = desc_text
                            except Exception as e:
                                logging.warning(f"Failed to extract text from description: {e}")
                        
                        if not full_text or full_text == " ":
                            full_text = title # Fallback
                        
                        # Force Twitter link format
                        # Some RSSHub instances return nitter links or x.com links
                        # User requested https://twitter.com/
                        final_link = f"https://twitter.com/{username}/status/{tweet_id}"

                        logging.info(f"DEBUG Item {i} extracted: id={tweet_id}, text='{full_text}'")

                        found_tweets.append({
                            "id": tweet_id,
                            "text": full_text,
                            "images": images,
                            "local_images": local_images,
                            "link": final_link,
                            "author": author_name,
                            "is_pinned": False 
                        })
                    except Exception as e:
                        logging.error(f"Error parsing RSS item: {e}")
                        continue
                
                if found_tweets:
                    # Filter logic
                    # Sort by ID descending (newest first)
                    # Note: Tweet IDs are roughly chronological but big integers.
                    found_tweets.sort(key=lambda x: int(x["id"]) if x["id"].isdigit() else x["id"], reverse=True)
                    
                    last_seen_id = get_last_seen_id(username)
                    
                    if not last_seen_id:
                        # First run, save the latest ID
                        latest = found_tweets[0]
                        save_last_seen_id(username, latest["id"])
                        logging.info(f"First run for {username}. Saved latest ID: {latest['id']}")
                        # Return the latest one for testing confirmation
                        return [latest]
                    
                    # Return tweets newer than last_seen_id
                    new_items = []
                    for t in found_tweets:
                        if t["id"].isdigit() and last_seen_id.isdigit():
                            if int(t["id"]) > int(last_seen_id):
                                new_items.append(t)
                        else:
                            # Fallback string comparison if IDs are not digits (unlikely for Twitter)
                            if t["id"] > last_seen_id:
                                new_items.append(t)
                    
                    if new_items:
                        save_last_seen_id(username, new_items[0]["id"])
                        
                    return new_items
                
        except Exception as e:
            logging.error(f"Error checking RSSHub instance {instance}: {e}")
            continue
            
    logging.error("All RSSHub instances failed.")
    return []

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tweets = check_for_new_tweets()
    print(f"Found {len(tweets)} tweets")
    if tweets:
        print(tweets[0])
