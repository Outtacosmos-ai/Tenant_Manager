from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'date', 'amount', 'paid')
    list_filter = ('paid', 'date')
    search_fields = ('patient__user__username',)
