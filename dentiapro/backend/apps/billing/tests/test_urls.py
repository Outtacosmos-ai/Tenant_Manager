from django.test import Client
import pytest

@pytest.fixture
def client():
    return Client()

def test_billing_urls(client):
    response = client.get('/api/billing/')  
    assert response.status_code == 200 
    
    
