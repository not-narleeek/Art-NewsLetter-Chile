import httpx
from bs4 import BeautifulSoup
from typing import List
from app.collector.scrapers.base import BaseScraper
from app.schemas.event import EventCreate
from app.models.enums import EventCategory, EventRegion, EventStatus

class SantiagoCulturaScraper(BaseScraper):
    BASE_URL = "https://www.santiagocultura.cl"
    URL = "https://www.santiagocultura.cl/agenda/"

    async def extract(self) -> List[EventCreate]:
        extracted_events = []
        try:
             # TODO: Implement selector logic
             pass
        except Exception as e:
            print(f"Error scraping Santiago Cultura: {e}")
        return extracted_events

class CulturizarteScraper(BaseScraper):
    BASE_URL = "https://culturizarte.cl"
    URL = "https://culturizarte.cl/category/panoramas/"

    async def extract(self) -> List[EventCreate]:
        extracted_events = []
        try:
             # TODO: Implement selector logic
             pass
        except Exception as e:
            print(f"Error scraping Culturizarte: {e}")
        return extracted_events
