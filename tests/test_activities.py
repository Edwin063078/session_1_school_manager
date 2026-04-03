import pytest

def test_get_activities(client):
    "Test retrieving all activities."
    # Arrange - No special setup needed
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert "Basketball" in data
    assert "Volleyball" in data
    
    # Verify structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_for_activity_success(client):
    "Test successful signup for an activity."
    # Arrange
    test_email = "test_signup_success@example.com"
    activity_name = "Basketball"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {test_email} for {activity_name}" in data["message"]
    
    # Verify the participant was added
    response = client.get("/activities")
    activities = response.json()
    assert test_email in activities[activity_name]["participants"]

def test_signup_already_signed_up(client):
    "Test signup when already signed up."
    # Arrange
    duplicate_email = "test_duplicate@example.com"
    activity_name = "Basketball"
    
    # Act - First signup
    client.post(f"/activities/{activity_name}/signup?email={duplicate_email}")
    
    # Act - Second signup should fail
    response = client.post(f"/activities/{activity_name}/signup?email={duplicate_email}")
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "is already signed up" in data["detail"]

def test_signup_invalid_activity(client):
    "Test signup for a non-existent activity."
    # Arrange
    test_email = "test_invalid@example.com"
    invalid_activity = "NonExistent"
    
    # Act & Assert - This should raise a KeyError
    with pytest.raises(KeyError):
        client.post(f"/activities/{invalid_activity}/signup?email={test_email}")

def test_unregister_from_activity_success(client):
    "Test successful unregistration from an activity."
    # Arrange
    test_email = "test_unregister_success@example.com"
    activity_name = "Volleyball"
    
    # Act - First signup
    client.post(f"/activities/{activity_name}/signup?email={test_email}")
    
    # Act - Then unregister
    response = client.delete(f"/activities/{activity_name}/unregister?email={test_email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Unregistered {test_email} from {activity_name}" in data["message"]
    
    # Verify the participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert test_email not in activities[activity_name]["participants"]

def test_unregister_not_registered(client):
    "Test unregistration when not registered."
    # Arrange
    not_registered_email = "test_not_registered@example.com"
    activity_name = "Chess Club"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={not_registered_email}")
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "is not registered" in data["detail"]

def test_unregister_invalid_activity(client):
    "Test unregistration from a non-existent activity."
    # Arrange
    test_email = "test_unregister_invalid@example.com"
    invalid_activity = "InvalidActivity"
    
    # Act
    response = client.delete(f"/activities/{invalid_activity}/unregister?email={test_email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_root_redirect(client):
    """Test root endpoint serves the static index.html."""
    # Arrange - No special setup needed
    
    # Act
    response = client.get("/")
    
    # Assert - TestClient follows redirects, so we get the HTML content
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "<!DOCTYPE html>" in response.text
    assert "Mergington High School" in response.text
