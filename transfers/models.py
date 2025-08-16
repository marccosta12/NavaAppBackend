import uuid
from django.db import models
from django.conf import settings

class Recipient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipients')
    
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    document_type = models.CharField(max_length=50, blank=True, null=True)
    document_number = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.full_name} ({self.country})'

class PaymentMethod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_methods')
    
    type = models.CharField(max_length=50)
    label = models.CharField(max_length=100, blank=True, null=True)
    masked_number = models.CharField(max_length=50, blank=True, null=True)
    provider = models.CharField(max_length=100, blank=True, null=True)
    provider_method_id = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    last_used_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.type} - {self.label}'

class Transfer(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # El usuario que inicia la transferencia
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_transfers')
    # El destinatario de la transferencia
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='received_transfers')
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    fx_rate = models.DecimalField(max_digits=12, decimal_places=6)
    recipient_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency_from = models.CharField(max_length=5)
    currency_to = models.CharField(max_length=5)
    
    # Campo para el tipo de método de pago (ej. 'bank_transfer', 'credit_card', etc.)
    method = models.CharField(max_length=50)
    
    # El estado de la transferencia
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    transfer_reference = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    cancelled_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Transferencia {self.id} de {self.amount} {self.currency_from} a {self.recipient.full_name}'