import requests
from bs4 import BeautifulSoup
from datetime import datetime

class OakTreeFetcher:
    def __init__(self):
        self.url = "https://www.oaktreecapital.com/insights/memos"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_latest_memos(self):
        """抓取最新的 Oak Tree Memos"""
        print(f"[OakTree] Fetching from {self.url}...")
        try:
            response = requests.get(self.url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            memos = []
            
            # 这是一个基于常见结构的猜测，因为无法实际查看页面源码。
            # 通常会有 article 标签，或者带有 memo/insight 类的 div。
            # 这里的逻辑寻找带有超链接的列表项
            
            # 在实际部署中，可能需要根据具体页面 DOM 结构调整选择器
            # 假设有一个列表容器
            items = soup.find_all('div', class_='oc-memo-item') # 假设的类名
            
            if not items:
                 # 备用：尝试查找所有包含 'memo' 文本的链接
                 links = soup.find_all('a', href=True)
                 for link in links:
                     if 'memos' in link['href'] and link.text.strip():
                         title = link.text.strip()
                         url = link['href']
                         if not url.startswith('http'):
                             url = "https://www.oaktreecapital.com" + url
                         
                         memos.append({
                             "title": title,
                             "url": url,
                             "source": "Oak Tree Capital",
                             "date": datetime.now().strftime("%Y-%m-%d"), # 暂无日期，使用当前日期
                             "content": title # 暂用标题作为内容，实际可能需要进一步点击抓取
                         })
                         # 简单的去重
                         if len(memos) > 5: break
            
            print(f"[OakTree] Found {len(memos)} memos.")
            return memos

        except Exception as e:
            print(f"[OakTree] Error fetching memos: {e}")
            return []
