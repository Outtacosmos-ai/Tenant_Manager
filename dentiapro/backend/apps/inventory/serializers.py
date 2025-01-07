from rest_framework import serializers
from .models import InventoryItem, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class InventoryItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = InventoryItem
        fields = ['id', 'name', 'category', 'quantity', 'unit_price', 'reorder_level']
