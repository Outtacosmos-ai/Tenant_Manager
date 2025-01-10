# backend/core/utils.py
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from functools import wraps

class CustomResponse:
    @staticmethod
    def success(data=None, message=None, status_code=status.HTTP_200_OK):
        response_data = {
            'status': 'success',
            'message': message,
            'data': data
        }
        return Response(response_data, status=status_code)

    @staticmethod
    def error(message=None, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        response_data = {
            'status': 'error',
            'message': message,
            'errors': errors
        }
        return Response(response_data, status=status_code)

class TenantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter queryset by tenant
        """
        queryset = super().get_queryset()
        return queryset.filter(tenant=self.request.tenant)
    
    def perform_create(self, serializer):
        """
        Add tenant to object on creation
        """
        serializer.save(tenant=self.request.tenant)

def tenant_required(f):
    """
    Decorator to ensure request has tenant
    """
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'tenant'):
            raise PermissionDenied("Tenant is required")
        return f(request, *args, **kwargs)
    return wrapper

def get_client_ip(request):
    """
    Get client IP address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Custom mixins
class TenantMixin:
    """
    Mixin to filter querysets by tenant
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(tenant=self.request.tenant)

class AuditMixin:
    """
    Mixin to add audit fields
    """
    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            tenant=self.request.tenant
        )

    def perform_update(self, serializer):
        serializer.save(
            updated_by=self.request.user
        )