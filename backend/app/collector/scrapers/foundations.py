import httpx
from bs4 import BeautifulSoup
from typing import List
from app.collector.scrapers.base import BaseScraper
from app.schemas.event import EventCreate
from app.models.enums import EventCategory, EventRegion, EventStatus

class TeatroAMilScraper(BaseScraper):
    BASE_URL = "https://teatroamil.cl"
    URL = "https://teatroamil.cl/cartelera/"

    async def extract(self) -> List[EventCreate]:
        extracted_events = []
        try:
             # TODO: Implement selector logic
             pass
        except Exception as e:
            print(f"Error scraping Teatro a Mil: {e}")
        return extracted_events

class CorpArtesScraper(BaseScraper):
    BASE_URL = "https://www.corpartes.cl"
    URL = "https://www.corpartes.cl/cartelera/"

    async def extract(self) -> List[EventCreate]:
        extracted_events = []
        try:
             # TODO: Implement selector logic
             pass
        except Exception as e:
            print(f"Error scraping CorpArtes: {e}")
        return extracted_events

class BAJScraper(BaseScraper):
    BASE_URL = "https://www.balmacedartejoven.cl"
    URL = "https://www.balmacedartejoven.cl/agenda/"

    async def extract(self) -> List[EventCreate]:
        extracted_events = []
        try:
             # TODO: Implement selector logic
             pass
        except Exception as e:
            print(f"Error scraping BAJ: {e}")
        return extracted_events
