from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from apps.cabinet.models import Cabinet
from apps.appointments.models import Appointment
from apps.medical_records.models import MedicalRecord
from apps.billing.models import Invoice
from apps.inventory.models import InventoryItem
from .serializers import (
    CabinetSerializer, AppointmentSerializer, MedicalRecordSerializer,
    InvoiceSerializer, InventoryItemSerializer
)

class TenantFilterMixin:
    """Mixin to filter queryset by tenant."""
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'tenant'):
            return queryset.filter(tenant=self.request.tenant)
        raise NotFound("Tenant not found.")

class CabinetViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [IsAuthenticated]

class AppointmentViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

class MedicalRecordViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

class InvoiceViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

class InventoryItemViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]
