from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'tenant', 'patient', 'dentist', 'date', 'start_time', 'end_time', 'status', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'status': {'required': True},
        }

    def validate_date(self, value):
        """Ensure the appointment date is in the future."""
        from datetime import datetime
        if value < datetime.now().date():
            raise serializers.ValidationError("Appointment date must be in the future.")
        return value

    def validate_date_time(self, value):
        """Ensure the appointment time is available for the dentist."""
        from datetime import datetime
        current_time = datetime.now().time()
        if value < current_time:
            raise serializers.ValidationError("Appointment time must be in the future.")
        return value

    def validate_status(self, value):
        """Custom validation for appointment status."""
        valid_statuses = ['scheduled', 'confirmed', 'in_progress', 'completed', 'cancelled']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Valid statuses are {', '.join(valid_statuses)}.")
        return value
