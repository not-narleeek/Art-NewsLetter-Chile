from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.subscriber import SubscriberCreate, Subscriber
from app.services import subscriber_service

router = APIRouter()

@router.post("/", response_model=Subscriber, status_code=status.HTTP_201_CREATED)
def create_subscriber(
    subscriber_in: SubscriberCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new subscriber. Sends a confirmation email.
    """
    subscriber = subscriber_service.get_by_email(db, email=subscriber_in.email)
    if subscriber:
        if subscriber.is_active:
             raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )
        else:
            # Resend confirmation email logic could be here
            pass
            
    return subscriber_service.create_subscriber(db=db, subscriber_in=subscriber_in)

@router.get("/confirm/{token}", response_model=Subscriber)
def confirm_subscription(
    token: str,
    db: Session = Depends(get_db)
):
    """
    Confirm a subscription using the token sent via email.
    """
    subscriber = subscriber_service.confirm_subscription(db, token)
    if not subscriber:
        raise HTTPException(status_code=404, detail="Invalid or expired token")
    return subscriber
