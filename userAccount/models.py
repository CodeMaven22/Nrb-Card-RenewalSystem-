from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, national_id, password, **extra_fields):
        user = self.model(national_id=national_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, national_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(national_id, password, **extra_fields)


class User(AbstractBaseUser):
    national_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to='media/profile_images/')
    # Add other relevant user details (optional)

    USERNAME_FIELD = 'national_id'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.get_full_name() or self.national_id
