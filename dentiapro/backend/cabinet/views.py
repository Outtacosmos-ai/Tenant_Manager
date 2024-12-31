from rest_framework import viewsets, permissions
from .models import Dentiste, Patient
from .serializers import DentisteSerializer, PatientSerializer

class DentisteViewSet(viewsets.ModelViewSet):
    queryset = Dentiste.objects.all()
    serializer_class = DentisteSerializer
    permission_classes = [permissions.IsAuthenticated]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]