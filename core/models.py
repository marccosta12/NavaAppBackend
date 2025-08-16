import uuid
from django.db import models

class MethodCache(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    country_from = models.CharField(max_length=100)
    country_to = models.CharField(max_length=100)
    method = models.CharField(max_length=50)
    currency_from = models.CharField(max_length=5)
    currency_to = models.CharField(max_length=5)
    fx_rate = models.DecimalField(max_digits=12, decimal_places=6)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    fee_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    minimum_fee = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    source_updated_at = models.DateTimeField()

    def __str__(self):
        return f'Método: {self.method} ({self.country_from} -> {self.country_to})'

class FxRateCache(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    currency_from = models.CharField(max_length=5)
    currency_to = models.CharField(max_length=5)
    fx_rate = models.DecimalField(max_digits=12, decimal_places=6)
    country_from = models.CharField(max_length=100)
    country_to = models.CharField(max_length=100)
    provider_name = models.CharField(max_length=100, blank=True, null=True)
    source_updated_at = models.DateTimeField()

    def __str__(self):
        return f'Tasa de cambio: {self.currency_from}/{self.currency_to}'