from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.enums import NewsletterStatus

class NewsletterBase(BaseModel):
    subject: str
    
class NewsletterCreate(NewsletterBase):
    event_ids: List[UUID]
    preview_text: Optional[str] = None

class NewsletterUpdate(NewsletterBase):
    pass

class NewsletterInDBBase(NewsletterBase):
    id: UUID
    status: NewsletterStatus
    content_html: str
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Newsletter(NewsletterInDBBase):
    pass
