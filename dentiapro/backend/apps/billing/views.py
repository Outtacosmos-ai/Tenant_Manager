from rest_framework import viewsets, permissions
from .models import Invoice
from .serializers import InvoiceSerializer
from core.utils import TenantViewSet

class InvoiceViewSet(TenantViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return invoices filtered by tenant and user role.
        Patients only have access to their own invoices.
        """
        queryset = super().get_queryset()
        
        # Role-based filtering
        if self.request.user.role == 'patient':
            return queryset.filter(patient=self.request.user)
        # Dentists or other roles can access all invoices (or implement additional checks if needed)
        return queryset