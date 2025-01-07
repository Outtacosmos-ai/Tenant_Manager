from django.contrib import admin
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'dentist', 'medication', 'date')
    list_filter = ('date', 'dentist')
    search_fields = ('patient__user__username', 'dentist__user__username', 'medication')

from django.apps import AppConfig

class PrescriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.prescription'

