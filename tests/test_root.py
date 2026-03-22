import pytest


class TestRoot:
    """Test suite for root endpoint."""

    def test_get_root_redirect(self, client):
        """Test GET / redirects to /static/index.html."""
        # Arrange: No setup needed

        # Act: Make GET request to /
        response = client.get("/", follow_redirects=False)  # Don't follow redirect

        # Assert: Check redirect status and location
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"