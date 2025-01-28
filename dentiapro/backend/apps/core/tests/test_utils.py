import pytest
from unittest.mock import Mock, patch
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.test import RequestFactory

# Import the utilities to test
from apps.core.utils import (
    CustomResponse, 
    TenantViewSet, 
    tenant_required, 
    get_client_ip,
    TenantMixin,
    AuditMixin
)

class TestCustomResponse:
    def test_success_response_default(self):
        """
        Test success response with default parameters
        """
        response = CustomResponse.success()
        
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'success'
        assert response.data['message'] is None
        assert response.data['data'] is None

    def test_success_response_with_data(self):
        """
        Test success response with data and message
        """
        test_data = {'key': 'value'}
        test_message = 'Operation successful'
        
        response = CustomResponse.success(
            data=test_data, 
            message=test_message
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'success'
        assert response.data['message'] == test_message
        assert response.data['data'] == test_data

    def test_error_response(self):
        """
        Test error response
        """
        test_message = 'Validation error'
        test_errors = {'field': ['Invalid input']}
        
        response = CustomResponse.error(
            message=test_message,
            errors=test_errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
        
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'error'
        assert response.data['message'] == test_message
        assert response.data['errors'] == test_errors

class TestTenantViewSet:
    def setup_method(self):
        """
        Setup method for TenantViewSet tests
        """
        self.view = TenantViewSet()
        self.request_factory = RequestFactory()

    def test_tenant_viewset_queryset_filtering(self):
        """
        Test queryset filtering by tenant
        """
        # Create a mock request with tenant
        mock_tenant = Mock()
        request = self.request_factory.get('/test')
        request.tenant = mock_tenant
        request.user = Mock(is_authenticated=True)

        # Mock the super().get_queryset() method
        with patch.object(self.view, 'get_queryset', return_value=Mock()) as mock_get_queryset:
            self.view.request = request
            filtered_queryset = self.view.get_queryset()

            # Verify queryset was filtered by tenant
            mock_get_queryset.return_value.filter.assert_called_once_with(tenant=mock_tenant)

    def test_tenant_viewset_perform_create(self):
        """
        Test perform_create method adds tenant context
        """
        # Create a mock request with tenant
        mock_tenant = Mock()
        request = self.request_factory.get('/test')
        request.tenant = mock_tenant
        request.user = Mock(is_authenticated=True)

        # Mock serializer
        mock_serializer = Mock()

        # Set request on view
        self.view.request = request

        # Call perform_create
        self.view.perform_create(mock_serializer)

        # Verify tenant was added during save
        mock_serializer.save.assert_called_once_with(tenant=mock_tenant)

class TestTenantRequired:
    def test_tenant_required_decorator(self):
        """
        Test tenant_required decorator
        """
        # Create a mock request without tenant
        request_without_tenant = Mock()
        request_without_tenant.tenant = None

        # Create a mock function
        @tenant_required
        def test_function(request):
            return "Function called"

        # Test that PermissionDenied is raised
        with pytest.raises(PermissionDenied, match="Tenant is required"):
            test_function(request_without_tenant)

    def test_tenant_required_decorator_with_tenant(self):
        """
        Test tenant_required decorator with tenant present
        """
        # Create a mock request with tenant
        request_with_tenant = Mock()
        request_with_tenant.tenant = Mock()

        # Create a mock function
        @tenant_required
        def test_function(request):
            return "Function called"

        # Test that function is called
        result = test_function(request_with_tenant)
        assert result == "Function called"

class TestClientIP:
    def test_get_client_ip_direct(self):
        """
        Test get_client_ip for direct connection
        """
        request = Mock()
        request.META = {'REMOTE_ADDR': '192.168.1.1'}
        
        ip = get_client_ip(request)
        assert ip == '192.168.1.1'

    def test_get_client_ip_forwarded(self):
        """
        Test get_client_ip with X-Forwarded-For
        """
        request = Mock()
        request.META = {
            'HTTP_X_FORWARDED_FOR': '203.0.113.195, 70.41.3.18'
        }
        
        ip = get_client_ip(request)
        assert ip == '203.0.113.195'

class TestTenantMixin:
    def test_tenant_mixin_queryset_filtering(self):
        """
        Test TenantMixin queryset filtering
        """
        class TestViewSet(TenantMixin, Mock):
            def get_queryset(self):
                return super().get_queryset()

        # Create mock objects
        mock_queryset = Mock()
        mock_request = Mock()
        mock_tenant = Mock()

        # Setup the view
        view = TestViewSet()
        view.request = mock_request
        view.request.tenant = mock_tenant

        # Mock the super().get_queryset() method
        with patch.object(view, 'get_queryset', return_value=mock_queryset) as mock_method:
            filtered_queryset = view.get_queryset()
            
            # Verify queryset was filtered by tenant
            mock_queryset.filter.assert_called_once_with(tenant=mock_tenant)

class TestAuditMixin:
    def test_audit_mixin_create(self):
        """
        Test AuditMixin perform_create
        """
        class TestViewSet(AuditMixin, Mock):
            def perform_create(self, serializer):
                super().perform_create(serializer)

        # Create mock objects
        mock_serializer = Mock()
        mock_request = Mock()
        mock_tenant = Mock()
        mock_user = Mock()

        # Setup the view
        view = TestViewSet()
        view.request = mock_request
        view.request.tenant = mock_tenant
        view.request.user = mock_user

        # Call perform_create
        view.perform_create(mock_serializer)

        # Verify serializer save was called with correct arguments
        mock_serializer.save.assert_called_once_with(
            created_by=mock_user,
            tenant=mock_tenant
        )

    def test_audit_mixin_update(self):
        """
        Test AuditMixin perform_update
        """
        class TestViewSet(AuditMixin, Mock):
            def perform_update(self, serializer):
                super().perform_update(serializer)

        # Create mock objects
        mock_serializer = Mock()
        mock_request = Mock()
        mock_user = Mock()

        # Setup the view
        view = TestViewSet()
        view.request = mock_request
        view.request.user = mock_user

        # Call perform_update
        view.perform_update(mock_serializer)

        # Verify serializer save was called with correct arguments
        mock_serializer.save.assert_called_once_with(
            updated_by=mock_user
        )