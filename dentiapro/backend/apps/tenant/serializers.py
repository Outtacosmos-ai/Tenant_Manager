from rest_framework import serializers
from .models import Tenant, Domain

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'name', 'subdomain', 'email', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_subdomain(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Subdomain must be alphanumeric.")
        return value

class DomainSerializer(serializers.ModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all())

    class Meta:
        model = Domain
        fields = ['id', 'domain', 'tenant', 'is_primary', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class TenantDetailSerializer(serializers.ModelSerializer):
    domains = DomainSerializer(many=True, read_only=True, source='domain_set')

    class Meta:
        model = Tenant
        fields = ['id', 'name', 'subdomain', 'email', 'created_at', 'updated_at', 'domains']
        read_only_fields = ['created_at', 'updated_at']
