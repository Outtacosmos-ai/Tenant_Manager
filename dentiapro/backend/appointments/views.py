from rest_framework import viewsets, permissions
from .models import RendezVous
from .serializers import RendezVousSerializer

class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer
    permission_classes = [permissions.IsAuthenticated]