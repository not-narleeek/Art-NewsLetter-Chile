"""
Database models for the newsletter application.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum as SQLEnum, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class SubscriberStatus(enum.Enum):
    """Subscriber status enum"""
    PENDING = "pending"
    ACTIVE = "active"
    UNSUBSCRIBED = "unsubscribed"
    BOUNCED = "bounced"


class EventCategory(enum.Enum):
    """Event category enum"""
    ARTE = "arte"
    MUSICA = "musica"
    TEATRO = "teatro"
    LITERATURA = "literatura"
    CINE = "cine"
    OTROS = "otros"


class EventStatus(enum.Enum):
    """Event status enum"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    PENDING_REVIEW = "pending_review"


class NewsletterStatus(enum.Enum):
    """Newsletter status enum"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENT = "sent"


# Association table for newsletter-events many-to-many relationship
newsletter_events = Table(
    'newsletter_events',
    Base.metadata,
    Column('newsletter_id', Integer, ForeignKey('newsletters.id')),
    Column('event_id', Integer, ForeignKey('events.id'))
)


class Subscriber(Base):
    """Subscriber model"""
    __tablename__ = 'subscribers'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    status = Column(SQLEnum(SubscriberStatus), default=SubscriberStatus.PENDING, nullable=False)
    confirmation_token = Column(String(500), nullable=True)
    confirmed_at = Column(DateTime, nullable=True)
    region = Column(String(100), nullable=True)
    preferences = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    email_logs = relationship("EmailLog", back_populates="subscriber")


class Event(Base):
    """Event model"""
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(SQLEnum(EventCategory), nullable=False)
    region = Column(String(100), nullable=True)
    start_date = Column(DateTime, nullable=False, index=True)
    end_date = Column(DateTime, nullable=True)
    venue = Column(String(200), nullable=True)
    address = Column(String(300), nullable=True)
    url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    source = Column(String(100), default="manual", nullable=False)  # manual, scraper name
    status = Column(SQLEnum(EventStatus), default=EventStatus.DRAFT, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    newsletters = relationship("Newsletter", secondary=newsletter_events, back_populates="events")


class Newsletter(Base):
    """Newsletter model"""
    __tablename__ = 'newsletters'
    
    id = Column(Integer, primary_key=True, index=True)
    edition_number = Column(Integer, nullable=True)
    subject = Column(String(200), nullable=False)
    content_html = Column(Text, nullable=True)
    send_date = Column(DateTime, nullable=True)
    status = Column(SQLEnum(NewsletterStatus), default=NewsletterStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    events = relationship("Event", secondary=newsletter_events, back_populates="newsletters")
    email_logs = relationship("EmailLog", back_populates="newsletter")


class EmailLog(Base):
    """Email log model for tracking"""
    __tablename__ = 'email_logs'
    
    id = Column(Integer, primary_key=True, index=True)
    subscriber_id = Column(Integer, ForeignKey('subscribers.id'), nullable=False)
    newsletter_id = Column(Integer, ForeignKey('newsletters.id'), nullable=True)
    sent_at = Column(DateTime, nullable=True)
    opened_at = Column(DateTime, nullable=True)
    clicked_at = Column(DateTime, nullable=True)
    bounce_type = Column(String(50), nullable=True)  # hard, soft
    error = Column(Text, nullable=True)
    status = Column(String(50), default="pending", nullable=False)  # pending, sent, failed, bounced
    
    # Relationships
    subscriber = relationship("Subscriber", back_populates="email_logs")
    newsletter = relationship("Newsletter", back_populates="email_logs")
