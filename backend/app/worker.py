from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.core.email import send_email
from app.models.newsletter import Newsletter, NewsletterStatus
from app.models.subscriber import Subscriber
from app.collector.pipeline import CollectorPipeline
import asyncio
from datetime import datetime

@celery_app.task
def send_test_email(email_to: str, subject: str, content: str):
    send_email(email_to=email_to, subject=subject, html_content=content)
    return "Email sent"

@celery_app.task
def send_newsletter_task(newsletter_id: str):
    db = SessionLocal()
    try:
        newsletter = db.query(Newsletter).filter(Newsletter.id == newsletter_id).first()
        if not newsletter:
            return "Newsletter not found"
        
        newsletter.status = NewsletterStatus.SENDING
        db.commit()
        
        # Fetch active subscribers
        subscribers = db.query(Subscriber).filter(Subscriber.is_active == True).all()
        
        count = 0
        for sub in subscribers:
            # Send email strictly individually for personalization in future
            # For MVP, we just reuse the static content_html
            try:
                send_email(
                    email_to=sub.email,
                    subject=newsletter.subject,
                    html_content=newsletter.content_html
                )
                count += 1
            except Exception as e:
                print(f"Error sending to {sub.email}: {e}")
                
        newsletter.status = NewsletterStatus.SENT
        newsletter.sent_at = datetime.utcnow()
        db.commit()
        return f"Sent to {count} subscribers"
        
    finally:
        db.close()

@celery_app.task
def run_collector_task():
    db = SessionLocal()
    try:
        pipeline = CollectorPipeline(db)
        # Async to sync adapter for Celery
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        # In a real production celery with greenlets/threads, this might need tweaks
        # strictly simpler: run pipeline.run() inside a sync wrapper or standard async run
        result = loop.run_until_complete(pipeline.run())
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()
