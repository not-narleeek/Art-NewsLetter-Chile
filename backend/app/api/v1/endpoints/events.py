from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.db.session import get_db
from app.schemas.event import Event, EventCreate, EventUpdate
from app.services import event_service
from app.core import storage
from app.models.enums import EventStatus, EventCategory, EventRegion

router = APIRouter()

@router.get("/", response_model=List[Event])
def read_events(
    skip: int = 0,
    limit: int = 100,
    status: Optional[EventStatus] = None,
    category: Optional[EventCategory] = None,
    region: Optional[EventRegion] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve events.
    """
    events = event_service.get_events(db, skip=skip, limit=limit, status=status, category=category, region=region)
    return events

@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    start_date: datetime = Form(...),
    end_date: Optional[datetime] = Form(None),
    category: EventCategory = Form(...),
    region: EventRegion = Form(...),
    external_url: Optional[str] = Form(None),
    status: EventStatus = Form(EventStatus.DRAFT),
    slug: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Create new event with optional image upload (Multipart Form Data).
    """
    image_url = None
    if image:
        try:
            image_url = await storage.save_image(image, filename=f"event-{title.lower()}")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
            
    event_in = EventCreate(
        title=title,
        description=description,
        start_date=start_date,
        end_date=end_date,
        category=category,
        region=region,
        external_url=external_url,
        status=status,
        slug=slug,
        image_url=image_url
    )
    
    return event_service.create_event(db=db, event_in=event_in)

@router.get("/{event_id}", response_model=Event)
def read_event(
    event_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get event by ID.
    """
    event = event_service.get_event(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=Event)
async def update_event(
    event_id: UUID,
    # Using simple JSON body for update without file for simplicity in this iteration, 
    # or multipart again. Let's do JSON for metadata update vs PATCH.
    # Actually, proper PUT with file requires multipart.
    # To simplify, we'll allow standard Body update via Pydantic schema for now (no new file upload in this easy endpoint).
    # If file upload is needed on update, a separate endpoint or multipart PUT is best.
    # For this MVP, let's stick to JSON update for props.
    event_in: EventUpdate,
    db: Session = Depends(get_db)
):
    """
    Update event (Metadata only).
    """
    event = event_service.get_event(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event = event_service.update_event(db=db, db_obj=event, event_in=event_in)
    return event

@router.delete("/{event_id}", response_model=Event)
def delete_event(
    event_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Archive event (Soft delete).
    """
    event = event_service.get_event(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event = event_service.delete_event(db=db, db_obj=event)
    return event
