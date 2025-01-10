from rest_framework import serializers
from .models import Tenant, Domain

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = [
            'id', 'name', 'schema_name', 'paid_until', 'on_trial', 'created_on',
            'updated_on'  # Explicitly include timestamps if needed
        ]
        read_only_fields = ['created_on', 'updated_on']  # Ensure timestamps are not writable


class DomainSerializer(serializers.ModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all())

    class Meta:
        model = Domain
        fields = [
            'id', 'domain', 'tenant', 'is_primary', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class TenantDetailSerializer(serializers.ModelSerializer):
    # Nested serializer to include related domains for a tenant
    domains = DomainSerializer(many=True, read_only=True, source='domain_set')

    class Meta:
        model = Tenant
        fields = [
            'id', 'name', 'schema_name', 'paid_until', 'on_trial', 'created_on', 'updated_on', 'domains'
        ]
        read_only_fields = ['created_on', 'updated_on']
