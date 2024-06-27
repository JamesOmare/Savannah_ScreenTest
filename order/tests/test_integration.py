from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from order.models import Order
from customer.models import Customer
from rest_framework import status
import json

class OrderIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone_number': '+254791813902'
        }
        self.customer = Customer.objects.create(**self.customer_data)
        self.client.force_authenticate(user=self.customer)

        self.order_data = {
            'item': 'Test Item',
            'amount': '100.00',
            'description': 'Test Description',
        }


    def test_create_order(self):
        # Test creating a new order
        create_url = reverse('order-list')
        response = self.client.post(create_url, data=json.dumps(self.order_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify the order creation success message
        self.assertIn('msg', response.data)
        self.assertEqual(response.data['msg'], 'Order created Successfully')

        # Optionally, check other response data if needed
        if 'sms_response' in response.data:
            self.assertIn('africastalking_response', response.data)
            self.assertIn('SMSMessageData', response.data['africastalking_response'])


    def test_list_orders(self):
        # Create a sample order
        order = Order.objects.create(
            item='Sample Item',
            amount=50.0,
            description='Sample Description',
            owner=self.customer
        )

        # Test listing orders
        list_url = reverse('order-list')
        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 
        self.assertEqual(response.data[0]['item'], order.item)
        self.assertEqual(float(response.data[0]['amount']), order.amount)
        self.assertEqual(response.data[0]['description'], order.description)

    def test_retrieve_order(self):
        # Create a sample order
        order = Order.objects.create(
            item='Sample Item',
            amount=50.0,
            description='Sample Description',
            owner=self.customer
        )

        # Test retrieving a specific order
        retrieve_url = reverse('order-detail', kwargs={'pk': order.id})
        response = self.client.get(retrieve_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['item'], order.item)
        self.assertEqual(float(response.data['amount']), order.amount)
        self.assertEqual(response.data['description'], order.description)
