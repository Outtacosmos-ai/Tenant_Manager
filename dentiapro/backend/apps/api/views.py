from rest_framework import viewsets
from apps.cabinet.models import Cabinet
from apps.appointments.models import Appointment
from apps.medical_records.models import MedicalRecord
from apps.billing.models import Invoice
from apps.inventory.models import InventoryItem
from .serializers import (
    CabinetSerializer, AppointmentSerializer, MedicalRecordSerializer,
    InvoiceSerializer, InventoryItemSerializer
)

class CabinetViewSet(viewsets.ModelViewSet):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer

    def get_queryset(self):
        return Cabinet.objects.filter(tenant=self.request.tenant)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.filter(cabinet__tenant=self.request.tenant)

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    def get_queryset(self):
        return MedicalRecord.objects.filter(patient__tenant=self.request.tenant)

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.filter(patient__tenant=self.request.tenant)

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer

    def get_queryset(self):
        return InventoryItem.objects.filter(cabinet__tenant=self.request.tenant)
