from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import User  # Adjust if necessary based on your project's structure

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all(), write_only=True)  # Assuming you have a Tenant model

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'role', 'phone', 
                  'address', 'date_of_birth', 'profile_picture', 'tenant', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensures password is not returned in responses
            'tenant': {'required': True}  # Ensures tenant is a required field
        }

    def create(self, validated_data):
        # Ensure password is hashed before saving
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        
        if password:
            user.password = make_password(password)  # Ensures password is hashed securely
            user.save()

        return user

    def update(self, instance, validated_data):
        # Handle password update securely
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        
        return super().update(instance, validated_data)

    def validate_password(self, value):
        """Custom validation for password strength"""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def validate_email(self, value):
        """Ensure unique email for each user"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address already exists.")
        return value

    def validate_phone(self, value):
        """Ensure valid phone format (can be extended based on your requirements)"""
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Phone number must be a 10-digit number.")
        return value

