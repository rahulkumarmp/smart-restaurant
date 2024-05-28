from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager



class CustomUserManager(BaseUserManager):
    def create_user(self, email, name=None, phone=None, password=None, **extra_fields):
        # if not name:
        #     raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, email, name=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self.create_user(email, name, phone, password, **extra_fields)

    # def create_table(self, email, name=None, phone=None, password=None, **extra_fields):
    #     # if not name:
    #     #     raise ValueError('The Email field must be set')
    #     email = self.normalize_email(email)
    #     user = self.model(email=email, name=name, phone=phone, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def create_superuser(self, email, name=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, phone, password, **extra_fields)


# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    phone_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = models.CharField(
        validators=[phone_regex],
        blank=True,
        null=True,
        max_length=16,
        unique=True,
    )
    password = models.CharField(_("password"), max_length=128, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_table_user = models.BooleanField(default=False)


    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = ['name']
    object = CustomUserManager()

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    @staticmethod
    def email_exists(email: str) -> bool:
        if email == "":
            return False
        return CustomUser.objects.filter(email=email.strip()).exists()

    @staticmethod
    def phone_exists(phone: str) -> bool:
        if not phone:
            return False
        return CustomUser.objects.filter(phone=phone).exists()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True


class Customers(models.Model):

    name = models.CharField(_("name"), max_length=200, null=True, blank=True)
    mobile = models.CharField(_("mobile"), max_length=15, null=True, blank=True)
    table = models.ForeignKey('admin_app.Table', on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Cart(models.Model):

    table = models.ForeignKey('admin_app.Table', on_delete=models.CASCADE)
    menu = models.ForeignKey('admin_app.Menu', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField("quantity")
    is_ordered = models.BooleanField("is_ordered", default=False)
    is_closed = models.BooleanField("is_closed", default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)