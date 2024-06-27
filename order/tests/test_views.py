# orders/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from order.models import Order
from customer.models import Customer

class OrderViewsetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer1 = Customer.objects.create(
            username='testuser',
            email='testuser@example.com'
        )
        
        self.client2 = APIClient()
        self.customer2 = Customer.objects.create(
            username='testuser2',
            email='testuser2@example.com',
            phone_number='+254791813456'
        )
        self.order = Order.objects.create(
            item='Test Item',
            amount=100.00,
            description='Test Description',
            owner=self.customer1
        )
        self.client.force_authenticate(user=self.customer1)
        self.client2.force_authenticate(user=self.customer2)
        

    def test_list_orders(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['item'], 'Test Item')

    def test_create_order_without_phone_number(self):
        order_data = {
            'item': 'New Item',
            'amount': 150.00,
            'description': 'New Description',
            'owner': self.customer1.id
        }
        response = self.client.post(reverse('order-list'), order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_order_with_phone_number(self):
        order_data = {
            'item': 'New Item2',
            'amount': 120.00,
            'description': 'New Description2',
            'owner': self.customer2.id
        }
        response = self.client2.post(reverse('order-list'), order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sms_response'], 'The sms message has been sent to the user with a status of Success')
