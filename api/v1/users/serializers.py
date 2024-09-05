from rest_framework import serializers

from api.v1 import common_serializers
from apps.fantasy import models as fantasy_models
from apps.finance.models import Tariff, TariffCase, Subscription
from apps.football import models as football_models
from apps.users import models


class _AccountSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountSettings
        fields = (
            "lang",
            "push_notifications",
        )


class _TeamSerializer(serializers.ModelSerializer):
    level = common_serializers.CommonLevelSerializer(source="current_level")

    class Meta:
        model = fantasy_models.Team
        fields = (
            "id",
            "name",
            "status",

            "total_points",
            "level",
        )
        ref_name = "UserAccountTeamDetail"


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
            "coin_balance",
            "pretty_balance",

            "team",
            "account_settings",
            "game_week",
        )

    @staticmethod
    def get_game_week(obj):
        current_round = football_models.Round.get_coming_gw()
        return common_serializers.CommonRoundSerializer(current_round).data


class UserTariffCaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TariffCase
        fields = (
            "id",
            "title",
            "tariff",
            "amount",
            "price",
            "discount_price",
        )


class UserTariffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = (
            "id",
            "title",
            "description",
            "type",
            "price",
            "discount_price",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["tariff_cases"] = UserTariffCaseListSerializer(instance.tariff_cases.all(), many=True).data
        return data


class TariffDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = (
            "id",
            "title",
            "description",
            "type",
            "price",
            "discount_price",
        )


class SubscriptionListSerilalizer(serializers.ModelSerializer):
    tariffs = TariffDetailSerializer(source="tariff", many=True)

    class Meta:
        model = Subscription
        fields = (
            "id",
            "user",
            "tariffs",
            "total_price",
        )
