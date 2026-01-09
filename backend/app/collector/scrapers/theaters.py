import httpx
from bs4 import BeautifulSoup
from typing import List
from app.collector.scrapers.base import BaseScraper
from app.schemas.event import EventCreate
from app.models.enums import EventCategory, EventRegion, EventStatus

class MunicipalScraper(BaseScraper):
    BASE_URL = "https://www.municipal.cl"
    URL = "https://www.municipal.cl/cartelera/"

    async def extract(self) -> List[EventCreate]:
        extracted_events = []
        try:
             # TODO: Implement selector logic
             pass
        except Exception as e:
            print(f"Error scraping Teatro Municipal: {e}")
        return extracted_events

class CEACScraper(BaseScraper):
    BASE_URL = "https://ceacuchile.cl"
    URL = "https://ceacuchile.cl/cartelera/"

    async def extract(self) -> List[EventCreate]:
        extracted_events = []
        try:
             # TODO: Implement selector logic
             pass
        except Exception as e:
            print(f"Error scraping CEAC: {e}")
        return extracted_events

class SCDScraper(BaseScraper):
    BASE_URL = "https://www.salascd.cl"
    URL = "https://www.salascd.cl/cartelera/"

    async def extract(self) -> List[EventCreate]:
        extracted_events = []
        try:
             # TODO: Implement selector logic
             pass
        except Exception as e:
            print(f"Error scraping Salas SCD: {e}")
        return extracted_events

class BiobioScraper(BaseScraper):
    BASE_URL = "https://teatrobiobio.cl"
    URL = "https://teatrobiobio.cl/cartelera/"

    async def extract(self) -> List[EventCreate]:
        extracted_events = []
        try:
             # TODO: Implement selector logic
             pass
        except Exception as e:
            print(f"Error scraping Teatro Biobio: {e}")
        return extracted_events
