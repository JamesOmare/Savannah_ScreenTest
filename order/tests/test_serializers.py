# orders/tests/test_serializers.py
from django.test import TestCase, RequestFactory
from order.serializers import OrderSerializer
from order.models import Order
from customer.models import Customer

class OrderSerializerTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.customer = Customer.objects.create(
            username='testuser',
            email='testuser@example.com',
            phone_number='+254791813902'
        )
        self.order_data = {
            'item': 'Test Item',
            'amount': 100.00,
            'description': 'Test Description',
        }
        self.order = Order.objects.create(owner=self.customer, **self.order_data)

    def test_order_serializer(self):
        serializer = OrderSerializer(self.order)
        data = serializer.data
        self.assertEqual(data['item'], self.order.item)
        self.assertEqual(data['amount'], format(self.order.amount, '.2f'))
        self.assertEqual(data['description'], self.order.description)
        # Test that 'owner' field is excluded from the serialized data
        self.assertNotIn('owner', data)

    def test_create_order_serializer(self):
        request = self.factory.post('/fake-url')
        request.user = self.customer
        serializer = OrderSerializer(data=self.order_data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        order = serializer.save()
        self.assertEqual(order.owner, self.customer)
        self.assertEqual(order.item, self.order_data['item'])
        self.assertEqual(order.amount, self.order_data['amount'])
        self.assertEqual(order.description, self.order_data['description'])
