from datetime import timedelta
from rest_framework import serializers
from .models import PhoneVerification, User, EmailVerification
from django.utils import timezone
import uuid
from django.contrib.auth import get_user_model
import random
from django.contrib.auth.hashers import make_password

User = get_user_model()

class RequestPhoneVerificationSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(max_length=20)

    def create(self, validated_data):
        phone_number = validated_data["phoneNumber"]

        # 🔹 1. Buscar o crear un usuario con este teléfono
        user, created = User.objects.get_or_create(
            phone_number=phone_number,
            defaults={
                "username": f"navauser_{uuid.uuid4().hex[:8]}",
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

        # 🔹 marcar usuario como verificado
        if not user.phone_verified:
            user.phone_verified = True
            user.save(update_fields=["phone_verified"])

        attrs['user'] = user
        return attrs
    
class SetEmailSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, attrs):
        phone_number = attrs['phoneNumber']
        email = attrs['email']

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        # caso 1: email ya existe en otro usuario
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            raise serializers.ValidationError("Email already in use")

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        email = validated_data['email']

        # asignamos email (si no lo tenía o queremos reenviar)
        user.email = email
        user.email_verified = False
        user.save()

        # generamos un nuevo código
        code = str(random.randint(100000, 999999))
        EmailVerification.objects.create(
            user=user,
            email=email,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=5)
        )

        # ⚡ Aquí después conectamos un servicio de envío real
        print(f"DEBUG: Código de verificación reenviado a {email}: {code}")

        return user

class VerifyEmailCodeSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs['phoneNumber']
        code = attrs['code']

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        try:
            record = EmailVerification.objects.filter(
                user=user,
                is_used=False
            ).latest('created_at')
        except EmailVerification.DoesNotExist:
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

        # marcar email como verificado
        user.email_verified = True
        user.save()

        attrs['user'] = user
        return attrs
    
class SetUsernameSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    username = serializers.CharField(min_length=3, max_length=50)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken")
        return value

    def validate(self, attrs):
        phone_number = attrs['phoneNumber']
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        if user.has_custom_username:  # si ya tenía username
            raise serializers.ValidationError("Username already set and cannot be changed")

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        user.username = validated_data['username']
        user.has_custom_username = True
        user.save()
        return user

class SetPasswordSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=6, max_length=6)
    acceptTerms = serializers.BooleanField()

    def validate(self, attrs):
        phone_number = attrs['phoneNumber']
        accept_Terms = attrs['acceptTerms']
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        
        if not accept_Terms:
            raise serializers.ValidationError("Terms not accepted")

        if user.can_change_password:
            raise serializers.ValidationError("Password already set")

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        user.password = make_password(validated_data['password'])
        user.accept_terms = validated_data['acceptTerms']
        user.can_change_password = True
        user.save()

        return user

