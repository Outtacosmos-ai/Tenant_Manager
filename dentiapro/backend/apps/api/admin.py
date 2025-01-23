from django.contrib import admin
from apps.cabinet.models import Cabinet
from apps.appointments.models import Appointment
from apps.medical_records.models import MedicalRecord
from apps.billing.models import Invoice
from apps.inventory.models import InventoryItem

# Custom admin models to enhance the admin panel functionality
@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tenant', 'created_at', 'updated_at')
    list_filter = ('tenant',)
    search_fields = ('name',)
    ordering = ('-created_at',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'cabinet', 'date', 'status')
    list_filter = ('status', 'cabinet')
    search_fields = ('patient__name', 'cabinet__name')
    ordering = ('-date',)

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'record_type', 'created_at')
    list_filter = ('record_type',)
    search_fields = ('patient__name', 'record_type')
    ordering = ('-created_at',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'amount', 'status', 'issued_at')
    list_filter = ('status',)
    search_fields = ('patient__name', 'status')
    ordering = ('-issued_at',)

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cabinet', 'quantity', 'last_updated')
    list_filter = ('cabinet',)
    search_fields = ('name', 'cabinet__name')
    ordering = ('-last_updated',)
