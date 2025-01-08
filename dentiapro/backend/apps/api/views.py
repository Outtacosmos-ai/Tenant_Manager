from rest_framework import viewsets
from apps.appointments.models import Appointment
from apps.patient.models import Patient
from apps.billing.models import Invoice
from apps.inventory.models import InventoryItem
from .serializers import AppointmentSerializer, PatientSerializer, InvoiceSerializer, InventoryItemSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
