import os
from dotenv import load_dotenv

# 加载 .env 文件 (如果有)
load_dotenv()

# 飞书/Lark 配置
LARK_APP_ID = os.getenv("LARK_APP_ID", "your_app_id")
LARK_APP_SECRET = os.getenv("LARK_APP_SECRET", "your_app_secret")
# 目标多维表格 Base 的 Token 和 Table ID
LARK_BASE_TOKEN = os.getenv("LARK_BASE_TOKEN", "your_base_token")
LARK_TABLE_ID = os.getenv("LARK_TABLE_ID", "your_table_id")

# 目标 URL
OAK_TREE_URL = "https://www.oaktreecapital.com/insights/memos"
RAY_DALIO_LINKEDIN_URL = "https://www.linkedin.com/in/raydalio/recent-activity/articles/"

# LinkedIn Cookies (如果需要)
LINKEDIN_COOKIES = os.getenv("LINKEDIN_COOKIES", "")
