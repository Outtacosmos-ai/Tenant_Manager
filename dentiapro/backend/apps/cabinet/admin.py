from django.contrib import admin
from .models import Cabinet

@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_number', 'email', 'is_active', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
