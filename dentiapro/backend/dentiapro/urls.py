from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import UserViewSet, RoleViewSet
from cabinet.views import DentisteViewSet, PatientViewSet
from appointments.views import RendezVousViewSet
from billing.views import FactureViewSet
from inventory.views import StockViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'dentistes', DentisteViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'rendez-vous', RendezVousViewSet)
router.register(r'factures', FactureViewSet)
router.register(r'stocks', StockViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]