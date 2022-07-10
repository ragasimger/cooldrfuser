from django.db import models
from apps.authentication.managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser

class User(AbstractBaseUser, PermissionsMixin):

    '''Custom User Model for the system.'''

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10, null=True, blank=True, unique=True)
    image = models.ImageField(upload_to="profile/photos", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    otp = models.CharField(max_length=15, null=True,blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
