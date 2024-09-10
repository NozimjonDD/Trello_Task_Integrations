from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from api.v1.users.serializers import UserTariffCaseListSerializer
from apps.finance import models
from apps.common.data import TariffOrderStatusChoices


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


class CoinTariffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoinTariff
        fields = (
            "id",
            "title",
            "image",
            "coin_amount",
            "price",
            "discount_price",
        )


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


class TariffOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TariffOrder
        fields = (
            "id",
            "tariff_option",
        )
        extra_kwargs = {
            "tariff_option": {"required": True},
        }

    def validate(self, attrs):
        tariff_option = attrs["tariff_option"]

        price = tariff_option.price
        if tariff_option.discount_price:
            price = tariff_option.discount_price

        if price > self.context["request"].user.coin_balance:
            raise serializers.ValidationError(
                code="insufficient_coin_balance",
                detail={"coin_balance": [_(f"Insufficient coin balance.")]},
            )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        validated_data["tariff"] = validated_data["tariff_option"].tariff
        validated_data["price"] = validated_data["tariff_option"].price
        validated_data["discount_price"] = validated_data["tariff_option"].discount_price
        instance = super().create(validated_data)
        instance.apply_tariff_order()
        return instance


class CoinOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoinOrder
        fields = (
            "id",
            "coin_tariff",
            "payment_type",
            "status",
        )
        extra_kwargs = {
            "coin_tariff": {"required": True},
            "payment_type": {"required": True},
            "status": {"read_only": True},
        }

    @transaction.atomic
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        validated_data["price"] = validated_data["coin_tariff"].price
        validated_data["coin_amount"] = validated_data["coin_tariff"].coin_amount
        validated_data["status"] = TariffOrderStatusChoices.PAYMENT_PROCESSING

        if validated_data["coin_tariff"].discount_price:
            validated_data["price"] = validated_data["coin_tariff"].discount_price
        instance = super().create(validated_data)
        return instance
