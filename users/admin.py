from django.contrib import admin
from .models import PhoneVerification, EmailVerification, KYCSubmission, FiscalAddress
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("id", "username", "email", "phone_number", "is_blocked", "kyc_status", "created_at")
    list_filter = ("is_blocked", "kyc_status", "created_at")
    search_fields = ("username", "email", "phone_number")
    ordering = ("-created_at",)


@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "code", "is_used", "expires_at", "attempts")
    list_filter = ("is_used", "created_at")
    search_fields = ("phone_number", "code")


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "code", "is_used", "expires_at", "attempts")
    list_filter = ("is_used", "created_at")
    search_fields = ("email", "code")


@admin.register(KYCSubmission)
class KYCSubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "document_type", "status", "reviewed_by", "reviewed_at")
    list_filter = ("status", "type")
    search_fields = ("user__username", "document_type")


@admin.register(FiscalAddress)
class FiscalAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "country", "city", "postal_code", "status")
    list_filter = ("status", "country")
    search_fields = ("user__username", "city", "postal_code")
