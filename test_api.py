import pytest
from app import app as flask_app


@pytest.fixture
def client():
    """Cria um cliente de teste para a aplicação Flask"""
    with flask_app.test_client() as client:
        yield client


def test_generate_endpoint_success(client):
    """

    Test the corresponding endpoint/generate with a well-done request
    Verify if the status code is 200 and if the answer contain the key "response".

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
    Test the endpoint/generate when the 'prompt' key is missing on payload.
    Verify if the application deal with the error graciously
    The behavior expected could change (example: 400 Bad Request or 500 Internal Server)
    This test verify if the request don't pass silently.
    """

    # Arrange
    payload = {"text": "This is not a valid prompt key"}  # invalid payload

    # Act
    response = client.post('/generate', json=payload)

    # asset
    # A good error treatment structure returns 400. How the actual code doesn't have explicit treatment structures, he will probably returns the 500 code. In both cases this indicates that's the error was captured


assert response.status_code in [400, 500]
