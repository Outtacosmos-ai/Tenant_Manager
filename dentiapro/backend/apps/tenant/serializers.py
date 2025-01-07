from rest_framework import serializers
from .models import Tenant, Domain

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'name', 'schema_name', 'paid_until', 'on_trial', 'created_on']

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['id', 'domain', 'tenant', 'is_primary']