from rest_framework import serializers

from apps.finance.models import Tariff


class TariffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = (
            "id",
            "title",
            "description",
            "type",
            "annual_price",
            "monthly_price",
        )


class TariffJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = (
            "id",
            "title",
            "description",
            "type",
            "annual_price",
            "monthly_price",
        )
