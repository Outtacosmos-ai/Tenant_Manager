from django.db import connection
from django_tenants.middleware import TenantMainMiddleware

class TenantMiddleware(TenantMainMiddleware):
    def process_request(self, request):
        connection.set_schema_to_public()
        hostname = self.hostname_from_request(request)
        
        tenant = self.get_tenant(domain_model=self.get_tenant_domain_model(),
                                 hostname=hostname)
        tenant.domain_url = hostname
        request.tenant = tenant
        connection.set_tenant(request.tenant)
        return None

