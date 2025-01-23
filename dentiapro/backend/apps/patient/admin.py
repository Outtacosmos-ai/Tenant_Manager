from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'phone_number', 'emergency_contact')
    search_fields = ('user__username', 'user__email', 'phone_number', 'emergency_contact')
    list_filter = ('date_of_birth',)
