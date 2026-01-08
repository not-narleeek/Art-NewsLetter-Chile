from typing import List
from datetime import datetime, timedelta
from app.collector.scrapers.base import BaseScraper
from app.schemas.event import EventCreate
from app.models.enums import EventCategory, EventRegion, EventStatus

class InstagramScraper(BaseScraper):
    async def extract(self) -> List[EventCreate]:
        # Mock implementation for Instagram Graph API
        # Future: Use httpx to call graph.facebook.com/v18.0/me/media...
        
        events = []
        event = EventCreate(
            title="Taller de Cerámica (Instagram)",
            description="Post de Instagram convertido en evento.",
            start_date=datetime.now() + timedelta(days=12),
            category=EventCategory.ART,
            region=EventRegion.BIOBIO,
            external_url="https://instagram.com/p/dummy-post",
            status=EventStatus.DRAFT,
            image_url="https://via.placeholder.com/600x600.png?text=Instagram+Post"
        )
        events.append(event)
        return events
