from rest_framework import serializers
from .models import Dentist, Specialization

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name', 'description']

class DentistSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    specialization = SpecializationSerializer(read_only=True)

    class Meta:
        model = Dentist
        fields = ['id', 'user', 'specialization', 'license_number', 'years_of_experience']