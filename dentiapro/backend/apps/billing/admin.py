from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice_number', 'amount')  # removed 'date', 'paid'
    list_filter = ('status',)  # removed 'paid', 'date'
    search_fields = ('patient__user__username',)
