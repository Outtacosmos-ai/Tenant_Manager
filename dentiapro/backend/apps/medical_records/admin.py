from django.contrib import admin
from .models import MedicalRecord

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'dentist', 'diagnosis')
    list_filter = ('dentist',)  # Fixed: `list_filter` should be a tuple or list
    search_fields = ('patient__user__username', 'dentist__user__username', 'diagnosis')
    ordering = ('-id',)
