from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Plan(models.Model):

    name = models.CharField(max_length=20)
    thumbnail_sizes = ArrayField(models.IntegerField())
    original_image_access = models.BooleanField()
    expiring_image_access = models.BooleanField()

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("User must have an username.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=40, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    plan = models.ForeignKey(
        Plan, on_delete=models.SET_NULL, default=None, null=True, blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
