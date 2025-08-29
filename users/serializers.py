from rest_framework import serializers
from .models import PhoneVerification, User
from django.utils import timezone
import uuid
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class RequestPhoneVerificationSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(max_length=20)

    def create(self, validated_data):
        phone_number = validated_data["phoneNumber"]

        # 🔹 1. Buscar o crear un usuario con este teléfono
        user, created = User.objects.get_or_create(
            phone_number=phone_number,
            defaults={
                "username": f"user_{uuid.uuid4().hex[:8]}",
                "email": f"{uuid.uuid4().hex[:8]}@placeholder.com",  # placeholder, ya se actualizará
                "accept_terms": False,
            },
        )

        # 🔹 2. Generar código aleatorio (ejemplo: 6 dígitos)
        code = str(random.randint(100000, 999999))

        # 🔹 3. Crear registro de verificación
        phone_verification = PhoneVerification.objects.create(
            user=user,
            phone_number=phone_number,
            code=code,
            expires_at=timezone.now() + timezone.timedelta(minutes=5),
        )

        # ⚠️ Aquí normalmente deberíamos enviar SMS con un proveedor real
        print(f"Sending verification code {code} to {phone_number}")

        return phone_verification


class VerifyPhoneCodeSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs['phoneNumber']
        code = attrs['code']

        try:
            record = PhoneVerification.objects.filter(
                phone_number=phone_number,
                is_used=False
            ).latest('created_at')
        except PhoneVerification.DoesNotExist:
            raise serializers.ValidationError("No verification request found.")

        if record.expires_at < timezone.now():
            raise serializers.ValidationError("Code expired.")

        if record.code != code:
            record.attempts += 1
            record.save()
            raise serializers.ValidationError("Invalid code.")

        # marcar como usado
        record.is_used = True
        record.save()

        # Si no existe usuario, lo creamos
        user, created = User.objects.get_or_create(phone_number=phone_number)
        if created:
            print(f"DEBUG: Usuario creado con teléfono {phone_number}")

        attrs['user'] = user
        return attrs