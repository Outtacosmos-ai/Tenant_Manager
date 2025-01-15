from django.contrib import admin
from .models import Tenant, Domain

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'paid_until', 'on_trial', 'is_active')
    search_fields = ('name', 'schema_name')
    list_filter = ('is_active', 'on_trial')  # Added filters

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    search_fields = ('domain', 'tenant__name')
    list_filter = ('is_primary',)  # Added filters for better management
