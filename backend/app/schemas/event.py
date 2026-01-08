from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.enums import EventStatus, EventCategory, EventRegion

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    category: EventCategory
    region: EventRegion
    external_url: Optional[str] = None # Pydantic v2 Url is stricter, using str for flexibility or HttpUrl
    image_url: Optional[str] = None
    status: EventStatus = EventStatus.DRAFT

    @field_validator('end_date')
    @classmethod
    def check_dates(cls, v, info):
        if v and info.data.get('start_date') and v < info.data['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

class EventCreate(EventBase):
    slug: Optional[str] = None # Can be auto-generated or provided

class EventUpdate(EventBase):
    title: Optional[str] = None
    start_date: Optional[datetime] = None
    category: Optional[EventCategory] = None
    region: Optional[EventRegion] = None

class EventInDBBase(EventBase):
    id: UUID
    slug: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Event(EventInDBBase):
    pass
