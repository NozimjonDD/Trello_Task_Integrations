from rest_framework import serializers

from apps.users import models
from apps.fantasy import models as fantasy_models


class _AccountSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountSettings
        fields = (
            "lang",
            "push_notifications",
        )


class _TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = fantasy_models.Team
        fields = (
            "id",
            "name",
        )


class AccountDetailSerializer(serializers.ModelSerializer):
    team = _TeamSerializer()
    account_settings = _AccountSettingsSerializer()

    class Meta:
        model = models.User
        fields = (
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "middle_name",
            "profile_picture",
            "date_of_birth",
            "balance",

            "team",
            "account_settings",
        )
