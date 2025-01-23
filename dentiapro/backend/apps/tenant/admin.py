# tenant/admin.py
from django.contrib import admin
from .models import Tenant, Domain

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'subdomain', 'email', 'phone', 'is_active', 'created_at')
    search_fields = ('name', 'subdomain', 'email')
    list_filter = ('is_active',)
    ordering = ('-created_at',)

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary', 'created_at')
    search_fields = ('domain', 'tenant__name')
    list_filter = ('is_primary',)
    ordering = ('-created_at',)
