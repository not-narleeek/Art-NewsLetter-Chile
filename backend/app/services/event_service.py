from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate
from app.models.enums import EventStatus, EventCategory, EventRegion
from typing import List, Optional
import uuid
import re

def generate_slug(title: str) -> str:
    # Simple slugify: lowercase, replace spaces with hyphens, remove non-alphanumeric
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s-]+', '-', slug).strip('-')
    return f"{slug}-{str(uuid.uuid4())[:8]}"

def get_event(db: Session, event_id: uuid.UUID) -> Optional[Event]:
    return db.query(Event).filter(Event.id == event_id).first()

def get_events(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[EventStatus] = None,
    category: Optional[EventCategory] = None,
    region: Optional[EventRegion] = None
) -> List[Event]:
    query = db.query(Event)
    
    if status:
        query = query.filter(Event.status == status)
    if category:
        query = query.filter(Event.category == category)
    if region:
        query = query.filter(Event.region == region)
        
    return query.order_by(desc(Event.start_date)).offset(skip).limit(limit).all()

def create_event(db: Session, event_in: EventCreate) -> Event:
    slug = event_in.slug if event_in.slug else generate_slug(event_in.title)
    
    db_obj = Event(
        **event_in.model_dump(exclude={"slug"}), # Pydantic v2
        slug=slug
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_event(db: Session, db_obj: Event, event_in: EventUpdate) -> Event:
    update_data = event_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
        
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_event(db: Session, db_obj: Event) -> Event:
    # Soft delete concept: simply archive it
    # But CRUD usually implies delete. 
    # For this system, let's implement actual delete but Plan mentioned soft-delete.
    # We will implement DELETE as Archiving for safety.
    db_obj.status = EventStatus.ARCHIVED
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
