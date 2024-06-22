from django.urls import path
from .views import oidc_authenticate, oidc_callback


urlpatterns = [
  # http://127.0.0.1:8000/customer/api/auth/
  path('api/auth/', oidc_authenticate, name="oidc_authenticate"),

  # http://127.0.0.1:8000/customer/api/auth0/callback/
  path('api/auth0/callback/', oidc_callback)
]

# from django.urls import path
# from .views import OIDCAuthenticateView, OIDCCallbackView

# urlpatterns = [
#     path('api/auth/', OIDCAuthenticateView.as_view(), name='oidc_authenticate'),
#     path('api/auth0/callback/', OIDCCallbackView.as_view(), name='oidc_callback'),
# ]