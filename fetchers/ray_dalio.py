import requests
from bs4 import BeautifulSoup
from config import LINKEDIN_COOKIES

class RayDalioFetcher:
    def __init__(self):
        self.url = "https://www.linkedin.com/in/raydalio/recent-activity/articles/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }
        if LINKEDIN_COOKIES:
            self.headers["Cookie"] = LINKEDIN_COOKIES

    def fetch_latest_articles(self):
        """抓取 Ray Dalio 最新的 LinkedIn 文章"""
        print(f"[RayDalio] Fetching from {self.url}...")
        
        if not LINKEDIN_COOKIES:
             print("[RayDalio] Warning: No LinkedIn Cookies provided. This fetch will likely fail or return a login page.")

        try:
            response = requests.get(self.url, headers=self.headers, timeout=15)
            # LinkedIn 返回 999 状态码表示被阻止
            if response.status_code == 999:
                print("[RayDalio] Request blocked by LinkedIn (Status 999). Authentication cookies are required.")
                return []
            
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            
            # 需要 LinkedIn 的实际 DOM 结构来解析
            # 这是一个占位逻辑。通常 LinkedIn 的类名是混淆过的 (例如 .ember-view)
            # 如果没有 Auth，看到的页面完全不同。
            
            print("[RayDalio] Parsing logic is highly dependent on login state.")
            # 这是一个示例，假设我们能看到公共页面
            items = soup.find_all('li', class_='artdeco-card')
            
            for item in items:
                link = item.find('a', href=True)
                if link:
                    title = link.get_text().strip()
                    url = link['href']
                    articles.append({
                        "title": title,
                        "url": url,
                        "source": "Ray Dalio (LinkedIn)",
                        "date": "Today",
                        "content": title
                    })
            
            if not articles:
                 print("[RayDalio] No articles found (possibly due to login wall).")

            return articles

        except Exception as e:
            print(f"[RayDalio] Error fetching articles: {e}")
            return []
