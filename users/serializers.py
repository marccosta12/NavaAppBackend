import uuid
import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from rest_framework import serializers
from .models import PhoneVerification, User, EmailVerification, KYCSubmission

User = get_user_model()

#Auth

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

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()   # phone, email o username
    password = serializers.CharField(write_only=True)

    def _find_user(self, identifier: str) -> User:
        """
        Busca por teléfono (exacto), email (case-insensitive) o username (case-insensitive).
        Si hubiese colisión, prioriza: teléfono > email > username.
        """
        qs = User.objects.filter(
            Q(phone_number=identifier) |
            Q(email__iexact=identifier) |
            Q(username__iexact=identifier)
        )

        if not qs.exists():
            raise User.DoesNotExist

        if qs.count() == 1:
            return qs.first()

        # Desambiguación explícita por prioridad
        phone_match = qs.filter(phone_number=identifier).first()
        if phone_match:
            return phone_match

        email_match = qs.filter(email__iexact=identifier).first()
        if email_match:
            return email_match

        username_match = qs.filter(username__iexact=identifier).first()
        if username_match:
            return username_match

        # Si llegamos aquí es muy raro, pero cubrimos el caso
        raise MultipleObjectsReturned("Multiple users matched this identifier")

    def validate(self, attrs):
        identifier = attrs.get("identifier", "").strip()
        password = attrs.get("password")

        try:
            user = self._find_user(identifier)
        except (User.DoesNotExist, MultipleObjectsReturned):
            raise serializers.ValidationError("Invalid credentials")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        if user.is_blocked:
            raise serializers.ValidationError("Account is blocked")

        attrs["user"] = user
        return attrs

#Users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "phone_number",
            "phone_verified",
            "email",
            "email_verified",
            "country",
            "city",
            "postal_code",
            "address",
            "kyc_status",
            "is_blocked",
        ]

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["country", "city", "postal_code", "address"]

    def update(self, instance, validated_data):
        instance.country = validated_data.get("country", instance.country)
        instance.city = validated_data.get("city", instance.city)
        instance.postal_code = validated_data.get("postal_code", instance.postal_code)
        instance.address = validated_data.get("address", instance.address)
        instance.save()
        return instance

#KYC
class KycUploadDocumentSerializer(serializers.ModelSerializer):
    documentType = serializers.ChoiceField(
        choices=["passport", "nie", "national_id"], source="document_type"
    )
    documentNumber = serializers.CharField(source="extracted_number", required=False, allow_blank=True)
    side = serializers.ChoiceField(
        choices=["Front", "Back"], source="side"
    )
    file = serializers.FileField(write_only=True)

    class Meta:
        model = KYCSubmission
        fields = ["documentType", "documentNumber", "side", "file"]

    def create(self, validated_data):
        user = self.context["request"].user
        uploaded_file = validated_data.pop("file")

        # Guardamos en FileField o como ruta
        submission = KYCSubmission.objects.create(
            user=user,
            type="DOCUMENT",
            file_url=uploaded_file,  # ⚡ aquí lo puedes cambiar por un FileField real si lo prefieres
            **validated_data
        )
        return submission


class KycUploadSelfieSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = KYCSubmission
        fields = ["file"]

    def create(self, validated_data):
        user = self.context["request"].user
        uploaded_file = validated_data.pop("file")

        return KYCSubmission.objects.create(
            user=user,
            type="SELFIE",
            file_url=uploaded_file
        )


