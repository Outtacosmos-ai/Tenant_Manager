from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Dentist, Specialization
from .serializers import DentistSerializer, SpecializationSerializer

class DentistViewSet(viewsets.ModelViewSet):
    queryset = Dentist.objects.all()
    serializer_class = DentistSerializer
    permission_classes = [IsAuthenticated]

class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAuthenticated]