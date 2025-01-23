from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CabinetViewSet, AppointmentViewSet, MedicalRecordViewSet,
    InvoiceViewSet, InventoryItemViewSet
)

router = DefaultRouter()
router.register(r'cabinets', CabinetViewSet, basename='cabinet')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'medical-records', MedicalRecordViewSet, basename='medicalrecord')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'inventory', InventoryItemViewSet, basename='inventory')

urlpatterns = [
    path('', include(router.urls)),
]
