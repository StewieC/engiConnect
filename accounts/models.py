from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        CLIENT    = 'client',    'Client'
        ENGINEER  = 'engineer',  'Freelance Engineer'
        IN_HOUSE  = 'in_house',  'In-House Engineer'
        ADMIN     = 'admin',     'Admin'

    # Core fields
    email        = models.EmailField(unique=True)
    full_name    = models.CharField(max_length=255)
    phone        = models.CharField(max_length=20, blank=True)
    role         = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)
    avatar       = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Status flags
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    date_joined  = models.DateTimeField(default=timezone.now)

    # For engineers: whether they have been verified by admin
    is_verified  = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.full_name} ({self.email})'

    @property
    def is_client(self):
        return self.role == self.Role.CLIENT

    @property
    def is_engineer(self):
        return self.role == self.Role.ENGINEER

    @property
    def is_in_house(self):
        return self.role == self.Role.IN_HOUSE

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN

    def get_dashboard_url(self):
        from django.urls import reverse
        role_dashboard = {
            self.Role.CLIENT:   'accounts:client_dashboard',
            self.Role.ENGINEER: 'accounts:engineer_dashboard',
            self.Role.IN_HOUSE: 'accounts:inhouse_dashboard',
            self.Role.ADMIN:    'accounts:admin_dashboard',
        }
        return reverse(role_dashboard.get(self.role, 'accounts:client_dashboard'))