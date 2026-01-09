import httpx
from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
import re
from app.collector.scrapers.base import BaseScraper
from app.schemas.event import EventCreate
from app.models.enums import EventCategory, EventRegion, EventStatus

def parse_spanish_date(date_str: str) -> datetime:
    spanish_months = {
        'enero': 1, 'fenero': 1, 'ene': 1, 'january': 1,
        'febrero': 2, 'feb': 2, 'february': 2,
        'marzo': 3, 'mar': 3, 'march': 3,
        'abril': 4, 'abr': 4, 'april': 4,
        'mayo': 5, 'may': 5,
        'junio': 6, 'jun': 6, 'june': 6,
        'julio': 7, 'jul': 7, 'july': 7,
        'agosto': 8, 'ago': 8, 'august': 8,
        'septiembre': 9, 'setiembre': 9, 'sep': 9, 'september': 9,
        'octubre': 10, 'oct': 10, 'october': 10,
        'noviembre': 11, 'nov': 11, 'november': 11,
        'diciembre': 12, 'dic': 12, 'december': 12
    }
    try:
        clean = date_str.lower().strip()
        # Pattern: 18 de noviembre de 2025 or 18 Nov 2025
        match = re.search(r'(\d{1,2})\s+(?:de\s+)?([a-z]+)\s+(?:de\s+)?(\d{4})', clean)
        if match:
            day = int(match.group(1))
            month_str = match.group(2)
            year = int(match.group(3))
            month = spanish_months.get(month_str, 1)
            return datetime(year, month, day)
        
        # Try finding just a month and year if day missing? Rare.
        return datetime.now()
    except Exception:
        return datetime.now()

class AninatScraper(BaseScraper):
    BASE_URL = "https://aninatgaleria.org"
    URLS = [
        "https://aninatgaleria.org/exhibiciones-2025-aux",
        "https://www.aninatgaleria.org/exhibiciones-2024",
        "https://www.aninatgaleria.org/exhibiciones-2023"
    ]

    async def extract(self) -> List[EventCreate]:
        extracted_events = []
        for url in self.URLS:
            try:
                html = await self._fetch_html(url)
                if not html:
                    continue
                
                soup = BeautifulSoup(html, 'html.parser')
                articles = soup.select('article.BlogList-item')
                
                for article in articles:
                    title_elem = article.select_one('.BlogList-item-title')
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    if link and not link.startswith('http'):
                        link = f"{self.BASE_URL}{link}"
                    
                    img_elem = article.select_one('img')
                    image_url = None
                    if img_elem:
                        image_url = img_elem.get('data-image') or img_elem.get('src')
                    
                    # Date extraction
                    start_date = datetime.now()
                    desc_elem = article.select_one('.BlogList-item-excerpt')
                    desc_text = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # Try to find a date in the excerpt
                    # Format: "Del 22 de noviembre al 31 de diciembre"
                    # We usually want the START date for sorting
                    # Regex for "Del X de Month"
                    date_match = re.search(r'(?:Del|Desde el)\s+(\d{1,2})\s+de\s+([a-z]+)', desc_text.lower())
                    if date_match:
                        day = int(date_match.group(1))
                        month_str = date_match.group(2)
                        # We accept current year by default, or look for year
                        year = datetime.now().year
                        # Check if year is in text
                        year_match = re.search(r'202\d', desc_text)
                        if year_match:
                            year = int(year_match.group(0))
                        
                        try:
                            month = self._get_month_number(month_str)
                            start_date = datetime(year, month, day)
                        except:
                            pass
                    else:
                        # Fallback to publish date meta
                        date_meta = article.select_one('.Blog-meta-item--date')
                        if date_meta:
                            start_date = parse_spanish_date(date_meta.get_text(strip=True))

                    extracted_events.append(EventCreate(
                        title=title,
                        description=desc_text,
                        start_date=start_date,
                        external_url=link,
                        image_url=image_url,
                        category=EventCategory.ART,
                        region=EventRegion.METROPOLITANA,
                        status=EventStatus.DRAFT
                    ))

            except Exception as e:
                print(f"Error scraping Galeria Aninat URL {url}: {e}")
                
        return extracted_events

    def _get_month_number(self, month_str: str) -> int:
        spanish_months = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
            'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
        return spanish_months.get(month_str.lower(), 1)

class NACScraper(BaseScraper):
    BASE_URL = "https://galerianac.cl"
    URL = "https://galerianac.cl/blogs/exposiciones"

    async def extract(self) -> List[EventCreate]:
        extracted_events = []
        try:
            html = await self._fetch_html(self.URL)
            if not html:
                return []
            
            soup = BeautifulSoup(html, 'html.parser')
            articles = soup.select('article') # Inside the main blog section
            
            for article in articles:
                title_elem = article.select_one('h3 a')
                if not title_elem:
                    continue
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                if link and not link.startswith('http'):
                    link = f"{self.BASE_URL}{link}"
                
                # Image in style attribute
                img_link = article.select_one('a.img')
                image_url = None
                if img_link and 'style' in img_link.attrs:
                    style = img_link['style']
                    # style="background-image: url(//cdn.shopify.com/...)"
                    match = re.search(r'url\((.*?)\)', style)
                    if match:
                        image_url = match.group(1).strip("'\"")
                        if image_url.startswith('//'):
                            image_url = f"https:{image_url}"
                
                # Description and Date
                bajada = article.select_one('.bajada')
                desc_text = bajada.get_text(strip=True) if bajada else ""
                
                # Parse date from description
                # "28 de Noviembre del 2025 al 10 de Enero del 2026"
                start_date = datetime.now()
                # Find first date pattern
                date_match = re.search(r'(\d{1,2})\s+de\s+([A-Za-z]+)(?:\s+del)?\s+(\d{4})', desc_text)
                if date_match:
                    start_date = parse_spanish_date(date_match.group(0))
                
                extracted_events.append(EventCreate(
                    title=title,
                    description=desc_text,
                    start_date=start_date,
                    external_url=link,
                    image_url=image_url,
                    category=EventCategory.ART,
                    region=EventRegion.METROPOLITANA,
                    status=EventStatus.DRAFT
                ))

        except Exception as e:
            print(f"Error scraping Galeria NAC: {e}")
        return extracted_events

class PatriciaReadyScraper(BaseScraper):
    BASE_URL = "https://galeriapready.cl"
    URL = "https://galeriapready.cl/exhibiciones"

    async def extract(self) -> List[EventCreate]:
        extracted_events = []
        try:
            # Webflow often requires User-Agent
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
            }
            html = await self._fetch_html(self.URL, headers=headers)
            if not html:
                return []
            
            soup = BeautifulSoup(html, 'html.parser')
            # Look for the exhibition items
            # Based on browser inspection: .w-dyn-item containing .exhib-tabs-item
            items = soup.select('.w-dyn-item .exhib-tabs-item')
            
            for item in items:
                title_div = item.select_one('.exhib-tab-title')
                if not title_div:
                    continue
                title = title_div.get_text(strip=True)
                
                desc_div = item.select_one('.exhib-tab-descr')
                description = desc_div.get_text(strip=True) if desc_div else ""
                
                link = item.get('href', '')
                if link and not link.startswith('http'):
                    link = f"{self.BASE_URL}{link}"
                
                img = item.select_one('img.exhib-tabs-img')
                image_url = img.get('src') if img else None
                
                # Date is not in the list view, usually.
                # Use current date as fallback or try to find it in description if present
                start_date = datetime.now()
                
                extracted_events.append(EventCreate(
                    title=title,
                    description=description,
                    start_date=start_date,
                    external_url=link,
                    image_url=image_url,
                    category=EventCategory.ART,
                    region=EventRegion.METROPOLITANA,
                    status=EventStatus.DRAFT
                ))

        except Exception as e:
            print(f"Error scraping Galeria Patricia Ready: {e}")
        return extracted_events
