from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from users import models
from . import fields as custom_fields


class UserRegisterSerializer(serializers.ModelSerializer):
    phone_number = custom_fields.PhoneNumberField()
    password = custom_fields.PasswordField()
    secret = serializers.CharField(max_length=50, read_only=True)

    class Meta:
        model = models.User
        fields = (
            "phone_number",
            "password",
            "date_of_birth",
            "secret",
        )

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")

        if models.User.objects.filter(phone_number=phone_number, is_active=True).exists():
            raise serializers.ValidationError(
                code="already_exists",
                detail={
                    "phone_number": [_("A user with that phone number already exists.")]
                }
            )
        return attrs

    def create(self, validated_data):
        phone_number = validated_data["phone_number"]
        password = validated_data.pop("password")

        try:
            user = models.User.objects.get(phone_number=phone_number)
        except models.User.DoesNotExist:
            validated_data["is_active"] = False
            user = super().create(validated_data=validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        otp = instance.generate_otp()
        data["secret"] = otp.secret
        return data


class UserRegisterConfirmSerializer(serializers.ModelSerializer):
    secret = serializers.CharField(max_length=100, write_only=True)
    otp = serializers.CharField(
        max_length=10,
        min_length=4,
        error_messages={
            "min_length": _("OTP must be at least 4 characters long."),
            "max_length": _("OTP must be at most 10 characters long."),
        },
        write_only=True
    )

    class Meta:
        model = models.User
        fields = (
            "id",
            "phone_number",
            "secret",
            "otp",
        )
        extra_kwargs = {
            "phone_number": {"read_only": True},
        }

    def validate(self, attrs):
        secret = attrs.get("secret")
        otp = attrs.get("otp")

        try:
            user_otp = models.UserOTP.objects.get(
                secret=secret,
                is_confirmed=False,
                user__is_deleted=False,
            )
        except models.UserOTP.DoesNotExist:
            raise serializers.ValidationError(
                code="invalid_secret",
                detail={
                    "secret": [_("Invalid secret.")]
                }
            )

        if user_otp.is_expired():
            raise serializers.ValidationError(
                code="expired_otp",
                detail={
                    "otp": [_("OTP is expired.")]
                }
            )

        if user_otp.code != otp:
            raise serializers.ValidationError(
                code="invalid_otp",
                detail={
                    "otp": [_("Invalid OTP.")]
                }
            )
        return attrs

    def create(self, validated_data):

        user_otp = models.UserOTP.objects.get(secret=validated_data["secret"])
        user = user_otp.user
        user.is_active = True
        user.save(update_fields=["is_active"])

        user_otp.is_confirmed = True
        user_otp.save(update_fields=["is_confirmed"])
        return user
