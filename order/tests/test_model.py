# orders/tests/test_models.py
from django.test import TestCase
from order.models import Order
from customer.models import Customer

class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            username='testuser',
            email='testuser@example.com'
        )
        self.order = Order.objects.create(
            item='Test Item',
            amount=100.00,
            description='Test Description',
            owner=self.customer
        )

    def test_order_creation(self):
        self.assertEqual(self.order.item, 'Test Item')
        self.assertEqual(self.order.amount, 100.00)
        self.assertEqual(self.order.description, 'Test Description')
        self.assertEqual(self.order.owner, self.customer)
