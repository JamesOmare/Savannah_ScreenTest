# customer/tests/test_integration.py
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from customer.models import Customer
from rest_framework import status
import json

class CustomerIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone_number': '+254791813902'
        }
        self.update_data = {
            'phone_number': '+254711111111'
        }
        self.customer = Customer.objects.create(**self.customer_data)
        self.client.force_authenticate(user=self.customer)
        

    def test_create_customer_and_update_phone_number(self):
        # Verify the customer was created
        customer = Customer.objects.get(username='testuser')
        self.assertEqual(customer.email, 'testuser@example.com')
        self.assertEqual(customer.phone_number, '+254791813902')
        
        # Test updating customer's phone number
        update_url = reverse('update_phone_number')
        response = self.client.put(update_url, data=json.dumps(self.update_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the phone number was updated
        customer.refresh_from_db()
        self.assertEqual(customer.phone_number, '+254711111111')
