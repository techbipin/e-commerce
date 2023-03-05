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

    verify_token = models.CharField(max_length=255, default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'contact']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Product(models.Model):
    
    COLLECTIONS = (
        ("Men", "Men"),
        ("Women", "Women"),
        ("Children", "Children")
    )
    
    SIZE = (
        ("Small", "Small"),
        ("Medium", "Medium"),
        ("Large", "Large")
    )
    
    image = models.ImageField(upload_to='products/')
    name = models.CharField(max_length=255, default="Product")
    description = models.TextField()
    price = models.FloatField(default=10.0)
    size = models.CharField(choices=SIZE, max_length=100)
    collection = models.CharField(choices=COLLECTIONS, max_length=100)