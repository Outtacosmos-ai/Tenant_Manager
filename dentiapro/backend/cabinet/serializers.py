from rest_framework import serializers
from .models import Dentiste, Patient

class DentisteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dentiste
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'