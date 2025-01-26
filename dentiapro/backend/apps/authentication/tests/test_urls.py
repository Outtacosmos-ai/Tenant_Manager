import pytest
from django.test import Client

@pytest.fixture
def client():
    return Client()

def test_index_view(client):
    response = client.get('/api')
    assert response.status_code == 200
    # Add more assertions to check the response content if needed

def test_auth_api_view(client):
    response = client.get('/api-auth/')
    assert response.status_code == 200
    # Add more assertions to check the response content if needed

# Add more test cases for other URLs if needed
