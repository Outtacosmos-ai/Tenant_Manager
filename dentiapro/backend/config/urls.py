# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # OAuth2 endpoints
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    
    # API endpoints
    path('api/', include('apps.api.urls')),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/tenants/', include('apps.tenant.urls')),
    path('api/cabinets/', include('apps.cabinet.urls')),
    path('api/appointments/', include('apps.appointments.urls')),
    path('api/billing/', include('apps.billing.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/medical-records/', include('apps.medical_records.urls')),
    path('api/prescriptions/', include('apps.prescription.urls')),
    
    # Prometheus metrics
    path('', include('django_prometheus.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add debug toolbar URLs in debug mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns