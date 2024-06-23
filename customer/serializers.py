from rest_framework import serializers
from .models import Customer
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from drf_spectacular.utils import extend_schema_field, OpenApiTypes

class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    
    # @extend_schema_field(OpenApiTypes.OBJECT)
    # def get_tokens(self, obj):
    #     return obj.tokens()
    
    class Meta:
        model = Customer
        fields = ['id', 'email', 'username', 'tokens']
        
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
