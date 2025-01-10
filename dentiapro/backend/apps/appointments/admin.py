from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'patient', 'dentist', 'date', 'start_time', 'status')
    list_filter = ('status', 'date', 'dentist')
    search_fields = ('patient__user__username', 'dentist__user__username', 'tenant__name')
