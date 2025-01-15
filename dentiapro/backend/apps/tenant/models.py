from django.db import models
from django.contrib.auth import get_user_model

class Tenant(models.Model):
    name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)  # Ensure unique emails for tenants
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='owned_tenants')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'tenants'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def is_active_tenant(self):
        """Utility method to check if the tenant is active."""
        return self.is_active

class Domain(models.Model):
    tenant = models.ForeignKey(Tenant, related_name='domains', on_delete=models.CASCADE)
    domain = models.CharField(max_length=255, unique=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'domains'

    def __str__(self):
        return self.domain
