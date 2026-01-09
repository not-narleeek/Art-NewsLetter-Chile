import uuid
from sqlalchemy.orm import Session
from app.models.subscriber import Subscriber
from app.schemas.subscriber import SubscriberCreate
from app.core.email import send_email
from app.core.config import settings

def get_by_email(db: Session, email: str) -> Subscriber | None:
    return db.query(Subscriber).filter(Subscriber.email == email).first()

def get_by_token(db: Session, token: str) -> Subscriber | None:
    return db.query(Subscriber).filter(Subscriber.confirmation_token == token).first()

def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Subscriber]:
    return db.query(Subscriber).offset(skip).limit(limit).all()

def create_subscriber(db: Session, subscriber_in: SubscriberCreate) -> Subscriber:
    # Check if exists
    existing = get_by_email(db, subscriber_in.email)
    if existing:
        return existing # Return existing to avoid error leaking or resend email logic could go here

    confirmation_token = str(uuid.uuid4())
    db_obj = Subscriber(
        email=subscriber_in.email,
        is_active=False,
        confirmation_token=confirmation_token
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    # Send confirmation email
    confirm_url = f"{settings.API_V1_STR}/subscribers/confirm/{confirmation_token}"
    # In a real app the link would be to the frontend, which then calls the API.
    # For this MVP API-first approach, we link to API or Frontend.
    # Let's link to Frontend: http://localhost:3000/confirm?token=...
    # But for MVP instructions "GET /subscribers/confirm/{token}" implies API handling it directly or returning a redirect.
    # Let's use the API endpoint for now as requested.
    
    full_confirm_url = f"http://localhost:8000{confirm_url}"
    
    email_content = f"""
    <h1>Confirm your subscription</h1>
    <p>Please click the link below to confirm your subscription to Art Newsletter Chile:</p>
    <a href="{full_confirm_url}">Confirm Subscription</a>
    """
    
    send_email(
        email_to=subscriber_in.email,
        subject="Confirm your subscription - Art Newsletter Chile",
        html_content=email_content
    )
    
    return db_obj

def confirm_subscription(db: Session, token: str) -> Subscriber | None:
    subscriber = get_by_token(db, token)
    if not subscriber:
        return None
    
    subscriber.is_active = True
    subscriber.confirmation_token = None # Clear token after use
    db.add(subscriber)
    db.commit()
    db.refresh(subscriber)
    return subscriber

def delete_subscriber(db: Session, subscriber_id: uuid.UUID) -> Subscriber | None:
    subscriber = db.query(Subscriber).filter(Subscriber.id == subscriber_id).first()
    if subscriber:
        db.delete(subscriber)
        db.commit()
    return subscriber
