import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Optional
import re

from app.collector.scrapers.base import BaseScraper
from app.schemas.event import EventCreate
from app.models.enums import EventCategory, EventRegion, EventStatus

class MNBAScraper(BaseScraper):
    BASE_URL = "https://www.mnba.gob.cl"
    URL = "https://www.mnba.gob.cl/cartelera"

    async def extract(self) -> List[EventCreate]:
        extracted_events = []
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.URL, timeout=30.0)
                response.raise_for_status()
                
            soup = BeautifulSoup(response.text, 'lxml')
            
            # The container for each event
            events = soup.select('.views-row')
            
            for event_card in events:
                try:
                    event = self._parse_single_event(event_card)
                    if event:
                        extracted_events.append(event)
                except Exception as e:
                    print(f"Error parsing event: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping MNBA: {e}")
            
        return extracted_events

    def _parse_single_event(self, card: BeautifulSoup) -> Optional[EventCreate]:
        # Title and Link
        title_tag = card.select_one('.destacado__title a')
        if not title_tag:
            return None
            
        title = title_tag.get_text(strip=True)
        link = title_tag.get('href', '')
        if link.startswith('/'):
            link = self.BASE_URL + link
            
        # Image
        image_tag = card.select_one('.field--name-field-image img')
        image_url = ""
        if image_tag:
            src = image_tag.get('src', '')
            if src.startswith('/'):
                image_url = self.BASE_URL + src
            else:
                image_url = src

        # Date Parsing
        # Try to get the specific single date field first (often clearer)
        date_text = None
        date_start = datetime.now()
        
        # Structure often has 'date' or 'field--name-field-fechas'
        date_el = card.select_one('.date')
        range_el = card.select_one('.field--name-field-fechas')
        
        # Prefer the range text if available as it often contains the start date clearly
        if range_el:
            date_text = range_el.get_text(strip=True)
        elif date_el:
            date_text = date_el.get_text(strip=True)
            
        if date_text:
            date_start = self._parse_spanish_date(date_text)

        description = f"Evento en Museo Nacional de Bellas Artes. Más info en: {link}"

        return EventCreate(
            title=title,
            description=description,
            start_date=date_start,
            category=EventCategory.ART,
            region=EventRegion.METROPOLITANA,
            external_url=link,
            status=EventStatus.DRAFT,
            image_url=image_url
        )

    def _parse_spanish_date(self, date_str: str) -> datetime:
        """
        Parses dates like '10/Julio/2025' or '10/Julio/2025 hasta el ...'
        """
        # Mapping Spanish months
        spanish_months = {
            'enero': 1, 'fenero': 1,
            'febrero': 2,
            'marzo': 3,
            'abril': 4,
            'mayo': 5,
            'junio': 6,
            'julio': 7,
            'agosto': 8,
            'septiembre': 9, 'setiembre': 9,
            'octubre': 10,
            'noviembre': 11,
            'diciembre': 12
        }
        
        try:
            # Clean string
            clean_str = date_str.lower().strip()
            
            # Extract first date pattern: dd/month/yyyy
            # Regex to find day, month (text), year
            match = re.search(r'(\d{1,2})\/([a-z]+)\/(\d{4})', clean_str)
            
            if match:
                day = int(match.group(1))
                month_str = match.group(2)
                year = int(match.group(3))
                
                month = spanish_months.get(month_str, 1)
                return datetime(year, month, day)
            
            # Fallback current date
            return datetime.now()
            
        except Exception:
            return datetime.now()
