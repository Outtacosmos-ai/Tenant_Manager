from rest_framework import viewsets, permissions
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from core.utils import TenantViewSet


class MedicalRecordViewSet(TenantViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by roles
        if self.request.user.role == 'patient':
            return queryset.filter(patient=self.request.user)
        elif self.request.user.role == 'dentist':
            return queryset.filter(dentist=self.request.user)

        # Allow tenant admin to view all
        if self.request.user.is_tenant_admin:
            return queryset

        return queryset.none()

    def perform_create(self, serializer):
        """Set tenant and validate roles during creation"""
        serializer.save(tenant=self.request.user.tenant)
