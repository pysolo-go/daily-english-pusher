import os
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
QQ_EMAIL = os.getenv("QQ_EMAIL")
QQ_EMAIL_PASSWORD = os.getenv("QQ_EMAIL_PASSWORD") # This should be the authorization code (授权码), not the login password
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", QQ_EMAIL) # Default to sending to self

# Twitter Configuration
# 监控列表：特朗普 + 核心新闻源 + 关键人物
TWITTER_USERS = [
    "realDonaldTrump",  # 特朗普
    "BBCBreaking",      # BBC 突发新闻 (全球视野)
    "BBCWorld",         # BBC 世界新闻
    "Reuters",          # 路透社 (金融/政治权威)
    "AP",               # 美联社 (事实源头)
    "elonmusk",         # 马斯克 (政策/科技风向)
    "DeItaone",         # Walter Bloomberg (全球金融快讯，非常快)
]
CHECK_INTERVAL = 300 # Check every 5 minutes

# Proxy Configuration (Optional)
# Example: http://127.0.0.1:7890
PROXY_URL = os.getenv("PROXY_URL")
