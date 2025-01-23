from rest_framework import viewsets, permissions
from .models import Tenant, Domain
from .serializers import TenantSerializer, DomainSerializer
from core.utils import TenantViewSet
from rest_framework.pagination import PageNumberPagination

class TenantViewSet(viewsets.ModelViewSet):
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Tenant.objects.all()
        return Tenant.objects.filter(id=self.request.tenant.id)

class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['tenant', 'is_primary']  # Added filtering capabilities