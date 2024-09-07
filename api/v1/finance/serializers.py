from rest_framework import serializers

from api.v1.users.serializers import UserTariffCaseListSerializer
from apps.finance import models


class TariffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tariff
        fields = (
            "id",
            "title",
            "description",
            "type",
            # "price",
            # "discount_price",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["tariff_cases"] = UserTariffCaseListSerializer(instance.tariff_cases.all(), many=True).data
        return data


class TariffOptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TariffOption
        fields = (
            "id",
            "title",
            "amount",
            "price",
            "discount_price",
        )
