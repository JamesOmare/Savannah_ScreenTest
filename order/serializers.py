# serializers.py
from rest_framework import serializers
from .models import Order, Customer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
