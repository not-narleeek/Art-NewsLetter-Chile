from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class SubscriberBase(BaseModel):
    email: EmailStr

class SubscriberCreate(SubscriberBase):
    pass

class SubscriberUpdate(SubscriberBase):
    pass

class SubscriberInDBBase(SubscriberBase):
    id: UUID
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Subscriber(SubscriberInDBBase):
    pass
