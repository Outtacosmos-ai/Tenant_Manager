import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.db.models import QuerySet

# Assuming these are your actual models and serializers
from apps.cabinet.models import Cabinet
from apps.cabinet.serializers import CabinetSerializer
from apps.cabinet.views import CabinetViewSet

@pytest.mark.django_db
class TestCabinetViewSet:
    def setup_method(self):
        """
        Setup method to initialize test environment
        """
        self.client = APIClient()
        self.view = CabinetViewSet()

    def create_test_cabinets(self, tenant, num_cabinets=5):
        """
        Helper method to create test cabinets
        """
        cabinets = []
        for i in range(num_cabinets):
            cabinet = Cabinet.objects.create(
                tenant=tenant,
                name=f'Test Cabinet {i}',
                address=f'{i} Test St',
                contact_number=f'+123456789{i}',
                email=f'test{i}@cabinet.com',
                is_active=i % 2 == 0  # Alternate active status
            )
            cabinets.append(cabinet)
        return cabinets

    def test_get_queryset(self, create_tenant):
        """
        Test the default queryset
        """
        tenant = create_tenant
        
        # Create test cabinets
        cabinets = self.create_test_cabinets(tenant)

        # Simulate request
        request = type('Request', (), {'user': type('User', (), {'is_authenticated': True})()})()
        
        # Set up view with the mock request
        self.view.request = request
        self.view.kwargs = {}

        # Get the queryset
        queryset = self.view.get_queryset()

        # Assert queryset is correct
        assert isinstance(queryset, QuerySet)
        assert queryset.count() == len(cabinets)

    def test_list_cabinets(self, create_authenticated_user, create_tenant):
        """
        Test listing cabinets
        """
        # Authenticate user
        user = create_authenticated_user
        self.client.force_authenticate(user=user)

        # Create tenant and cabinets
        tenant = create_tenant
        cabinets = self.create_test_cabinets(tenant)

        # Get the list endpoint
        url = reverse('cabinet-list')
        response = self.client.get(url)

        # Assert response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(cabinets)

    def test_create_cabinet(self, create_authenticated_user, create_tenant):
        """
        Test creating a new cabinet
        """
        # Authenticate user
        user = create_authenticated_user
        self.client.force_authenticate(user=user)

        # Get tenant
        tenant = create_tenant

        # Prepare cabinet data
        cabinet_data = {
            'tenant': tenant.id,
            'name': 'New Test Cabinet',
            'address': '789 New St',
            'contact_number': '+1234567890',
            'email': 'new@cabinet.com',
            'is_active': True
        }

        # Get the create endpoint
        url = reverse('cabinet-list')
        response = self.client.post(url, cabinet_data)

        # Assert response
        assert response.status_code == status.HTTP_201_CREATED
        assert Cabinet.objects.filter(name='New Test Cabinet').exists()

    def test_retrieve_cabinet(self, create_authenticated_user, create_tenant):
        """
        Test retrieving a specific cabinet
        """
        # Authenticate user
        user = create_authenticated_user
        self.client.force_authenticate(user=user)

        # Create tenant and cabinet
        tenant = create_tenant
        cabinet = self.create_test_cabinets(tenant, num_cabinets=1)[0]

        # Get the detail endpoint
        url = reverse('cabinet-detail', kwargs={'pk': cabinet.id})
        response = self.client.get(url)

        # Assert response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == cabinet.name

    def test_update_cabinet(self, create_authenticated_user, create_tenant):
        """
        Test updating a cabinet
        """
        # Authenticate user
        user = create_authenticated_user
        self.client.force_authenticate(user=user)

        # Create tenant and cabinet
        tenant = create_tenant
        cabinet = self.create_test_cabinets(tenant, num_cabinets=1)[0]

        # Prepare update data
        update_data = {
            'name': 'Updated Cabinet Name',
            'address': '456 Updated St',
            'contact_number': '+0987654321',
            'email': 'updated@cabinet.com',
            'is_active': not cabinet.is_active
        }

        # Get the update endpoint
        url = reverse('cabinet-detail', kwargs={'pk': cabinet.id})
        response = self.client.patch(url, update_data)

        # Assert response
        assert response.status_code == status.HTTP_200_OK
        
        # Retrieve updated cabinet
        updated_cabinet = Cabinet.objects.get(id=cabinet.id)
        assert updated_cabinet.name == 'Updated Cabinet Name'
        assert updated_cabinet.is_active != cabinet.is_active

    def test_delete_cabinet(self, create_authenticated_user, create_tenant):
        """
        Test deleting a cabinet
        """
        # Authenticate user
        user = create_authenticated_user
        self.client.force_authenticate(user=user)

        # Create tenant and cabinet
        tenant = create_tenant
        cabinet = self.create_test_cabinets(tenant, num_cabinets=1)[0]

        # Get the delete endpoint
        url = reverse('cabinet-detail', kwargs={'pk': cabinet.id})
        response = self.client.delete(url)

        # Assert response
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Cabinet.objects.filter(id=cabinet.id).exists()

    def test_cabinet_filtering(self, create_authenticated_user, create_tenant):
        """
        Test filtering cabinets
        """
        # Authenticate user
        user = create_authenticated_user
        self.client.force_authenticate(user=user)

        # Create tenant and cabinets
        tenant = create_tenant
        self.create_test_cabinets(tenant)

        # Test filtering by tenant
        url = reverse('cabinet-list')
        response = self.client.get(url, {'tenant': tenant.id})
        assert response.status_code == status.HTTP_200_OK
        assert all(item['tenant'] == tenant.id for item in response.data)

        # Test filtering by is_active
        response = self.client.get(url, {'is_active': 'true'})
        assert response.status_code == status.HTTP_200_OK
        assert all(item['is_active'] is True for item in response.data)

    def test_unauthorized_access(self):
        """
        Test unauthorized access to cabinet endpoints
        """
        # Create URLs for different actions
        list_url = reverse('cabinet-list')
        detail_url = reverse('cabinet-detail', kwargs={'pk': 1})

        # Test list view
        response = self.client.get(list_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Test detail view
        response = self.client.get(detail_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

# Fixtures for creating test data
@pytest.fixture
def create_tenant():
    """
    Fixture to create a tenant for testing
    """
    from apps.tenant.models import Tenant
    return Tenant.objects.create(
        name="Test Tenant",
        domain_url="test.com"
    )

@pytest.fixture
def create_authenticated_user(django_user_model):
    """
    Fixture to create an authenticated user
    """
    user = django_user_model.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    return user