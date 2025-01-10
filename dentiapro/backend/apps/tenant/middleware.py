from django.db import connection
from django.http import HttpResponseForbidden
from .models import Tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return self.get_response(request)

        try:
            tenant = Tenant.objects.get(id=tenant_id)
            connection.set_tenant(tenant)
            request.tenant = tenant
        except Tenant.DoesNotExist:
            return HttpResponseForbidden("Invalid tenant")

        response = self.get_response(request)
        connection.set_schema_to_public()
        return response