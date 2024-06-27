from django.test import TestCase
from customer.models import Customer

class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            username='testuser',
            email='testuser@example.com'
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.username, 'testuser')
        self.assertEqual(self.customer.email, 'testuser@example.com')

    def test_generate_unique_code(self):
        code = self.customer.generate_unique_code()
        self.assertEqual(len(code), 10)
