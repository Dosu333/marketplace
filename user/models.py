from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from .managers import CustomUserManager


class User(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=225, blank=False, null=False)
    last_name = models.CharField(max_length=225, blank=False, null=False)
    phone = models.CharField(max_length=14, blank=True, null=True)
    acct_no = models.CharField(max_length=10, blank=True, null=True)
    image = models.FileField(upload_to='users/', blank=True, null=True)
    referrer = models.ForeignKey('self', on_delete=models.CASCADE,blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save_last_login(self):
        self.last_login = datetime.now()
        self.save()