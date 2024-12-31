from rest_framework import viewsets, permissions
from .models import Facture
from .serializers import FactureSerializer

class FactureViewSet(viewsets.ModelViewSet):
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer
    permission_classes = [permissions.IsAuthenticated]