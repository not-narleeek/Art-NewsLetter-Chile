from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.subscriber import Subscriber
from app.models.event import Event
from app.models.newsletter import Newsletter
from app.models.enums import EventStatus, NewsletterStatus

def get_dashboard_stats(db: Session):
    total_subscribers = db.query(func.count(Subscriber.id)).scalar()
    active_subscribers = db.query(func.count(Subscriber.id)).filter(Subscriber.is_active == True).scalar()
    
    total_events = db.query(func.count(Event.id)).scalar()
    published_events = db.query(func.count(Event.id)).filter(Event.status == EventStatus.PUBLISHED).scalar()
    draft_events = db.query(func.count(Event.id)).filter(Event.status == EventStatus.DRAFT).scalar()
    
    total_newsletters = db.query(func.count(Newsletter.id)).scalar()
    sent_newsletters = db.query(func.count(Newsletter.id)).filter(Newsletter.status == NewsletterStatus.SENT).scalar()
    
    return {
        "subscribers": {
            "total": total_subscribers,
            "active": active_subscribers
        },
        "events": {
            "total": total_events,
            "published": published_events,
            "draft": draft_events
        },
        "newsletters": {
            "total": total_newsletters,
            "sent": sent_newsletters
        }
    }
