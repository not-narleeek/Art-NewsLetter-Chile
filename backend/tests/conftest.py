"""
Pytest configuration and fixtures for testing.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from models import Base
from database import get_db
from app import app

# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_db():
    """Create a fresh test database for each test"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with test database"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_subscriber_data():
    """Sample subscriber data for testing"""
    return {
        "email": "test@example.com",
        "region": "Santiago"
    }


@pytest.fixture
def sample_event_data():
    """Sample event data for testing"""
    from datetime import datetime, timedelta
    
    return {
        "title": "Exposición de Arte Contemporáneo",
        "description": "Una muestra de arte moderno en el GAM",
        "category": "arte",
        "region": "Santiago",
        "start_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "end_date": (datetime.now() + timedelta(days=14)).isoformat(),
        "venue": "GAM",
        "url": "https://example.com/evento"
    }
