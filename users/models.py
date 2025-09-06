import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    # Reemplazamos el ID por UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Fechas de creación/actualización
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Email (ya viene en AbstractUser, pero lo redefinimos como único)
    email = models.EmailField(unique=True, null=False, blank=False)

    # Teléfono
    phone_number = models.CharField(max_length=20, unique=True, null=False, blank=False)
    phone_verified = models.BooleanField(default=False)

    # Email verificado
    email_verified = models.BooleanField(default=False)

    # Creación nombre usuario
    has_custom_username = models.BooleanField(default=False)
    can_change_password = models.BooleanField(default=False)

    # Aceptación de términos
    accept_terms = models.BooleanField(default=False)

    # Dirección
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    # KYC
    kyc_status = models.CharField(max_length=20, default="PENDING")
    kyc_document_id = models.UUIDField(null=True, blank=True)
    kyc_selfie_id = models.UUIDField(null=True, blank=True)

    # Cliente externo (Stripe, proveedor de pagos, etc.)
    customer_id = models.CharField(max_length=100, null=True, blank=True)

    # Bloqueo de cuenta
    is_blocked = models.BooleanField(default=False)
    block_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username or self.email
    
class PhoneVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="phone_verifications")
    phone_number = models.CharField(max_length=20)
    code = models.CharField(max_length=10)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.phone_number} - {self.code}"


class EmailVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="email_verifications")
    email = models.EmailField()
    code = models.CharField(max_length=10)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.email} - {self.code}"


class KYCSubmission(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    SIDE_CHOICES = [
        ("FRONT", "Front"),
        ("BACK", "Back"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="kyc_submissions")
    type = models.CharField(max_length=50)  # Ej: "DOCUMENT", "SELFIE"
    document_type = models.CharField(max_length=50, null=True, blank=True)
    side = models.CharField(max_length=10, choices=SIDE_CHOICES, null=True, blank=True)  # FRONT / BACK
    file_url = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    reviewed_by = models.UUIDField(null=True, blank=True)  # luego podremos relacionarlo con AdminUser
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    extracted_country = models.CharField(max_length=50, null=True, blank=True)
    extracted_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.type} - {self.status}"


class FiscalAddress(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="fiscal_address")
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    address_line = models.TextField()
    proof_document_url = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    reviewed_by = models.UUIDField(null=True, blank=True)  # luego lo conectamos a AdminUser
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.country}, {self.city}"

