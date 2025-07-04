import requests
from bs4 import BeautifulSoup
from .models import ScrapedItem, ChangeLog

def fetch_fbi_data():
    url = 'https://www.fbi.gov/wanted/topten'
    print(url,'url')
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(response, 'response')
    
    new_items = []
    existing_titles = ScrapedItem.objects.values_list('title', flat=True)
    
    wanted_cards = soup.select('.portal-type-person')
    current_titles = set()
    
    for card in wanted_cards:
        title = card.select_one('h3.title').text.strip()
        image_url = card.img['src']
        description = card.select_one('.summary').text.strip()
        current_titles.add(title)
        
        if title not in existing_titles:
            ScrapedItem.objects.create(title=title, image_url=image_url, description=description)
            ChangeLog.objects.create(title=title, change_type='added')
    
    removed = set(existing_titles) - current_titles
    for r in removed:
        ChangeLog.objects.create(title=r, change_type='removed')
