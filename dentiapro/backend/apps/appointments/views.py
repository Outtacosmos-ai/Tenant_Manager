from rest_framework import viewsets, permissions
from .models import Appointment
from .serializers import AppointmentSerializer
from core.utils import TenantViewSet

class AppointmentViewSet(TenantViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return appointments filtered by the tenant of the authenticated user,
        and filter based on the user's role (patient, dentist, etc.).
        """
        queryset = super().get_queryset()
        
        # Role-based filtering
        if self.request.user.role == 'patient':
            return queryset.filter(patient=self.request.user)
        elif self.request.user.role == 'dentist':
            return queryset.filter(dentist=self.request.user)
        return queryset
