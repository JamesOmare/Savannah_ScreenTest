from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewset

router = DefaultRouter()
router.register(r'orders', OrderViewset, basename='order')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]