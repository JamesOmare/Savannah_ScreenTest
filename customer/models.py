# models.py
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
import uuid

class CustomerManager(BaseUserManager):
    def create_user(self, email, username):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have an email')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            username=username,
        )

        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class Customer(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    email = models.EmailField(
        unique=True,
        max_length=255,
        db_index=True
    )
    code = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = CustomerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    
    def generate_unique_code(self):
        return uuid.uuid4().hex[:10].upper()
    
    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        }
