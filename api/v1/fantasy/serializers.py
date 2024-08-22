from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.fantasy import models
from apps.common.data import TransferTypeChoices

from api.v1 import common_serializers


class _FormationPositionSerializer(serializers.ModelSerializer):
    position__id = serializers.IntegerField(source="position.pk")
    position__name = serializers.StringRelatedField(source="position.name")
    position__short_name = serializers.StringRelatedField(source="position.short_name")

    class Meta:
        model = models.FormationPosition
        fields = (
            "id",
            "index",
            "position__id",
            "position__name",
            "position__short_name",
        )


class FormationListSerializer(serializers.ModelSerializer):
    positions = _FormationPositionSerializer(many=True)

    class Meta:
        model = models.Formation
        fields = (
            "id",
            "title",
            "positions",
        )


class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = (
            "id",
            "name",
            "status",
        )
        extra_kwargs = {
            "status": {"read_only": True},
            "name": {"required": True},
        }

    def validate(self, attrs):
        if hasattr(self.context["request"].user, "team"):
            raise serializers.ValidationError(
                code="already_exists",
                detail={"name": _("You have already created a team!")}
            )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user

        instance = super().create(validated_data)

        models.Squad.objects.create(
            team=instance,
            formation=models.Formation.objects.get(scheme="4-3-3"),
            is_default=True,
        )
        return instance


class _TeamPlayerSerializer(serializers.ModelSerializer):
    player = common_serializers.CommonPlayerSerializer()
    team_position = common_serializers.CommonPositionSerializer(source="position")

    class Meta:
        model = models.TeamPlayer
        fields = (
            "id",
            "player",
            "team_position",
        )


class _DefaultSquadPlayerSerializer(serializers.ModelSerializer):
    team_player = _TeamPlayerSerializer(source="player")
    team_position = common_serializers.CommonFormationPositionSerializer(source="position")

    class Meta:
        model = models.SquadPlayer
        fields = (
            "id",
            "team_position",
            "team_player",
            "is_captain",
            "is_substitution",
        )


class _DefaultSquadSerializer(serializers.ModelSerializer):
    formation = common_serializers.CommonFormationSerializer()
    squad_players = _DefaultSquadPlayerSerializer(many=True, source="players")

    class Meta:
        model = models.Squad
        fields = (
            "id",
            "formation",
            "squad_players",
        )


class TeamDetailSerializer(serializers.ModelSerializer):
    default_squad = _DefaultSquadSerializer(read_only=True)
    team_players = _TeamPlayerSerializer(many=True)

    class Meta:
        model = models.Team
        fields = (
            "id",
            "name",
            "status",

            "default_squad",
            "team_players",

            "created_at",
            "updated_at",
        )


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transfer
        fields = (
            "id",
            "transfer_type",
            "team",
            "player",
            "swapped_player",
            "fee",
        )
        extra_kwargs = {
            "fee": {"read_only": True},
            "team": {"read_only": True},
        }

    def validate(self, attrs):
        transfer_type = attrs["transfer_type"]
        team = self.context["request"].user.p_team
        player = attrs["player"]
        swapped_player = attrs.get("swapped_player", None)

        if not team:
            raise serializers.ValidationError(
                code="not_created",
                detail={"team": [_("You have not created a team!")]}
            )

        if team.team_players.filter(is_deleted=False).count() >= 15:
            raise serializers.ValidationError(
                code="full_team",
                detail={"team": [_("Your team is full!")]}
            )

        if transfer_type == TransferTypeChoices.BUY:
            if not player.market_value or player.market_value > team.user.balance:
                raise serializers.ValidationError(
                    code="insufficient_balance",
                    detail={"player": [_("You do not have enough balance to buy this player!")]}
                )
            try:
                del attrs["swapped_player"]
            except KeyError:
                pass

        elif transfer_type == TransferTypeChoices.SELL:
            raise serializers.ValidationError("Not implemented!")
        elif transfer_type == TransferTypeChoices.SWAP:
            raise serializers.ValidationError("Not implemented!")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        team = self.context["request"].user.p_team
        transfer_type = validated_data["transfer_type"]

        validated_data["team"] = team
        validated_data["fee"] = 0
        if transfer_type in [TransferTypeChoices.BUY, TransferTypeChoices.SELL]:
            validated_data["fee"] = validated_data["player"].market_value
        instance = super().create(validated_data)

        instance.apply()
        return instance
