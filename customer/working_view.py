from django.shortcuts import redirect
from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from loguru import logger
import requests
import json
import jwt
from jwt.algorithms import RSAAlgorithm
from .serializers import CustomerSerializer
from .models import Customer

@extend_schema_view(
    get=extend_schema(
        description='Redirects user to Auth0 for authentication',
        responses={302: None},
        tags=['Authentication'],
    )
)
class OIDCAuthenticateView(APIView):
    def get(self, request):
        auth0_authorization_url = f"https://{settings.AUTH0_DOMAIN}/authorize"
        params = {
            "response_type": "code",
            "client_id": settings.AUTH0_CLIENT_ID,
            "redirect_uri": settings.REDIRECT_URI,
            "scope": "openid profile email",
        }
        redirect_url = f"{auth0_authorization_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
        return Response({"redirect_url": redirect_url}, status=status.HTTP_200_OK)
      
@extend_schema_view(
    get=extend_schema(
        description='Handles Auth0 callback',
        responses={
            200: CustomerSerializer,
            403: dict(type='object', properties={'error': dict(type='string'), 'error_description': dict(type='string')}),
            400: dict(type='object', properties={'error': dict(type='string')}),
        },
        tags=['Authentication'],
    )
)
class OIDCCallbackView(APIView):
    def get(self, request):
        if 'error' in request.GET:
            error_description = request.GET.get('error_description')
            return Response({'error': 'access_denied', 'error_description': error_description}, status=status.HTTP_403_FORBIDDEN)

        code = request.GET.get('code')
        logger.info(f"Request data: {request.GET}")
        logger.info(f"Code: {code}")
        token_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
        token_data = {
            "grant_type": "authorization_code",
            "client_id": settings.AUTH0_CLIENT_ID,
            "client_secret": settings.AUTH0_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.REDIRECT_URI
        }
        
        logger.info(f"Token data: {token_data}")

        token_response = requests.post(token_url, data=token_data)
        token_response_data = token_response.json()
        logger.info(f"Token response data: {token_response_data}")
        id_token = token_response_data.get('id_token')

        if not id_token:
            return Response({'error': 'Invalid token response'}, status=status.HTTP_400_BAD_REQUEST)

        jwks = requests.get(settings.AUTH0_JWKS_ENDPOINT).json()
        public_key = None
        id_token_jwt_header = jwt.get_unverified_header(id_token)

        for jwk in jwks['keys']:
            if jwk['kid'] == id_token_jwt_header['kid']:
                public_key = RSAAlgorithm.from_jwk(json.dumps(jwk))

        if public_key is None:
            return Response({'error': 'Public key not found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_data = jwt.decode(id_token, public_key, audience=settings.AUTH0_CLIENT_ID, issuer=settings.AUTH0_ISSUER, algorithms=['RS256'])
            logger.info(f"Decoded data: {decoded_data}")
            email = decoded_data.get('email')
            user, created = Customer.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': decoded_data.get('given_name', ''),
                    'last_name': decoded_data.get('family_name', '')
                }
            )

            if created:
                user.set_unusable_password()
                user.save()

            serializer = CustomerSerializer(user)
            return Response(serializer.data)

        except jwt.exceptions.DecodeError as e:
            return Response({'error': f'Invalid token: {e}'}, status=status.HTTP_400_BAD_REQUEST)
