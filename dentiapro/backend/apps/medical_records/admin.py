from django.contrib import admin
from .models import MedicalRecord

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'dentist', 'date', 'diagnosis')
    list_filter = ('date', 'dentist')
    search_fields = ('patient__user__username', 'dentist__user__username', 'diagnosis')
    ordering = ('-date',)
