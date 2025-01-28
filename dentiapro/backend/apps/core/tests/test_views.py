import pytest
from django.test import RequestFactory
from django.conf import settings
from django.http import JsonResponse
from rest_framework.test import APIClient
from rest_framework import status

# Import the views to test
from apps.core.views import health_check, version_info

@pytest.mark.django_db
class TestCoreViews:
    def setup_method(self):
        """
        Setup method to initialize test environment
        """
        self.client = APIClient()
        self.request_factory = RequestFactory()

    def test_health_check_view(self):
        """
        Test health check endpoint
        """
        # Create a GET request
        request = self.request_factory.get('/health/')

        # Call the view
        response = health_check(request)

        # Assertions
        assert isinstance(response, JsonResponse)
        assert response.status_code == 200
        
        # Parse the JSON response
        data = response.json()
        
        # Verify response structure
        assert 'status' in data
        assert 'environment' in data
        assert data['status'] == 'ok'
        assert data['environment'] == settings.ENVIRONMENT

    def test_health_check_via_client(self):
        """
        Test health check endpoint using APIClient
        """
        # Make a GET request to the health check endpoint
        response = self.client.get('/health/')

        # Assertions
        assert response.status_code == 200
        assert response.json()['status'] == 'ok'
        assert response.json()['environment'] == settings.ENVIRONMENT

    def test_version_info_view(self):
        """
        Test version info endpoint
        """
        # Create a GET request
        request = self.request_factory.get('/version/')

        # Call the view
        response = version_info(request)

        # Assertions
        assert isinstance(response, JsonResponse)
        assert response.status_code == 200
        
        # Parse the JSON response
        data = response.json()
        
        # Verify response structure and content
        expected_keys = ['app_name', 'version', 'description']
        for key in expected_keys:
            assert key in data

        # Specific assertions about version info
        assert data['app_name'] == 'Dentiapro'
        assert data['version'] == '1.0.0'
        assert data['description'] == 'Multi-tenant Dental Management Application'

    def test_version_info_via_client(self):
        """
        Test version info endpoint using APIClient
        """
        # Make a GET request to the version info endpoint
        response = self.client.get('/version/')

        # Assertions
        assert response.status_code == 200
        
        data = response.json()
        assert data['app_name'] == 'Dentiapro'
        assert data['version'] == '1.0.0'

    def test_views_allow_any_permission(self):
        """
        Test that views are accessible without authentication
        """
        # Endpoints to test
        endpoints = [
            '/health/',
            '/version/'
        ]

        # Test each endpoint
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            assert response.status_code == 200, f"Failed for {endpoint}"

    @pytest.mark.parametrize('endpoint,view_func', [
        ('/health/', health_check),
        ('/version/', version_info)
    ])
    def test_view_method_restrictions(self, endpoint, view_func):
        """
        Test that views only accept GET method
        """
        # Test POST method
        request = self.request_factory.post(endpoint)
        with pytest.raises(Exception):
            view_func(request)

        # Test PUT method
        request = self.request_factory.put(endpoint)
        with pytest.raises(Exception):
            view_func(request)

        # Test DELETE method
        request = self.request_factory.delete(endpoint)
        with pytest.raises(Exception):
            view_func(request)

def test_environment_configuration():
    """
    Verify that environment is properly configured
    """
    # Check that ENVIRONMENT is set in settings
    assert hasattr(settings, 'ENVIRONMENT')
    assert settings.ENVIRONMENT is not None
    assert isinstance(settings.ENVIRONMENT, str)

# Optional: Parametrized test for version info variations
@pytest.mark.parametrize('version,description', [
    ('1.0.0', 'Multi-tenant Dental Management Application'),
    # Add more test cases if version info might change
])
def test_version_info_variations(version, description):
    """
    Parametrized test for version info
    """
    # Create a request
    request_factory = RequestFactory()
    request = request_factory.get('/version/')

    # Call the view
    response = version_info(request)

    # Parse the JSON response
    data = response.json()

    # Verify version and description
    assert data['version'] == version
    assert data['description'] == description

# Fixture for testing views (if needed)
@pytest.fixture
def api_client():
    """
    Fixture to provide an APIClient
    """
    return APIClient()