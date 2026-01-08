from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.models.newsletter import Newsletter
from app.models.event import Event
from app.schemas.newsletter import NewsletterCreate
from app.services import template_service
from app.worker import send_newsletter_task
from app.models.enums import NewsletterStatus

def get_newsletters(db: Session, skip: int = 0, limit: int = 100) -> List[Newsletter]:
    return db.query(Newsletter).order_by(desc(Newsletter.created_at)).offset(skip).limit(limit).all()

def get_newsletter(db: Session, newsletter_id: str) -> Optional[Newsletter]:
    return db.query(Newsletter).filter(Newsletter.id == newsletter_id).first()

def preview_newsletter(db: Session, newsletter_in: NewsletterCreate) -> str:
    events = db.query(Event).filter(Event.id.in_(newsletter_in.event_ids)).all()
    # Simple order by start date
    events.sort(key=lambda x: x.start_date)
    
    return template_service.render_newsletter(
        events=events,
        title=newsletter_in.subject,
        preview_text=newsletter_in.preview_text
    )

def create_newsletter(db: Session, newsletter_in: NewsletterCreate) -> Newsletter:
    content_html = preview_newsletter(db, newsletter_in)
    
    db_obj = Newsletter(
        subject=newsletter_in.subject,
        content_html=content_html,
        status=NewsletterStatus.DRAFT
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def send_newsletter(db: Session, newsletter_id: str) -> Optional[Newsletter]:
    newsletter = get_newsletter(db, newsletter_id)
    if not newsletter:
        return None
    
    if newsletter.status != NewsletterStatus.DRAFT:
        # Already sending or sent
        # Logic to allow resend or retry could go here
        pass
        
    # Trigger Celery Task
    send_newsletter_task.delay(str(newsletter.id))
    
    # Update status to SENDING tentatively (worker will confirm)
    newsletter.status = NewsletterStatus.SENDING
    db.commit()
    db.refresh(newsletter)
    return newsletter
