import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    
    # Check that each activity has required fields
    for name, details in data.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)


def test_signup_for_activity():
    """Test signing up for an activity"""
    # Use an activity with available spots
    response = client.post("/activities/Basketball%20Team/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "test@mergington.edu" in data["message"]
    assert "Basketball Team" in data["message"]


def test_signup_already_signed_up():
    """Test signing up when already signed up"""
    # First signup
    client.post("/activities/Soccer%20Club/signup?email=duplicate@mergington.edu")
    
    # Try again
    response = client.post("/activities/Soccer%20Club/signup?email=duplicate@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_activity_not_found():
    """Test signing up for non-existent activity"""
    response = client.post("/activities/NonExistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_from_activity():
    """Test unregistering from an activity"""
    # First signup
    client.post("/activities/Art%20Club/signup?email=unregister@mergington.edu")
    
    # Then unregister
    response = client.delete("/activities/Art%20Club/signup?email=unregister@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]


def test_unregister_not_signed_up():
    """Test unregistering when not signed up"""
    response = client.delete("/activities/Drama%20Club/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]


def test_unregister_activity_not_found():
    """Test unregistering from non-existent activity"""
    response = client.delete("/activities/NonExistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_root_redirect():
    """Test root endpoint redirects to static page"""
    response = client.get("/")
    assert response.status_code == 200  # RedirectResponse, but TestClient follows redirects
    # Since it redirects to /static/index.html, and static is mounted, it should work