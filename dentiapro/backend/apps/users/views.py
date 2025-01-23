from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer
from core.utils import TenantViewSet

class UserViewSet(TenantViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return users filtered by the tenant of the authenticated user.
        """
        return User.objects.filter(tenant=self.request.tenant)