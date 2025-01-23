from rest_framework import viewsets, permissions
from .models import InventoryItem, Category
from .serializers import InventoryItemSerializer, CategorySerializer
from core.utils import TenantViewSet

class InventoryItemViewSet(TenantViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(tenant=self.request.tenant).select_related('category')

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)

class CategoryViewSet(TenantViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(tenant=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)