from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Cabinet
from .serializers import CabinetSerializer

class CabinetViewSet(viewsets.ModelViewSet):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [IsAuthenticated]