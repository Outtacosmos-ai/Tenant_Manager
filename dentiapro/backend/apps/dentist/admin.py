from django.contrib import admin
from .models import Dentist

@admin.register(Dentist)
class DentistAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'license_number')
    search_fields = ('user_username', 'user_email', 'specialization')

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')