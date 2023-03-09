from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Permission
from dheera.models import UUIDModel
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group

# Create your models here.
# Organization, User, User Type

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email is requirede")
        
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, UUIDModel):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = AccountManager()

    def __str__(self):
        return self.email
