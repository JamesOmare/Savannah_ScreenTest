# serializers.py
from attr import fields
from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('owner',)

    def create(self, validated_data):
        owner = self.context['request'].user
        return Order.objects.create(owner=owner, **validated_data)