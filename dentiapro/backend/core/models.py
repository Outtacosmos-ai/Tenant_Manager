from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name='owned_tenants')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'tenants'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Domain(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    tenant = models.ForeignKey(Tenant, related_name='domains', on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'domains'

    def __str__(self):
        return self.domain
