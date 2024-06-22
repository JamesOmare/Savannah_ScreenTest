from rest_framework import serializers
from .models import Customer
from django.contrib import auth

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        email = attrs.get('email', '')

        if not email:
            raise serializers.ValidationError('Email is required')

        return attrs
    
    def create(self, validated_data):
        return Customer.objects.create_user(**validated_data)
