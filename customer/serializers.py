from rest_framework import serializers
from .models import Customer
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
import phonenumbers
from loguru import logger


class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    
    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_tokens(self, obj):
        return obj.tokens()
    
    class Meta:
        model = Customer
        fields = ['id', 'email', 'code', 'username', 'tokens']
        
    def validate(self, attrs):
        email = attrs.get('email', '')
        
        user = auth.authenticate(email=email)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact support team')
        
        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['phone_number']
    
    def validate_phone_number(self, phone_number):
        if not phone_number:
            raise serializers.ValidationError('Phone number is required')

        try:
            parsed_number = phonenumbers.parse(phone_number, "KE")
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError("Invalid phone number")
            valid_phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            return valid_phone_number
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid phone number")

    def to_representation(self, instance):
        return {
            "data": f"Phone number {instance.phone_number} has been added successfully"
            }
