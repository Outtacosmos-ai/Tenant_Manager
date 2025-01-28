import pytest
from django.urls import reverse, resolve
from rest_framework.test import APIClient
from apps.cabinet.views import CabinetViewSet

@pytest.mark.django_d
class TestCabinetUrls:
    def setup_method(self):
        """
        Setup method to initialize test environment
        """
        self.client = APIClient()

    def test_cabinet_list_url(self):
        """
        Test the cabinet list URL
        """
        # Generate the URL for the cabinet list
        url = reverse('cabinet-list')
        
        # Verify the URL
        assert url == '/cabinets/'

        # Resolve the URL
        resolver_match = resolve(url)
        
        # Check if the resolved view is the correct viewset
        assert resolver_match.func.cls == CabinetViewSet
        assert resolver_match.view_name == 'cabinet-list'

    def test_cabinet_detail_url(self):
        """
        Test the cabinet detail URL
        """
        # Generate the URL for a specific cabinet
        cabinet_id = 1
        url = reverse('cabinet-detail', kwargs={'pk': cabinet_id})
        
        # Verify the URL
        assert url == f'/cabinets/{cabinet_id}/'

        # Resolve the URL
        resolver_match = resolve(url)
        
        # Check if the resolved view is the correct viewset
        assert resolver_match.func.cls == CabinetViewSet
        assert resolver_match.view_name == 'cabinet-detail'

    def test_cabinet_url_actions(self):
        """
        Test additional URL actions for CabinetViewSet
        """
        # List of expected actions
        expected_actions = [
            'list',
            'create',
            'retrieve',
            'update',
            'partial_update',
            'destroy'
        ]

        # Test each action
        for action in expected_actions:
            # Generate the URL based on the action
            if action in ['list', 'create']:
                url = reverse(f'cabinet-{action}')
            else:
                url = reverse(f'cabinet-{action}', kwargs={'pk': 1})
            
            # Resolve the URL
            resolver_match = resolve(url)
            
            # Check if the resolved view is the correct viewset
            assert resolver_match.func.cls == CabinetViewSet
            assert resolver_match.view_name == f'cabinet-{action}'

    def test_cabinet_url_methods(self, create_cabinet):
        """
        Test URL methods for different HTTP verbs
        """
        # Create a test cabinet
        cabinet = create_cabinet
        
        # Test GET methods
        list_url = reverse('cabinet-list')
        detail_url = reverse('cabinet-detail', kwargs={'pk': cabinet.id})

        # List view GET
        response = self.client.get(list_url)
        assert response.status_code in [200, 401, 403]  # Depending on authentication

        # Detail view GET
        response = self.client.get(detail_url)
        assert response.status_code in [200, 401, 403]

    def test_cabinet_url_permissions(self, create_authenticated_user, create_cabinet):
        """
        Test URL access with different user permissions
        """
        # Authenticate the user
        user = create_authenticated_user
        self.client.force_authenticate(user=user)

        # Create a test cabinet
        cabinet = create_cabinet

        # URLs to test
        urls_to_test = [
            ('cabinet-list', None),
            ('cabinet-detail', {'pk': cabinet.id})
        ]

        for url_name, kwargs in urls_to_test:
            # Generate the URL
            url = reverse(url_name, kwargs=kwargs) if kwargs else reverse(url_name)

            # Test GET method
            response = self.client.get(url)
            assert response.status_code in [200, 403]

            # Test POST method (for list URL)
            if url_name == 'cabinet-list':
                response = self.client.post(url, {})
                assert response.status_code in [201, 400, 403]

            # Test PUT/PATCH method (for detail URL)
            if url_name == 'cabinet-detail':
                response = self.client.patch(url, {})
                assert response.status_code in [200, 400, 403]

    def test_router_registration(self):
        """
        Test router registration for CabinetViewSet
        """
        from rest_framework.routers import DefaultRouter
        from apps.cabinet.urls import router

        # Verify router registration
        registered_viewsets = [
            viewset.__name__ for viewset in router.registry
        ]

        assert 'CabinetViewSet' in [viewset.__name__ for viewset in router.registry]
        assert len(router.registry) > 0

# Fixtures for testing
@pytest.fixture
def create_cabinet(create_tenant):
    """
    Fixture to create a test cabinet
    """
    from apps.cabinet.models import Cabinet
    
    return Cabinet.objects.create(
        tenant=create_tenant,
        name='Test Cabinet',
        address='123 Test St',
        contact_number='+1234567890',
        email='test@cabinet.com'
    )

@pytest.fixture
def create_tenant():
    """
    Fixture to create a test tenant
    """
    from apps.tenant.models import Tenant
    
    return Tenant.objects.create(
        name='Test Tenant',
        domain_url='test.com'
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