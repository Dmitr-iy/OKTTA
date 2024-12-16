from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from user_app.managers import UserManager


class User (AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, verbose_name='Имя', null=True, blank=True)
    last_name = models.CharField(max_length=255, verbose_name='Отчество', null=True, blank=True)
    family_name = models.CharField(max_length=255, verbose_name='Фамилия', null=True, blank=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    name_company = models.CharField(max_length=255, null=True, blank=True)
    website_link = models.URLField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Manager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managers')
    email = models.EmailField(unique=True, default='default@example.com')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Manager {self.email}"
