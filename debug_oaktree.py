import requests
from bs4 import BeautifulSoup

url = "https://www.oaktreecapital.com/insights/memos"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Try to find the first few memo items and print their HTML to see if date is there
    # Looking for a general container if specific classes aren't known
    
    # Based on the user screenshot: "class='sf_colsIn col-md-10'" or "full-width-tabs-wrapper"
    print("Searching for 'full-width-tabs-wrapper'...")
    tabs = soup.find(class_="full-width-tabs-wrapper")
    if tabs:
        print("Found tabs wrapper.")
        # Look for the first active tab content
        active_tab = tabs.find(class_="tab active") # Note: class names might be different in raw HTML vs rendered
        if active_tab:
            print("Found active tab.")
            # Print first 500 chars of active tab
            print(active_tab.prettify()[:1000])
        else:
             # Just print the first appearing list of links/items
             print("No active tab found in static HTML. Printing first 5 links in tabs:")
             links = tabs.find_all('a')[:5]
             for l in links:
                 print(l)
                 print(l.parent) # check parent for date
                 
    else:
        print("Tabs wrapper not found. searching for 'memo' in text")
        links = soup.find_all('a', string=lambda t: t and "Bubble" in t)
        for l in links:
            print(f"Found link: {l}")
            print(f"Parent: {l.parent}")
            print(f"Grandparent: {l.parent.parent}")

except Exception as e:
    print(e)
