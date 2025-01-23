
from django.db import models
from apps.tenant.models import Tenant

class Cabinet(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='cabinets')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cabinets'
        ordering = ['name']

    def __str__(self):
        return self.name
