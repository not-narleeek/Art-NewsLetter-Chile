import uuid
from sqlalchemy import Column, String, Text, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base_class import Base
from app.models.enums import EventStatus, EventCategory, EventRegion

class Event(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    
    category = Column(SAEnum(EventCategory), nullable=False, index=True)
    region = Column(SAEnum(EventRegion), nullable=False, index=True)
    
    external_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    
    status = Column(SAEnum(EventStatus), default=EventStatus.DRAFT, nullable=False, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
