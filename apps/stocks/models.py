from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import (
    make_password,
    check_password,
)  # 🔹 Para encriptar y verificar contraseñas


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    logo = models.ImageField(upload_to="user/logos", null=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # 🔹 Almacena la contraseña encriptada

    def set_password(self, raw_password):
        self.password = make_password(raw_password)  # 🔹 Encripta la contraseña

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # 🔹 Verifica la contraseña

    def __str__(self):
        return self.username


class Corporation(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    country = models.CharField(max_length=100)
    sector = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Investment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        "stocks.Usuario",
        on_delete=models.CASCADE,
        default=1,
        related_name="investments",
    )
    corporation = models.ForeignKey(
        "stocks.Corporation",
        on_delete=models.CASCADE,
        default=1,
        related_name="investments",
    )
    stocks_amount = models.DecimalField(max_digits=10, decimal_places=2)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_investment(self):
        return self.stocks_amount * self.price_at_purchase

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.corporation.name} ({self.total_investment:.2f}€)"
