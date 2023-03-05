from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager

timezone.activate('Asia/Kolkata')


class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=255, default="Anonymous")
    email = models.EmailField(unique=True)
    contact = models.PositiveBigIntegerField(default=100)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    reset_token = models.CharField(max_length=255, default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'contact']

    objects = UserManager()

    def __str__(self):
        return self.email