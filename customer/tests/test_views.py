# customers/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class OIDCAuthenticateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_oidc_authenticate_view(self):
        response = self.client.get(reverse('oidc-authenticate'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('redirect_url', response.data)
        
    def test_oidc_authenticate_view(self):
        response = self.client.get(reverse('oidc_authenticate'))
        self.assertEqual(response.status_code, 200)
