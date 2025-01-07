from django.contrib import admin
from .models import Cabinet

@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_number', 'email')
    search_fields = ('name', 'email')