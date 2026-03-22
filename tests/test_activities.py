import pytest


class TestActivities:
    """Test suite for activities-related endpoints."""

    def test_math_max(self, client):
        """Check that Math Club has max 1 for testing."""
        response = client.get("/activities")
        data = response.json()
        assert data["Math Club"]["max_participants"] == 1

    def test_get_activities_success(self, client):
        """Test GET /activities returns all activities successfully."""
        # Arrange: No setup needed, activities are pre-seeded

        # Act: Make GET request to /activities
        response = client.get("/activities")

        # Assert: Check status code and response structure
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0  # Should have pre-seeded activities
        # Check structure of one activity
        activity = next(iter(data.values()))
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

    def test_signup_success(self, client):
        """Test POST /activities/{activity_name}/signup with valid data."""
        # Arrange: Use an activity that has space
        activity_name = "Programming Class"
        email = "newstudent@mergington.edu"

        # Act: Make POST request
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert: Check success
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "signed up" in data["message"].lower()

        # Verify participant was added
        get_response = client.get("/activities")
        activities = get_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_activity_not_found(self, client):
        """Test POST /activities/{activity_name}/signup for non-existent activity."""
        # Arrange
        activity_name = "NonExistentActivity"
        email = "test@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_already_signed_up(self, client):
        """Test POST /activities/{activity_name}/signup when already signed up."""
        # Arrange: Use an activity with existing participant
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in participants

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_remove_participant_success(self, client):
        """Test DELETE /activities/{activity_name}/participants/{email} success."""
        # Arrange: Use an activity with participant
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Pre-seeded

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "removed" in data["message"].lower()

        # Verify removed
        get_response = client.get("/activities")
        activities = get_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_remove_participant_activity_not_found(self, client):
        """Test DELETE for non-existent activity."""
        # Arrange
        activity_name = "NonExistent"
        email = "test@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_remove_participant_not_signed_up(self, client):
        """Test DELETE for participant not signed up."""
        # Arrange
        activity_name = "Chess Club"
        email = "notsigned@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()