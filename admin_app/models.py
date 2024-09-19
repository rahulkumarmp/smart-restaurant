from datetime import date

from django.db import models

from user_app.admin import CustomUser
from user_app.models import Customers


# Create your models here.
class Table(models.Model):
    name = models.CharField(max_length=60, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=602)
    password = models.CharField(max_length=30)
    total_seats = models.IntegerField(blank=True, null=True)
    seats_taken = models.IntegerField(blank=True, null=True)
    qr_token = models.CharField(max_length=100, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_qr_login = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @classmethod
    def authenticate(cls, username, password):
        try:
            return cls.objects.get(username=username, password=password)
        except:
            return None

    @classmethod
    def authenticate_with_qr_token(cls, qr_token):
        try:
            return cls.objects.get(qr_token=qr_token)
        except cls.DoesNotExist:
            return None

class Menu(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)
    offer = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='static/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_todays_menu(cls):
        today = date.today()
        return cls.objects.filter(created_at__date=today)

class Invoice(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    file = models.FileField(upload_to='invoices/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)