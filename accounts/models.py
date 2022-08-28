from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class UserManager(BaseUserManager):

    def _create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    # create a custom super_user method to override
    # the required username field for create_superuser()
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self._create_user(email, password, **kwargs)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        max_length=200,
        unique=True,
        error_messages={
            "unique": "A user with that email already exists."
        },
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


class Organization(User):
    SIZE_CHOICES = [
        ('small', '1-50'),
        ('mid', '51-200'),
        ('big', '201-1000'),
    ]

    company_name = models.CharField(max_length=200, unique=True)
    company_size = models.CharField(
        max_length=5,
        choices=SIZE_CHOICES,
        default='small', blank=True)
    slug = models.SlugField(null=True, max_length=250)
    phone_number = PhoneNumberField(blank=True, )

    def __str__(self):
        return self.company_name

    def get_absolute_url(self):
        return self.slug


@receiver(pre_save, sender=Organization)
def slugify_name(sender, instance, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.company_name)


