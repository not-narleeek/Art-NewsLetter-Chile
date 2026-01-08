from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.newsletter import Newsletter, NewsletterCreate
from app.services import newsletter_service

router = APIRouter()

@router.get("/", response_model=List[Newsletter])
def read_newsletters(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    newsletters = newsletter_service.get_newsletters(db, skip=skip, limit=limit)
    return newsletters

@router.post("/preview", response_model=str)
def preview_newsletter(
    newsletter_in: NewsletterCreate,
    db: Session = Depends(get_db)
):
    """
    Returns HTML content for preview.
    """
    return newsletter_service.preview_newsletter(db, newsletter_in)

@router.post("/", response_model=Newsletter, status_code=status.HTTP_201_CREATED)
def create_newsletter(
    newsletter_in: NewsletterCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new newsletter draft.
    """
    return newsletter_service.create_newsletter(db, newsletter_in)

@router.post("/{newsletter_id}/send", response_model=Newsletter)
def send_newsletter(
    newsletter_id: str,
    db: Session = Depends(get_db)
):
    """
    Trigger sending of the newsletter.
    """
    newsletter = newsletter_service.send_newsletter(db, newsletter_id)
    if not newsletter:
        raise HTTPException(status_code=404, detail="Newsletter not found")
    return newsletter
