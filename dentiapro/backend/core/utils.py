# backend/core/utils.py
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from functools import wraps

class CustomResponse:
    @staticmethod
    def success(data=None, message=None, status_code=status.HTTP_200_OK):
        """
        Standard response for success.
        """
        response_data = {
            'status': 'success',
            'message': message,
            'data': data
        }
        return Response(response_data, status=status_code)

    @staticmethod
    def error(message=None, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        Standard response for error.
        """
        response_data = {
            'status': 'error',
            'message': message,
            'errors': errors
        }
        return Response(response_data, status=status_code)

class TenantViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet that filters querysets and performs actions based on the tenant context.
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter queryset by tenant to ensure multi-tenant isolation.
        """
        queryset = super().get_queryset()
        return queryset.filter(tenant=self.request.tenant)
    
    def perform_create(self, serializer):
        """
        Add tenant context to object during creation.
        """
        serializer.save(tenant=self.request.tenant)

def tenant_required(f):
    """
    Decorator to ensure that request contains tenant information.
    Raises PermissionDenied if tenant is not provided.
    """
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'tenant'):
            raise PermissionDenied("Tenant is required")
        return f(request, *args, **kwargs)
    return wrapper

def get_client_ip(request):
    """
    Get client IP address from request headers or direct connection.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Custom Mixins for multi-tenancy support

class TenantMixin:
    """
    Mixin to filter querysets based on tenant association.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(tenant=self.request.tenant)

class AuditMixin:
    """
    Mixin to automatically add audit fields to created/updated objects.
    """
    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,  # Audit: created_by
            tenant=self.request.tenant      # Audit: tenant context
        )

    def perform_update(self, serializer):
        serializer.save(
            updated_by=self.request.user   # Audit: updated_by
        )
