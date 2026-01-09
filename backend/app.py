"""
Main FastAPI application for Newsletter Cultural Chile.
"""
from fastapi import FastAPI, Depends, HTTPException, Response, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
import secrets
import os

from database import get_db, init_db
from models import (
    Subscriber, Event, Newsletter, EmailLog,
    SubscriberStatus, EventStatus, EventCategory, NewsletterStatus
)
from email_service import send_confirmation_email, send_newsletter

# Initialize FastAPI app
app = FastAPI(
    title="Newsletter Cultural Chile",
    description="Sistema de newsletter cultural para Chile",
    version="1.0.0"
)

# Mount static files
if os.path.exists("../static"):
    app.mount("/static", StaticFiles(directory="../static"), name="static")

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()


# ============================================================================
# Pydantic Schemas
# ============================================================================

class SubscriberCreate(BaseModel):
    email: EmailStr
    region: Optional[str] = None


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    region: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    venue: Optional[str] = None
    address: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    region: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    venue: Optional[str] = None
    address: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[str] = None


# ============================================================================
# Subscriber Endpoints
# ============================================================================

@app.post("/api/subscribe")
def subscribe(subscriber_data: SubscriberCreate, db: Session = Depends(get_db)):
    """Subscribe a new user"""
    # Check if already subscribed
    existing = db.query(Subscriber).filter(Subscriber.email == subscriber_data.email).first()
    
    if existing:
        if existing.status == SubscriberStatus.ACTIVE:
            return {"message": "Ya estás suscrito", "status": "already_subscribed"}
        elif existing.status == SubscriberStatus.PENDING:
            # Resend confirmation
            send_confirmation_email(existing.email, existing.confirmation_token)
            return {"message": "Te hemos reenviado el correo de confirmación", "status": "resent"}
    
    # Create new subscriber
    confirmation_token = secrets.token_urlsafe(32)
    
    new_subscriber = Subscriber(
        email=subscriber_data.email,
        region=subscriber_data.region,
        status=SubscriberStatus.PENDING,
        confirmation_token=confirmation_token
    )
    
    db.add(new_subscriber)
    db.commit()
    
    # Send confirmation email
    send_confirmation_email(subscriber_data.email, confirmation_token)
    
    return {
        "message": "Por favor revisa tu correo para confirmar la suscripción",
        "status": "pending_confirmation"
    }


@app.get("/confirm/{token}")
def confirm_subscription(token: str, db: Session = Depends(get_db)):
    """Confirm email subscription"""
    subscriber = db.query(Subscriber).filter(
        Subscriber.confirmation_token == token
    ).first()
    
    if not subscriber:
        raise HTTPException(status_code=404, detail="Token inválido")
    
    if subscriber.status == SubscriberStatus.ACTIVE:
        return HTMLResponse("""
            <html><body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>✅ Ya estás suscrito</h1>
                <p>Tu suscripción ya estaba confirmada.</p>
            </body></html>
        """)
    
    # Activate subscriber
    subscriber.status = SubscriberStatus.ACTIVE
    subscriber.confirmed_at = datetime.utcnow()
    db.commit()
    
    return HTMLResponse("""
        <html><body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>🎉 ¡Suscripción confirmada!</h1>
            <p>Gracias por suscribirte a Newsletter Cultural Chile.</p>
            <p>Recibirás los mejores eventos culturales en tu correo.</p>
        </body></html>
    """)


@app.get("/unsubscribe")
def unsubscribe(email: EmailStr = Query(...), db: Session = Depends(get_db)):
    """Unsubscribe from newsletter"""
    subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
    
    if not subscriber:
        raise HTTPException(status_code=404, detail="Email no encontrado")
    
    subscriber.status = SubscriberStatus.UNSUBSCRIBED
    db.commit()
    
    return HTMLResponse("""
        <html><body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>👋 Suscripción cancelada</h1>
            <p>Has sido dado de baja de Newsletter Cultural Chile.</p>
            <p>Lamentamos verte partir.</p>
        </body></html>
    """)


# ============================================================================
# Event Endpoints
# ============================================================================

@app.get("/api/events")
def get_events(
    status: Optional[str] = None,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get list of events with filters"""
    query = db.query(Event)
    
    if status:
        query = query.filter(Event.status == EventStatus(status))
    if category:
        query = query.filter(Event.category == EventCategory(category))
    
    query = query.order_by(Event.start_date.desc())
    events = query.offset(skip).limit(limit).all()
    
    return {
        "events": [
            {
                "id": e.id,
                "title": e.title,
                "description": e.description,
                "category": e.category.value,
                "region": e.region,
                "start_date": e.start_date.isoformat(),
                "end_date": e.end_date.isoformat() if e.end_date else None,
                "venue": e.venue,
                "url": e.url,
                "image_url": e.image_url,
                "status": e.status.value
            }
            for e in events
        ],
        "total": query.count()
    }


@app.post("/api/events")
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    """Create a new event"""
    new_event = Event(
        title=event_data.title,
        description=event_data.description,
        category=EventCategory(event_data.category),
        region=event_data.region,
        start_date=event_data.start_date,
        end_date=event_data.end_date,
        venue=event_data.venue,
        address=event_data.address,
        url=event_data.url,
        image_url=event_data.image_url,
        status=EventStatus.PUBLISHED
    )
    
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    
    return {"message": "Evento creado", "id": new_event.id}


@app.get("/api/events/{event_id}")
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a single event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "category": event.category.value,
        "region": event.region,
        "start_date": event.start_date.isoformat(),
        "end_date": event.end_date.isoformat() if event.end_date else None,
        "venue": event.venue,
        "address": event.address,
        "url": event.url,
        "image_url": event.image_url,
        "status": event.status.value
    }


@app.put("/api/events/{event_id}")
def update_event(event_id: int, event_data: EventUpdate, db: Session = Depends(get_db)):
    """Update an event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    # Update fields
    update_data = event_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "category" and value:
            setattr(event, field, EventCategory(value))
        elif field == "status" and value:
            setattr(event, field, EventStatus(value))
        else:
            setattr(event, field, value)
    
    db.commit()
    
    return {"message": "Evento actualizado"}


@app.delete("/api/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete (archive) an event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    event.status = EventStatus.ARCHIVED
    db.commit()
    
    return {"message": "Evento archivado"}


# ============================================================================
# Newsletter Endpoints
# ============================================================================

@app.get("/api/newsletter/preview")
def preview_newsletter(db: Session = Depends(get_db)):
    """Preview newsletter with upcoming events"""
    # Get published events for next 45 days
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=45)
    
    events = db.query(Event).filter(
        Event.status == EventStatus.PUBLISHED,
        Event.start_date >= start_date,
        Event.start_date <= end_date
    ).order_by(Event.start_date).limit(15).all()
    
    events_data = [
        {
            "title": e.title,
            "description": e.description,
            "category": e.category.value.title(),
            "region": e.region,
            "start_date": e.start_date.strftime("%d/%m/%Y"),
            "end_date": e.end_date.strftime("%d/%m/%Y") if e.end_date else None,
            "venue": e.venue,
            "url": e.url,
            "image_url": e.image_url
        }
        for e in events
    ]
    
    return {
        "events": events_data,
        "count": len(events_data)
    }


@app.post("/api/newsletter/send")
def send_newsletter_now(db: Session = Depends(get_db)):
    """Send newsletter to all active subscribers"""
    from email_service import send_batch_newsletters
    
    # Get active subscribers
    subscribers = db.query(Subscriber).filter(
        Subscriber.status == SubscriberStatus.ACTIVE
    ).all()
    
    if not subscribers:
        return {"message": "No hay suscriptores activos", "sent": 0}
    
    # Get events for newsletter
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=45)
    
    events = db.query(Event).filter(
        Event.status == EventStatus.PUBLISHED,
        Event.start_date >= start_date,
        Event.start_date <= end_date
    ).order_by(Event.start_date).limit(15).all()
    
    # Create newsletter record
    newsletter = Newsletter(
        subject=f"Newsletter Cultural Chile - {start_date.strftime('%B %Y')}",
        status=NewsletterStatus.SENT,
        send_date=datetime.utcnow()
    )
    db.add(newsletter)
    db.commit()
    db.refresh(newsletter)
    
    # Prepare data
    subscribers_data = [{"id": s.id, "email": s.email} for s in subscribers]
    events_data = [
        {
            "title": e.title,
            "description": e.description,
            "category": e.category.value.title(),
            "region": e.region,
            "start_date": e.start_date.strftime("%d/%m/%Y"),
            "end_date": e.end_date.strftime("%d/%m/%Y") if e.end_date else None,
            "venue": e.venue,
            "url": e.url,
            "image_url": e.image_url
        }
        for e in events
    ]
    
    # Send emails
    stats = send_batch_newsletters(
        subscribers=subscribers_data,
        subject=newsletter.subject,
        events=events_data,
        newsletter_id=newsletter.id
    )
    
    return {
        "message": "Newsletter enviado",
        "sent": stats["sent"],
        "failed": stats["failed"],
        "newsletter_id": newsletter.id
    }


# ============================================================================
# Tracking Endpoints
# ============================================================================

@app.get("/track/open/{newsletter_id}/{subscriber_id}/{token}.gif")
def track_open(newsletter_id: int, subscriber_id: int, token: str, db: Session = Depends(get_db)):
    """Track email open"""
    # Find or create email log
    log = db.query(EmailLog).filter(
        EmailLog.newsletter_id == newsletter_id,
        EmailLog.subscriber_id == subscriber_id
    ).first()
    
    if log and not log.opened_at:
        log.opened_at = datetime.utcnow()
        db.commit()
    
    # Return 1x1 transparent GIF
    gif_data = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    return Response(content=gif_data, media_type="image/gif")


# ============================================================================
# Stats Endpoints
# ============================================================================

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get basic statistics"""
    total_subscribers = db.query(Subscriber).count()
    active_subscribers = db.query(Subscriber).filter(
        Subscriber.status == SubscriberStatus.ACTIVE
    ).count()
    total_events = db.query(Event).filter(
        Event.status == EventStatus.PUBLISHED
    ).count()
    
    return {
        "total_subscribers": total_subscribers,
        "active_subscribers": active_subscribers,
        "total_events": total_events
    }


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/")
def root():
    """Redirect to landing page"""
    return RedirectResponse(url="/static/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
