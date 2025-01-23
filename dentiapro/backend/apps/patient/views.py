from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import Patient
from .serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Restrict access to the patient's own record
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user)
        return self.queryset

    def perform_create(self, serializer):
        # Enforce the user field to be the authenticated user
        if hasattr(self.request.user, 'patient'):
            raise NotFound("A patient record for this user already exists.")
        serializer.save(user=self.request.user)