# tests/test_inventory_urls.py
import decimal
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.inventory.models import Category, InventoryItem

@pytest.mark.django_db
def test_inventory_item_list_url():
    # Create a test client
    client = APIClient()

    # Get the URL for the InventoryItem list view
    url = reverse('inventory-item-list')

    # Send a GET request to the URL
    response = client.get(url)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

@pytest.mark.django_db
def test_inventory_item_detail_url():
    # Create a test client
    client = APIClient()

    # Create a Category instance
    category = Category.objects.create(name='Dental Tools', description='Tools used in dental procedures')

    # Create an InventoryItem instance
    item = InventoryItem.objects.create(
        name='Dental Mirror',
        category=category,
        quantity=100,
        unit_price=decimal('5.99'),
        reorder_level=20
    )

    # Get the URL for the InventoryItem detail view
    url = reverse('inventory-item-detail', args=[item.id])

    # Send a GET request to the URL
    response = client.get(url)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    assert response.data['name'] == 'Dental Mirror'

@pytest.mark.django_db
def test_category_list_url():
    # Create a test client
    client = APIClient()

    # Get the URL for the Category list view
    url = reverse('category-list')

    # Send a GET request to the URL
    response = client.get(url)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

@pytest.mark.django_db
def test_category_detail_url():
    # Create a test client
    client = APIClient()

    # Create a Category instance
    category = Category.objects.create(name='Dental Tools', description='Tools used in dental procedures')

    # Get the URL for the Category detail view
    url = reverse('category-detail', args=[category.id])

    # Send a GET request to the URL
    response = client.get(url)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    assert response.data['name'] == 'Dental Tools'