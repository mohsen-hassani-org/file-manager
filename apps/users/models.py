# from uuid import uuid4
from django.db import models
# from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from apps.core.mixins import Activable, Timestampable
from apps.users.mixins import UserFileManagerMixin


class CustomUserManager(UserManager, models.Manager):
    def create_superuser(self, email, password = ..., **extra_fields):
        return super().create_superuser(email, email, password, **extra_fields)

    def create_user(self, email, password = ..., **extra_fields):
        return super().create_user(email, email, password, **extra_fields)


class User(Timestampable, AbstractUser, Activable, UserFileManagerMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if self.pk == None:
            self.username = self.email
        return super().save(*args, **kwargs)

    @property
    def display_name(self):
        return (
            ' '.join((self.first_name, self.last_name))
            if self.first_name and self.last_name
            else self.email
        )
