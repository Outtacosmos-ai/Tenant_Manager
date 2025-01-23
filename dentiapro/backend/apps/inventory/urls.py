from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'items', InventoryItemViewSet, basename='inventory-item')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
