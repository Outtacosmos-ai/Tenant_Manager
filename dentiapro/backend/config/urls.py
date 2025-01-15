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

# JWT API endpoints
jwt_urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# Application-specific API endpoints
api_urlpatterns = [
    path('auth/', include('apps.authentication.urls')),
    path('users/', include('apps.users.urls')),
    path('tenants/', include('apps.tenant.urls')),
    path('cabinets/', include('apps.cabinet.urls')),
    path('appointments/', include('apps.appointments.urls')),
    path('billing/', include('apps.billing.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('medical-records/', include('apps.medical_records.urls')),
    path('prescriptions/', include('apps.prescription.urls')),
]

# Main urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT and OAuth2 endpoints
    path('api/jwt/', include(jwt_urlpatterns)),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    
    # Prometheus metrics
    path('metrics/', include('django_prometheus.urls')),

    # API endpoints
    path('api/', include(api_urlpatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug toolbar endpoints (only in DEBUG mode)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
