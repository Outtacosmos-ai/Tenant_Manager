from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, PatientViewSet, InvoiceViewSet, InventoryItemViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'inventory', InventoryItemViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="DentiaPro API",
      default_version='v1',
      description="API for DentiaPro dental clinic management system",
      terms_of_service="https://www.dentiapro.com/terms/",
      contact=openapi.Contact(email="contact@dentiapro.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
