from django.urls import path
from .views import OIDCAuthenticateView, OIDCCallbackView, UpdatePhoneNumberView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/v1/auth/', OIDCAuthenticateView.as_view(), name='oidc_authenticate'),
    path('api/v1/auth0/callback/', OIDCCallbackView.as_view(), name='oidc_callback'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/update-phone-number/', UpdatePhoneNumberView.as_view(), name='update_phone_number'),
]