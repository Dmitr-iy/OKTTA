from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from user_app.managers import UserManager


class User (AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    token_balance = models.IntegerField(default=0)
    integrations = models.JSONField(default=list)
    # plan = models.CharField(max_length=50)  # e.g., "free", "premium"
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Manager {self.user.email}"


class UserManagerRelationship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managers')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='managed_users')

    class Meta:
        unique_together = ('user', 'manager')

    def __str__(self):
        return f"{self.manager.user.email} manages {self.user.email}"
