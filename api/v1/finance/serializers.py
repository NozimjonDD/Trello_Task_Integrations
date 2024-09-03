from rest_framework import serializers

from api.v1.users.serializers import UserTariffCaseListSerializer
from apps.finance.models import Tariff, Subscription


class TariffListSerializer(serializers.ModelSerializer):
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

    # def get_calc_all_tariff_price(self, obj):
    #     data = obj.calculate_total_price
    #     return data


class SubscriptionCreateSerilalizer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            "id",
            "user",
            "tariff",
            "total_price",
        )
