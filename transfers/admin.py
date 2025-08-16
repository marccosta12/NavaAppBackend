from django.contrib import admin
from .models import Recipient, PaymentMethod, Transfer

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'country', 'is_active', 'created_at')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('country', 'is_active')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('label', 'user', 'type', 'currency', 'is_verified')
    search_fields = ('label','provider')
    list_filter = ('type', 'is_verified', 'is_active')

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipient', 'amount', 'status', 'created_at')
    search_fields = ('id', 'recipient__full_name')
    list_filter = ('status', 'method', 'currency_from', 'currency_to')