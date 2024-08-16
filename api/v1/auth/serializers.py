from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from users import models, utils


class PhoneNumberField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs["max_length"] = 13
        kwargs["min_length"] = 13
        kwargs["validators"] = [utils.phone_number_validator]
        super().__init__(**kwargs)


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs["write_only"] = True
        kwargs["style"] = {"input_type": "password"}
        kwargs["min_length"] = 8
        kwargs["max_length"] = 64
        kwargs["validators"] = [validate_password]
        super().__init__(**kwargs)


class UserRegisterSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    password = PasswordField()
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
