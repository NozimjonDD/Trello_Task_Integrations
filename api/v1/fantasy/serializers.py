from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.fantasy import models

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
