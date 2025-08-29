import os
import pytest
os.environ.setdefault("FAKE_MODEL", "1")  # Ensure tests don't download weights

from app import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_generate_endpoint_success(client):
    payload = {"prompt": "Hello world"}
    response = client.post('/generate', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
    assert isinstance(data['response'], str)

def test_generate_endpoint_missing_prompt(client):
    payload = {"text": "Invalid key"}
    response = client.post('/generate', json=payload)
    assert response.status_code == 400
