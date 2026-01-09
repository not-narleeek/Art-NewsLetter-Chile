"""
Tests for API endpoints.
"""
import pytest


def test_subscribe_endpoint(client, sample_subscriber_data):
    """Test subscribing a new user"""
    response = client.post("/api/subscribe", json=sample_subscriber_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending_confirmation"
    assert "correo" in data["message"].lower()


def test_subscribe_duplicate(client, sample_subscriber_data):
    """Test subscribing with duplicate email"""
    # First subscription
    client.post("/api/subscribe", json=sample_subscriber_data)
    
    # Second subscription with same email
    response = client.post("/api/subscribe", json=sample_subscriber_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["already_subscribed", "resent"]


def test_create_event(client, sample_event_data):
    """Test creating an event"""
    response = client.post("/api/events", json=sample_event_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["message"] == "Evento creado"


def test_get_events(client, sample_event_data):
    """Test getting events list"""
    # Create an event first
    client.post("/api/events", json=sample_event_data)
    
    # Get events
    response = client.get("/api/events")
    
    assert response.status_code == 200
    data = response.json()
    assert "events" in data
    assert len(data["events"]) > 0


def test_get_single_event(client, sample_event_data):
    """Test getting a single event"""
    # Create event
    create_response = client.post("/api/events", json=sample_event_data)
    event_id = create_response.json()["id"]
    
    # Get event
    response = client.get(f"/api/events/{event_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == sample_event_data["title"]


def test_delete_event(client, sample_event_data):
    """Test deleting an event"""
    # Create event
    create_response = client.post("/api/events", json=sample_event_data)
    event_id = create_response.json()["id"]
    
    # Delete event
    response = client.delete(f"/api/events/{event_id}")
    
    assert response.status_code == 200
    assert "archivado" in response.json()["message"].lower()


def test_get_stats(client):
    """Test getting statistics"""
    response = client.get("/api/stats")
    
    assert response.status_code == 200
    data = response.json()
    assert "total_subscribers" in data
    assert "active_subscribers" in data
    assert "total_events" in data


def test_newsletter_preview(client, sample_event_data):
    """Test newsletter preview"""
    # Create some events
    client.post("/api/events", json=sample_event_data)
    
    response = client.get("/api/newsletter/preview")
    
    assert response.status_code == 200
    data = response.json()
    assert "events" in data
    assert "count" in data
