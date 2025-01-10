from django.contrib import admin
from .models import InventoryItem, Category

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'cost_price', 'minimum_quantity', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category__name')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
