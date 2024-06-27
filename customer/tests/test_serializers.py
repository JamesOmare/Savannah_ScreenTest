# customers/tests/test_serializers.py
from django.test import TestCase
from customer.serializers import CustomerSerializer
from customer.models import Customer

class CustomerSerializerTest(TestCase):
    def setUp(self):
        self.customer_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
        }
        self.customer = Customer.objects.create(**self.customer_data)

    def test_customer_serializer(self):
        serializer = CustomerSerializer(self.customer)
        data = serializer.data
        self.assertEqual(data['email'], self.customer.email)
        self.assertEqual(data['username'], self.customer.username)
