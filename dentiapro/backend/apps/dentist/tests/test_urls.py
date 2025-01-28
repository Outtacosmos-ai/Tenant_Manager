import pytest
from django.urls import reverse, resolve
from rest_framework.test import APIClient
from apps.dentist.views import DentistViewSet, SpecializationViewSet

@pytest.mark.django_db
class TestDentistUrls:
    def setup_method(self):
        """
        Setup method to initialize test environment
        """
        self.client = APIClient()

    def test_dentist_list_url(self):
        """
        Test the dentist list URL
        """
        # Generate the URL for the dentist list
        url = reverse('dentist-list')
        
        # Verify the URL
        assert url == '/dentists/'

        # Resolve the URL
        resolver_match = resolve(url)
        
        # Check if the resolved view is the correct viewset
        assert resolver_match.func.cls == DentistViewSet
        assert resolver_match.view_name == 'dentist-list'

    def test_dentist_detail_url(self):
        """
        Test the dentist detail URL
        """
        # Generate the URL for a specific dentist
        dentist_id = 1
        url = reverse('dentist-detail', kwargs={'pk': dentist_id})
        
        # Verify the URL
        assert url == f'/dentists/{dentist_id}/'

        # Resolve the URL
        resolver_match = resolve(url)
        
        # Check if the resolved view is the correct viewset
        assert resolver_match.func.cls == DentistViewSet
        assert resolver_match.view_name == 'dentist-detail'

    def test_specialization_list_url(self):
        """
        Test the specialization list URL
        """
        # Generate the URL for the specialization list
        url = reverse('specialization-list')
        
        # Verify the URL
        assert url == '/specializations/'

        # Resolve the URL
        resolver_match = resolve(url)
        
        # Check if the resolved view is the correct viewset
        assert resolver_match.func.cls == SpecializationViewSet
        assert resolver_match.view_name == 'specialization-list'

    def test_specialization_detail_url(self):
        """
        Test the specialization detail URL
        """
        # Generate the URL for a specific specialization
        specialization_id = 1
        url = reverse('specialization-detail', kwargs={'pk': specialization_id})
        
        # Verify the URL
        assert url == f'/specializations/{specialization_id}/'

        # Resolve the URL
        resolver_match = resolve(url)
        
        # Check if the resolved view is the correct viewset
        assert resolver_match.func.cls == SpecializationViewSet
        assert resolver_match.view_name == 'specialization-detail'

    def test_dentist_url_actions(self):
        """
        Test additional URL actions for DentistViewSet
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
                url = reverse(f'dentist-{action}')
            else:
                url = reverse(f'dentist-{action}', kwargs={'pk': 1})
            
            # Resolve the URL
            resolver_match = resolve(url)
            
            # Check if the resolved view is the correct viewset
            assert resolver_match.func.cls == DentistViewSet
            assert resolver_match.view_name == f'dentist-{action}'

    def test_specialization_url_actions(self):
        """
        Test additional URL actions for SpecializationViewSet
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
                url = reverse(f'specialization-{action}')
            else:
                url = reverse(f'specialization-{action}', kwargs={'pk': 1})
            
            # Resolve the URL
            resolver_match = resolve(url)
            
            # Check if the resolved view is the correct viewset
            assert resolver_match.func.cls == SpecializationViewSet
            assert resolver_match.view_name == f'specialization-{action}'

    def test_url_method_restrictions(self):
        """
        Test URL method restrictions
        """
        # URLs to test
        urls_to_test = [
            ('dentist-list', None),
            ('dentist-detail', {'pk': 1}),
            ('specialization-list', None),
            ('specialization-detail', {'pk': 1})
        ]

        for url_name, kwargs in urls_to_test:
            # Generate the URL
            url = reverse(url_name, kwargs=kwargs) if kwargs else reverse(url_name)

            # Test GET method
            response = self.client.get(url)
            assert response.status_code in [200, 401, 403]

            # Test POST method (for list URLs)
            if 'list' in url_name:
                response = self.client.post(url, {})
                assert response.status_code in [201, 400, 401, 403]

            # Test PUT/PATCH method (for detail URLs)
            if 'detail' in url_name:
                response = self.client.patch(url, {})
                assert response.status_code in [200, 400, 401, 403]

    def test_router_registration(self):
        """
        Test router registration for ViewSets
        """
        from rest_framework.routers import DefaultRouter
        from apps.dentist.urls import router

        # Verify router registration
        registered_viewsets = [
            viewset.__name__ for viewset in router.registry
        ]

        assert 'DentistViewSet' in registered_viewsets
        assert 'SpecializationViewSet' in registered_viewsets
        assert len(router.registry) == 2

# Fixtures for testing (if needed)
@pytest.fixture
def authenticated_client(django_user_model):
    """
    Fixture to create an authenticated client
    """
    client = APIClient()
    user = django_user_model.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    client.force_authenticate(user=user)
    return client