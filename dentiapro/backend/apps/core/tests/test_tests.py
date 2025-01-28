import pytest
from unittest.mock import Mock
from rest_framework import status
from rest_framework.response import Response
from apps.core.utils import CustomResponse, get_client_ip

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
        Test success response with data
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

    def test_success_response_custom_status(self):
        """
        Test success response with custom status code
        """
        custom_status = status.HTTP_201_CREATED
        
        response = CustomResponse.success(
            status_code=custom_status
        )
        
        assert response.status_code == custom_status

    def test_error_response_default(self):
        """
        Test error response with default parameters
        """
        response = CustomResponse.error()
        
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'error'
        assert response.data['message'] is None
        assert response.data['errors'] is None

    def test_error_response_with_details(self):
        """
        Test error response with message and errors
        """
        test_message = 'Validation failed'
        test_errors = {
            'field': ['Invalid input']
        }
        
        response = CustomResponse.error(
            message=test_message, 
            errors=test_errors
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'error'
        assert response.data['message'] == test_message
        assert response.data['errors'] == test_errors

    def test_error_response_custom_status(self):
        """
        Test error response with custom status code
        """
        custom_status = status.HTTP_404_NOT_FOUND
        
        response = CustomResponse.error(
            status_code=custom_status
        )
        
        assert response.status_code == custom_status

class TestClientIPUtility:
    def test_get_client_ip_direct_connection(self):
        """
        Test get_client_ip for a direct connection
        """
        # Create a mock request
        request = Mock()
        request.META = {
            'REMOTE_ADDR': '192.168.1.100'
        }
        
        ip = get_client_ip(request)
        
        assert ip == '192.168.1.100'

    def test_get_client_ip_with_forwarded_for(self):
        """
        Test get_client_ip with X-Forwarded-For header
        """
        # Create a mock request with X-Forwarded-For
        request = Mock()
        request.META = {
            'HTTP_X_FORWARDED_FOR': '203.0.113.195, 70.41.3.18, 150.172.238.178'
        }
        
        ip = get_client_ip(request)
        
        assert ip == '203.0.113.195'

    def test_get_client_ip_multiple_forwarded_ips(self):
        """
        Test get_client_ip with multiple forwarded IPs
        """
        # Create a mock request with multiple forwarded IPs
        request = Mock()
        request.META = {
            'HTTP_X_FORWARDED_FOR': '10.0.0.1, 10.0.0.2, 10.0.0.3'
        }
        
        ip = get_client_ip(request)
        
        assert ip == '10.0.0.1'

    def test_get_client_ip_no_ip_available(self):
        """
        Test get_client_ip when no IP is available
        """
        # Create a mock request with empty META
        request = Mock()
        request.META = {}
        
        ip = get_client_ip(request)
        
        assert ip is None

def test_custom_response_type():
    """
    Verify that CustomResponse returns a Response object
    """
    success_response = CustomResponse.success()
    error_response = CustomResponse.error()
    
    assert isinstance(success_response, Response)
    assert isinstance(error_response, Response)

def test_custom_response_data_structure():
    """
    Verify the data structure of CustomResponse
    """
    # Success response
    success_response = CustomResponse.success(
        data={'key': 'value'}, 
        message='Test success'
    )
    assert set(success_response.data.keys()) == {'status', 'message', 'data'}
    assert success_response.data['status'] == 'success'

    # Error response
    error_response = CustomResponse.error(
        message='Test error', 
        errors={'field': ['error']}
    )
    assert set(error_response.data.keys()) == {'status', 'message', 'errors'}
    assert error_response.data['status'] == 'error'

# Parametrized tests for additional scenarios
@pytest.mark.parametrize('method,kwargs,expected_status', [
    (CustomResponse.success, {}, status.HTTP_200_OK),
    (CustomResponse.success, {'status_code': status.HTTP_201_CREATED}, status.HTTP_201_CREATED),
    (CustomResponse.error, {}, status.HTTP_400_BAD_REQUEST),
    (CustomResponse.error, {'status_code': status.HTTP_404_NOT_FOUND}, status.HTTP_404_NOT_FOUND),
])
def test_custom_response_status_codes(method, kwargs, expected_status):
    """
    Parametrized test for various status codes
    """
    response = method(**kwargs)
    assert response.status_code == expected_status