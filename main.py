import time
from config import LARK_BASE_TOKEN, LARK_TABLE_ID
from lark_client import LarkClient
from fetchers.oak_tree import OakTreeFetcher
from fetchers.ray_dalio import RayDalioFetcher

def main():
    print("=== Starting News Fetching Job ===")

    # Initialize Client
    lark = LarkClient()
    oak_fetcher = OakTreeFetcher()
    dalio_fetcher = RayDalioFetcher()

    all_articles = []

    # 1. Fetch from Oak Tree
    try:
        memos = oak_fetcher.fetch_latest_memos()
        all_articles.extend(memos)
    except Exception as e:
        print(f"Error fetching Oak Tree memos: {e}")

    # 2. Fetch from Ray Dalio
    try:
        articles = dalio_fetcher.fetch_latest_articles()
        all_articles.extend(articles)
    except Exception as e:
        print(f"Error fetching Ray Dalio articles: {e}")

    print(f"Total articles found: {len(all_articles)}")

    # 3. Process each article
    for article in all_articles:
        print(f"Processing: {article['title']}")
        
        # Translate Title
        translated_title = lark.translate_text(article['title'])
        print(f"  Translated Title: {translated_title}")
        
        # Translate Content (Summary or full text depending on what we fetched)
        # Note: Translating large blocks might hit limits or require segmentation.
        # Here we just translate the first 500 chars if it's long.
        content_to_translate = article['content'][:1000] 
        translated_content = lark.translate_text(content_to_translate)

        # 4. Upload to Lark
        fields = {
            "Title (English)": article['title'],
            "Title (Chinese)": translated_title,
            "URL": article['url'],
            "Source": article['source'],
            "Publish Date": article['date'], # Needs to match Date field format in Base
            "Content (Original)": article['content'],
            "Content (Translated)": translated_content
        }

        # Note: You need to ensure the keys in `fields` match the EXACT field names in your Lark Base table.
        # If they don't match, the create_record call will fail or ignore them.
        
        result = lark.create_record(LARK_BASE_TOKEN, LARK_TABLE_ID, fields)
        if result:
            print("  -> Uploaded to Lark successfully.")
        else:
            print("  -> Failed to upload to Lark.")
        
        time.sleep(1) # Rate limit protection

    print("=== Job Finished ===")

if __name__ == "__main__":
    main()
