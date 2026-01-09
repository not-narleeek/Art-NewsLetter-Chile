"""
Tests for database models.
"""
import pytest
from datetime import datetime, timedelta
from models import Subscriber, Event, Newsletter, SubscriberStatus, EventStatus, EventCategory


def test_create_subscriber(test_db):
    """Test creating a subscriber"""
    subscriber = Subscriber(
        email="test@example.com",
        status=SubscriberStatus.PENDING,
        confirmation_token="test_token"
    )
    
    test_db.add(subscriber)
    test_db.commit()
    
    assert subscriber.id is not None
    assert subscriber.email == "test@example.com"
    assert subscriber.status == SubscriberStatus.PENDING


def test_subscriber_unique_email(test_db):
    """Test that email must be unique"""
    subscriber1 = Subscriber(email="test@example.com", status=SubscriberStatus.ACTIVE)
    test_db.add(subscriber1)
    test_db.commit()
    
    # Try to add another with same email
    subscriber2 = Subscriber(email="test@example.com", status=SubscriberStatus.ACTIVE)
    test_db.add(subscriber2)
    
    with pytest.raises(Exception):  # Should raise integrity error
        test_db.commit()


def test_create_event(test_db):
    """Test creating an event"""
    event = Event(
        title="Test Event",
        description="Test description",
        category=EventCategory.ARTE,
        start_date=datetime.now() + timedelta(days=7),
        status=EventStatus.PUBLISHED
    )
    
    test_db.add(event)
    test_db.commit()
    
    assert event.id is not None
    assert event.title == "Test Event"
    assert event.category == EventCategory.ARTE


def test_event_date_validation(test_db):
    """Test event dates are stored correctly"""
    start = datetime.now() + timedelta(days=7)
    end = datetime.now() + timedelta(days=14)
    
    event = Event(
        title="Test Event",
        category=EventCategory.MUSICA,
        start_date=start,
        end_date=end,
        status=EventStatus.PUBLISHED
    )
    
    test_db.add(event)
    test_db.commit()
    
    assert event.start_date == start
    assert event.end_date == end


def test_create_newsletter(test_db):
    """Test creating a newsletter"""
    newsletter = Newsletter(
        subject="Test Newsletter",
        status=NewsletterStatus.DRAFT
    )
    
    test_db.add(newsletter)
    test_db.commit()
    
    assert newsletter.id is not None
    assert newsletter.subject == "Test Newsletter"
