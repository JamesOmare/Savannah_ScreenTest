# models.py
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class CustomerManager(BaseUserManager):
    def create_user(self, email, first_name, last_name):
        if first_name is None:
            raise TypeError('Users should have a first name')
        if last_name is None:
            raise TypeError('Users should have a last name')
        if email is None:
            raise TypeError('Users should have an email')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name
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
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(
        unique=True,
        max_length=255,
        db_index=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email
