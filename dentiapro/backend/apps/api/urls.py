from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CabinetViewSet, AppointmentViewSet, MedicalRecordViewSet,
    InvoiceViewSet, InventoryItemViewSet
)

router = DefaultRouter()
router.register(r'cabinets', CabinetViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'medical-records', MedicalRecordViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'inventory', InventoryItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
