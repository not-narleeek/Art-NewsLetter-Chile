from sqlalchemy.orm import Session
from typing import List
from app.schemas.event import EventCreate
from app.services import event_service
from app.collector.scrapers.chile_cultura import ChileCulturaScraper
from app.collector.scrapers.instagram import InstagramScraper
from app.collector.scrapers.mnba import MNBAScraper
from app.collector.scrapers.museums import GAMScraper, PrecolombinoScraper, MuseoMemoriaScraper
from app.collector.scrapers.galleries import AninatScraper, PatriciaReadyScraper, NACScraper
from app.collector.scrapers.theaters import MunicipalScraper, CEACScraper, SCDScraper, BiobioScraper
from app.collector.scrapers.agendas import SantiagoCulturaScraper, CulturizarteScraper
from app.collector.scrapers.foundations import TeatroAMilScraper, CorpArtesScraper, BAJScraper

class CollectorPipeline:
    def __init__(self, db: Session):
        self.db = db
        self.scrapers = [
            # ChileCulturaScraper(), # Mock scraper disabled
            MNBAScraper(),
            GAMScraper(),
            PrecolombinoScraper(),
            MuseoMemoriaScraper(),
            AninatScraper(),
            PatriciaReadyScraper(),
            NACScraper(),
            MunicipalScraper(),
            CEACScraper(),
            SCDScraper(),
            BiobioScraper(),
            SantiagoCulturaScraper(),
            CulturizarteScraper(),
            TeatroAMilScraper(),
            CorpArtesScraper(),
            BAJScraper(),
            # InstagramScraper()
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
