# from celery import shared_task
# from .utils import fetch_fbi_data
# import requests
# from bs4 import BeautifulSoup
# from .models import ScrapedItem, ChangeLog
# import logging
# logger = logging.getLogger(__name__)

# @shared_task
# def scrape_fbi_data():
#     headers = {
#     "User-Agent": (
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#         "AppleWebKit/537.36 (KHTML, like Gecko) "
#         "Chrome/115.0.0.0 Safari/537.36"
#     ),
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Connection": "keep-alive",
# }
#     url = 'https://www.fbi.gov/wanted/topten'
#     logger.info(f"Scraping URL: {url}")
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     logger.info(f"Scraping response: {response}")
    
#     new_items = []
#     existing_titles = ScrapedItem.objects.values_list('title', flat=True)
    
#     wanted_cards = soup.select('.portal-type-person')
#     current_titles = set()
    
#     for card in wanted_cards:
#         title = card.select_one('h3.title').text.strip()
#         image_url = card.img['src']
#         description = card.select_one('.summary').text.strip()
#         current_titles.add(title)
        
#         if title not in existing_titles:
#             ScrapedItem.objects.create(title=title, image_url=image_url, description=description)
#             ChangeLog.objects.create(title=title, change_type='added')
    
#     removed = set(existing_titles) - current_titles
#     for r in removed:
#         ChangeLog.objects.create(title=r, change_type='removed')

#     #fetch_fbi_data()





# from celery import shared_task
# from requests_html import HTMLSession
# from bs4 import BeautifulSoup
# from .models import ScrapedItem, ChangeLog

# @shared_task
# def scrape_fbi_data():
#     print("🚀 Starting scrape with requests_html...")

#     session = HTMLSession()
#     try:
#         r = session.get("https://www.fbi.gov/wanted/topten")
#         r.html.render(timeout=30)  # Renders JavaScript content

#         soup = BeautifulSoup(r.html.html, "html.parser")

#         wanted_cards = soup.select("li.card.wanted-person")
#         print("✅ Found cards:", len(wanted_cards))

#         existing_titles = set(ScrapedItem.objects.values_list('title', flat=True))
#         current_titles = set()

#         for card in wanted_cards:
#             title_tag = card.select_one("h3.title")
#             img_tag = card.select_one("img")
#             desc_tag = card.select_one(".summary")

#             if not (title_tag and img_tag and desc_tag):
#                 continue

#             title = title_tag.text.strip()
#             image_url = img_tag['src']
#             description = desc_tag.text.strip()
#             current_titles.add(title)

#             if title not in existing_titles:
#                 ScrapedItem.objects.create(
#                     title=title,
#                     image_url=image_url,
#                     description=description
#                 )
#                 ChangeLog.objects.create(title=title, change_type='added')
#                 print(f"🆕 Added: {title}")

#         # Handle removed items
#         removed_titles = existing_titles - current_titles
#         for title in removed_titles:
#             ChangeLog.objects.create(title=title, change_type='removed')
#             print(f"❌ Removed: {title}")

#         print("✅ Scraping finished successfully.")

#     except Exception as e:
#         print("❗ Error during scraping:", e)



from celery import shared_task
import requests
from .models import ScrapedItem, ChangeLog

@shared_task
def scrape_fbi_data():
    print("🚀 Using FBI public API...")

    url = "https://www.fbi.gov/wanted/topten/api"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
        "Referer": "https://www.fbi.gov/wanted/topten",
        "Connection": "keep-alive",
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("❌ Failed to fetch data:", response.status_code)
        return

    data = response.json()
    items = data.get("items", [])

    print("✅ Found cards:", len(items))

    existing_titles = set(ScrapedItem.objects.values_list("title", flat=True))
    current_titles = set()

    for item in items:
        title = item.get("title", "").strip()
        description = item.get("description", "").strip()
        image_url = item.get("images", [{}])[0].get("original", "")
        current_titles.add(title)

        if title not in existing_titles:
            ScrapedItem.objects.create(
                title=title,
                image_url=image_url,
                description=description
            )
            ChangeLog.objects.create(title=title, change_type="added")
            print(f"🆕 Added: {title}")

    removed_titles = existing_titles - current_titles
    for title in removed_titles:
        ChangeLog.objects.create(title=title, change_type="removed")
        print(f"❌ Removed: {title}")

    print("✅ Scraping finished successfully.")
