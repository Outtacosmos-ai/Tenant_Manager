from rest_framework import viewsets, permissions
from .models import Prescription
from .serializers import PrescriptionSerializer
from core.utils import TenantViewSet

class PrescriptionViewSet(TenantViewSet):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return prescriptions filtered by tenant and user role.
        - Patients can only see their own prescriptions.
        - Dentists can see prescriptions for their patients.
        - Superusers can see all prescriptions.
        """
        queryset = super().get_queryset()

        if self.request.user.is_superuser:
            return queryset
        if self.request.user.role == 'patient':
            return queryset.filter(patient=self.request.user)
        if self.request.user.role == 'dentist':
            return queryset.filter(dentist=self.request.user)
        return queryset
