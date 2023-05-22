import re

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        required_fields = {
            'email': "Users must have an email address",
            'username': "Users must have a username",
            'first_name': "Users must have a first name",
            'last_name': "Users must have a last name",
        }

        for field, error_message in required_fields.items():
            if not kwargs.get(field) and field != 'email':
                raise ValueError(error_message)
            elif field == 'email' and not email:
                raise ValueError(error_message)

        user = self.model(
            email=self.normalize_email(email),
            username=kwargs.get('username').lower(),
            first_name=kwargs.get('first_name').title(),
            last_name=kwargs.get('last_name').title(),
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractBaseUser):
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    CATEGORY_CHOICES = (
        ('developpeur', 'Développeur'),
        ('entrepreneur', 'Entrepreneur'),
    )

    id = models.AutoField(primary_key=True)
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False
    )

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(
        blank=False,
        max_length=250
    )
    last_name = models.CharField(
        blank=False,
        max_length=250
    )
    username = models.CharField(
        unique=True,
        blank=False,
        max_length=250,
    )
    phone_number = models.CharField(
        max_length=10,
        blank=True,
    )
    category = models.CharField(
        max_length=250,
        blank=False,
        choices=CATEGORY_CHOICES,
        default='developpeur'
    )
    company_name = models.CharField(
        max_length=250,
        blank=True,
    )


    USERNAME_FIELD = 'email'  # field that will be used to distinguish users. can be username, email, first_name etc...
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.phone_number = re.sub('[^0-9]', '', self.phone_number)
        super().save(*args, **kwargs)


class EmailConfirmation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)

    def generate_token(self):
        self.token = get_random_string(length=64)

