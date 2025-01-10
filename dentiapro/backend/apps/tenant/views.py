from rest_framework import viewsets, permissions
from .models import Tenant, Domain
from .serializers import TenantSerializer, DomainSerializer
from core.utils import TenantViewSet

class TenantViewSet(viewsets.ModelViewSet):
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return a list of tenants based on user permissions.
        Superusers can see all tenants.
        Regular users can only see their assigned tenant.
        """
        if self.request.user.is_superuser:
            return Tenant.objects.all()
        return Tenant.objects.filter(id=self.request.tenant.id)

class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [permissions.IsAdminUser]
