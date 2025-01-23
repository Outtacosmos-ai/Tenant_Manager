from django.contrib import admin
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'dentist')
    list_filter = ('dentist',)  # Fixed: `list_filter` should be a tuple or list
    search_fields = ('patient__user__username', 'dentist__user__username')

# No changes needed for the AppConfig class
from django.apps import AppConfig

class PrescriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.prescription'
