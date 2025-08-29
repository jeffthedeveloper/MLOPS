import pytest
from app import app as flask_app


@pytest.fixture
def client():
    """Creates a test client for the Flask application."""
    with flask_app.test_client() as client:
        yield client


def test_generate_endpoint_success(client):
    """
    Tests the /generate endpoint with a successful request.
    Verifies that the status code is 200 and the response contains the 'response' key.
    """
    # Arrange
    payload = {"prompt": "Hello world"}

    # Act
    response = client.post('/generate', json=payload)

    # Assert
    assert response.status_code == 200
    response_data = response.get_json()
    assert 'response' in response_data
    assert isinstance(response_data['response'], str)


def test_generate_endpoint_missing_prompt(client):
    """
    Tests the /generate endpoint when the 'prompt' key is missing in the payload.
    Verifies that the application handles the error gracefully.
    """
    # Arrange
    payload = {"text": "This is not a valid prompt key"}  # Invalid payload

    # Act
    response = client.post('/generate', json=payload)

    # Assert
    # A robust error handling should return 400. Since the current code
    # has an explicit check, we expect 400.
    assert response.status_code == 400
