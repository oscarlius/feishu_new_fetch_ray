import requests
import json
import time
from config import LARK_APP_ID, LARK_APP_SECRET

class LarkClient:
    def __init__(self):
        self.app_id = LARK_APP_ID
        self.app_secret = LARK_APP_SECRET
        self.token = None
        self.token_expire_time = 0

    def get_tenant_access_token(self):
        """获取 Tenant Access Token (企业自建应用)"""
        if self.token and time.time() < self.token_expire_time:
            return self.token

        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("code") == 0:
                self.token = data["tenant_access_token"]
                # 提前 5 分钟过期，确保安全性
                self.token_expire_time = time.time() + data["expire"] - 300
                print(f"[Lark] Token acquired, expires in {data['expire']}s")
                return self.token
            else:
                print(f"[Lark] Error getting token: {data}")
                return None
        except Exception as e:
            print(f"[Lark] Exception getting token: {e}")
            return None

    def translate_text(self, text, source_lang="en", target_lang="zh"):
        """使用飞书翻译 API 翻译文本"""
        token = self.get_tenant_access_token()
        if not token:
            return None

        url = "https://open.feishu.cn/open-apis/translation/v1/text/translate"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        payload = {
            "source_language": source_lang,
            "target_language": target_lang,
            "text": text
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("code") == 0:
                return data["data"]["translation"]
            else:
                print(f"[Lark] Translation error: {data}")
                return text # Return original if translation fails
        except Exception as e:
            print(f"[Lark] Translation exception: {e}")
            return text

    def create_record(self, app_token, table_id, fields):
        """在多维表格中创建记录"""
        token = self.get_tenant_access_token()
        if not token:
            return None

        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        payload = {
            "fields": fields
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("code") == 0:
                print(f"[Lark] Record created successfully.")
                return data["data"]["record"]
            else:
                print(f"[Lark] Create record error: {data}")
                return None
        except Exception as e:
            print(f"[Lark] Create record exception: {e}")
            return None
