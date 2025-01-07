from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TenantViewSet, DomainViewSet

router = DefaultRouter()
router.register(r'tenants', TenantViewSet)
router.register(r'domains', DomainViewSet)

urlpatterns = [
    path('', include(router.urls)),
]