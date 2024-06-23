from django.urls import path
from .views import OIDCAuthenticateView, OIDCCallbackView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/auth/', OIDCAuthenticateView.as_view(), name='oidc_authenticate'),
    path('api/auth0/callback/', OIDCCallbackView.as_view(), name='oidc_callback'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]