from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.cabinet.views import CabinetViewSet
from apps.patient.views import PatientViewSet
from apps.appointments.views import AppointmentViewSet
from apps.billing.views import InvoiceViewSet
from apps.inventory.views import InventoryItemViewSet

# Create a router for viewsets
router = DefaultRouter()
router.register(r'cabinets', CabinetViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'inventory', InventoryItemViewSet)

urlpatterns = [
    # Admin and token-related endpoints
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Viewset-based routes from the router
    path('api/', include(router.urls)),

    # Modular includes for app-specific URL files
    path('api/auth/', include('apps.authentication.urls')),
    path('api/cabinet/', include('apps.cabinet.urls')),
    path('api/patient/', include('apps.patient.urls')),
    path('api/appointment/', include('apps.appointment.urls')),
    path('api/medical-record/', include('apps.medical_record.urls')),
    path('api/billing/', include('apps.billing.urls')),
    path('api/inventory/', include('apps.inventory.urls')),

    # OAuth2 provider URLs
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
