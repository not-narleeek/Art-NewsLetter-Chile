from abc import ABC, abstractmethod
from typing import List, Optional, Dict
import httpx
from app.schemas.event import EventCreate

class BaseScraper(ABC):
    @abstractmethod
    async def extract(self) -> List[EventCreate]:
        """
        Extracts events from the source and returns a list of EventCreate objects.
        """
        pass

    async def _fetch_html(self, url: str, headers: Optional[Dict[str, str]] = None) -> Optional[str]:
        """
        Helper to fetch HTML content from a URL correctly handling errors.
        """
        if not headers:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
            }
            
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.text
        except Exception as e:
            print(f"Error fetching URL {url}: {e}")
            return None
