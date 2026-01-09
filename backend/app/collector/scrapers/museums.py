from typing import List, Optional
from datetime import datetime
import re
from bs4 import BeautifulSoup
from app.collector.scrapers.base import BaseScraper
from app.schemas.event import EventCreate
from app.models.enums import EventCategory, EventRegion, EventStatus

# Helper function
def parse_spanish_date(date_str: str) -> datetime:
    spanish_months = {
        'enero': 1, 'fenero': 1, 'ene': 1,
        'febrero': 2, 'feb': 2,
        'marzo': 3, 'mar': 3,
        'abril': 4, 'abr': 4,
        'mayo': 5, 'may': 5,
        'junio': 6, 'jun': 6,
        'julio': 7, 'jul': 7,
        'agosto': 8, 'ago': 8,
        'septiembre': 9, 'setiembre': 9, 'sep': 9,
        'octubre': 10, 'oct': 10,
        'noviembre': 11, 'nov': 11,
        'diciembre': 12, 'dic': 12
    }
    try:
        clean = date_str.lower().strip()
        # Pattern: 3 Oct 2025
        match = re.search(r'(\d{1,2})\s+([a-z]+)\s+(\d{4})', clean)
        if match:
            day = int(match.group(1))
            month_str = match.group(2)
            year = int(match.group(3))
            month = spanish_months.get(month_str, 1)
            return datetime(year, month, day)
            
        return datetime.now()
    except Exception:
        return datetime.now()

class GAMScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.url = "https://gam.cl/calendario/"

    async def extract(self) -> List[EventCreate]:
        html = await self._fetch_html(self.url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, "html.parser")
        events = []
        
        buttons = soup.select('button[data-bs-toggle="tooltip"]')
        
        for button in buttons:
            tooltip_content = button.get('title') or button.get('data-bs-original-title')
            if not tooltip_content:
                continue
                
            tooltip_soup = BeautifulSoup(tooltip_content, "html.parser")
            
            title_node = tooltip_soup.select_one('.tool-titulo p')
            if not title_node:
                continue
            title = title_node.get_text(strip=True)
            
            link_node = tooltip_soup.select_one('.tool-link a')
            url = link_node['href'] if link_node else None
            if url and not url.startswith('http'):
                url = f"https://gam.cl{url}"
            
            img_node = tooltip_soup.select_one('.tool-img img')
            image_url = img_node['src'] if img_node else None
            if image_url and not image_url.startswith('http'):
                image_url = f"https://gam.cl{image_url}"
                
            resumen = tooltip_soup.select_one('.tool-resumen p b')
            start_date = datetime.now()
            if resumen:
                date_str = resumen.get_text(strip=True)
                start_date = parse_spanish_date(date_str)
            
            if title and url:
                events.append(EventCreate(
                    title=title,
                    description=f"Evento GAM. Fechas: {resumen.get_text(strip=True) if resumen else 'N/A'}",
                    start_date=start_date,
                    external_url=url,
                    image_url=image_url,
                    category=EventCategory.ART,
                    region=EventRegion.METROPOLITANA,
                    status=EventStatus.DRAFT
                ))
                
        return events

class PrecolombinoScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.url = "https://precolombino.cl/wp/exposiciones/"

    async def extract(self) -> List[EventCreate]:
        html = await self._fetch_html(self.url)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        events = []
        
        items = soup.select('div.destacado-chico.mosaic-block')
        
        for item in items:
            link_node = item.select_one('a.mosaic-overlay')
            if not link_node:
                continue
                
            url = link_node.get('href')
            
            title_node = link_node.select_one('.details h3')
            title = title_node.get_text(strip=True) if title_node else "Sin título"
            
            desc_node = link_node.select_one('.details p')
            description = desc_node.get_text(strip=True) if desc_node else ""
            
            img_node = item.select_one('.mosaic-backdrop img')
            image_url = img_node.get('src') if img_node else None
            
            events.append(EventCreate(
                title=title,
                description=description,
                start_date=datetime.now(),
                external_url=url,
                image_url=image_url,
                category=EventCategory.ART,
                region=EventRegion.METROPOLITANA,
                status=EventStatus.DRAFT
            ))
            
        return events

class MuseoMemoriaScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.url = "https://mmdh.cl/cartelera"

    async def extract(self) -> List[EventCreate]:
        # Required implementation for advanced SPA scraping.
        # Currently returning empty to avoid blocking the pipeline.
        return []
