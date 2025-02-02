# tests/test_inventory_views.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.inventory.models import Category, InventoryItem
from apps.inventory.serializers import CategorySerializer, InventoryItemSerializer
from backend.apps.tenant.models import Tenant

@pytest.mark.django_db
def test_inventory_item_list_view():
    # Create a test client
    client = APIClient()

    # Create a Tenant instance (assuming Tenant model exists)
    tenant = Tenant.objects.create(name='Test Tenant', description='Test Description')

    # Create a Category instance
    category = Category.objects.create(tenant=tenant, name='Dental Tools', description='Tools used in dental procedures')

    # Create an InventoryItem instance
    InventoryItem.objects.create(
        tenant=tenant,
        category=category,
        name='Dental Mirror',
        description='Test Description',
        quantity=100,
        unit='pieces',
        minimum_quantity=5,
        cost_price=9.99
    )

    # Simulate a request with the tenant in the context
    client.force_authenticate(user=None)  # Assuming no user authentication is required
    url = reverse('inventory-item-list')
    response = client.get(url, HTTP_TENANT_ID=tenant.id)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == status.HTTP_200_OK

    # Assert that the response data matches the serialized data
    items = InventoryItem.objects.filter(tenant=tenant).select_related('category')
    serializer = InventoryItemSerializer(items, many=True)
    assert response.data == serializer.data

@pytest.mark.django_db
def test_inventory_item_create_view():
    # Create a test client
    client = APIClient()

    # Create a Tenant instance
    tenant = Tenant.objects.create(name='Test Tenant', description='Test Description')

    # Create a Category instance
    category = Category.objects.create(tenant=tenant, name='Dental Tools', description='Tools used in dental procedures')

    # Data for creating an InventoryItem instance
    item_data = {
        "name": "Dental Mirror",
        "category": category.id,
        "description": "Test Description",
        "quantity": 100,
        "unit": "pieces",
        "minimum_quantity": 5,
        "cost_price": 9.99
    }

    # Simulate a request with the tenant in the context
    client.force_authenticate(user=None)  # Assuming no user authentication is required
    url = reverse('inventory-item-list')
    response = client.post(url, data=item_data, HTTP_TENANT_ID=tenant.id, format='json')

    # Assert that the response status code is 201 (Created)
    assert response.status_code == status.HTTP_201_CREATED

    # Assert that the InventoryItem was created with the correct tenant
    item = InventoryItem.objects.get(id=response.data['id'])
    assert item.tenant == tenant

@pytest.mark.django_db
def test_category_list_view():
    # Create a test client
    client = APIClient()

    # Create a Tenant instance
    tenant = Tenant.objects.create(name='Test Tenant', description='Test Description')

    # Create a Category instance
    Category.objects.create(tenant=tenant, name='Dental Tools', description='Tools used in dental procedures')

    # Simulate a request with the tenant in the context
    client.force_authenticate(user=None)  # Assuming no user authentication is required
    url = reverse('category-list')
    response = client.get(url, HTTP_TENANT_ID=tenant.id)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == status.HTTP_200_OK

    # Assert that the response data matches the serialized data
    categories = Category.objects.filter(tenant=tenant)
    serializer = CategorySerializer(categories, many=True)
    assert response.data == serializer.data

@pytest.mark.django_db
def test_category_create_view():
    # Create a test client
    client = APIClient()

    # Create a Tenant instance
    tenant = Tenant.objects.create(name='Test Tenant', description='Test Description')

    # Data for creating a Category instance
    category_data = {
        "name": "Dental Tools",
        "description": "Tools used in dental procedures"
    }

    # Simulate a request with the tenant in the context
    client.force_authenticate(user=None)  # Assuming no user authentication is required
    url = reverse('category-list')
    response = client.post(url, data=category_data, HTTP_TENANT_ID=tenant.id, format='json')

    # Assert that the response status code is 201 (Created)
    assert response.status_code == status.HTTP_201_CREATED

    # Assert that the Category was created with the correct tenant
    category = Category.objects.get(id=response.data['id'])
    assert category.tenant == tenant