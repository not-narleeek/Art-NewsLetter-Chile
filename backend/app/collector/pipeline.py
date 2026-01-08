from sqlalchemy.orm import Session
from typing import List
from app.schemas.event import EventCreate
from app.services import event_service
from app.collector.scrapers.chile_cultura import ChileCulturaScraper
from app.collector.scrapers.instagram import InstagramScraper

class CollectorPipeline:
    def __init__(self, db: Session):
        self.db = db
        self.scrapers = [
            ChileCulturaScraper(),
            InstagramScraper()
        ]
        
    async def run(self) -> dict:
        results = {
            "total_extracted": 0,
            "new_events": 0,
            "errors": []
        }
        
        for scraper in self.scrapers:
            try:
                events = await scraper.extract()
                results["total_extracted"] += len(events)
                
                for event_in in events:
                    # Deduplication logic
                    # Check by exact title match (simple) or implement slug check
                    # Since we generate slug from title + uuid in service, we can't check slug easily before creation
                    # unless we standardize slug generation.
                    # Best check: Title + Date overlap?
                    # For MVP: Simple Title check
                    existing = self.db.query(event_service.Event).filter(
                        event_service.Event.title == event_in.title
                    ).first()
                    
                    if not existing:
                        # Force DRAFT status for scraped events
                        event_in.status = "draft" 
                        event_service.create_event(self.db, event_in)
                        results["new_events"] += 1
                        
            except Exception as e:
                results["errors"].append(str(e))
                
        return results
