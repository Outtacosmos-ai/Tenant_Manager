from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DentistViewSet, SpecializationViewSet

router = DefaultRouter()
router.register(r'dentists', DentistViewSet)
router.register(r'specializations', SpecializationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]