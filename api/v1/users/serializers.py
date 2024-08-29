from django.conf import settings

from rest_framework import serializers

from apps.users import models
from apps.fantasy import models as fantasy_models
from apps.football import models as football_models

from api.v1 import common_serializers


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
            "status",
        )


class AccountDetailSerializer(serializers.ModelSerializer):
    team = _TeamSerializer()
    account_settings = _AccountSettingsSerializer()
    game_week = serializers.SerializerMethodField()

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
            "pretty_balance",

            "team",
            "account_settings",
            "game_week",
        )

    @staticmethod
    def get_game_week(obj):
        current_round = football_models.Round.objects.filter(
            league__remote_id=settings.PREMIER_LEAGUE_ID,
            season__is_current=True,
            is_current=True,
        ).first()
        return common_serializers.CommonRoundSerializer(current_round).data
