from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.fantasy import models
from apps.football import models as football_models
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
    # positions = _FormationPositionSerializer(many=True)

    class Meta:
        model = models.Formation
        fields = (
            "id",
            "title",
            # "positions",
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

        squad = models.Squad.objects.create(
            team=instance,
            formation=models.Formation.objects.get(scheme="4-3-3"),
            is_default=True,
        )
        for f_position in models.FormationPosition.objects.filter(formation__scheme="4-3-3"):
            models.SquadPlayer.objects.create(
                squad=squad,
                position=f_position,
                player=None,
                is_substitution=f_position.is_substitution,
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

    gk = serializers.SerializerMethodField()
    squad_players = serializers.SerializerMethodField()
    substitutes = serializers.SerializerMethodField()

    class Meta:
        model = models.Squad
        fields = (
            "id",
            "formation",
            "gk",
            "squad_players",
            "substitutes",
        )

    @staticmethod
    def get_squad_players(obj):
        squad_players = obj.players.filter(
            is_substitution=False
        ).exclude(position__position__short_name="GK").order_by("position__ordering")

        squad_players = list(squad_players)

        scheme = obj.formation.scheme

        result = []
        cnt = 0
        for i in scheme.split("-"):
            section = []
            for j in range(int(i)):
                section.append(_DefaultSquadPlayerSerializer(squad_players[cnt], many=False).data)
                cnt += 1
            result.append(section)

        return result

    @staticmethod
    def get_gk(obj):
        gk = obj.players.filter(
            is_substitution=False,
            position__position__short_name="GK"
        ).first()
        return _DefaultSquadPlayerSerializer(gk, many=False).data

    @staticmethod
    def get_substitutes(obj):
        substitutes = obj.players.filter(
            is_substitution=True
        ).order_by("position__ordering")
        return _DefaultSquadPlayerSerializer(substitutes, many=True).data


class TeamDetailSerializer(serializers.ModelSerializer):
    default_squad = _DefaultSquadSerializer(read_only=True)

    # team_players = _TeamPlayerSerializer(many=True)

    class Meta:
        model = models.Team
        fields = (
            "id",
            "name",
            "status",

            "default_squad",
            # "team_players",

            "created_at",
            "updated_at",
        )


class SquadDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Squad
        fields = (
            "id",
            "formation",
            "is_default",
        )
        extra_kwargs = {
            "is_default": {"read_only": True},
            "formation": {"required": True},
        }


class TransferSerializer(serializers.ModelSerializer):
    player = serializers.PrimaryKeyRelatedField(
        queryset=football_models.Player.objects.filter(is_deleted=False, club__league__remote_id=271)
    )
    squad_player = serializers.PrimaryKeyRelatedField(
        queryset=models.SquadPlayer.objects.filter(
            is_deleted=False, player=None, squad__is_default=True
        ),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = models.Transfer
        fields = (
            "id",
            "transfer_type",
            "team",
            "player",
            "swapped_player",
            "squad_player",
            "fee",
        )
        extra_kwargs = {
            "fee": {"read_only": True},
            "team": {"read_only": True},
        }

    def validate_squad_player(self, value):
        team = self.context["request"].user.p_team
        return value

    def validate(self, attrs):
        transfer_type = attrs["transfer_type"]
        team = self.context["request"].user.p_team
        player = attrs["player"]
        swapped_player = attrs.get("swapped_player", None)
        squad_player = attrs.get("squad_player", None)

        if not team:
            raise serializers.ValidationError(
                code="not_created",
                detail={"team": [_("You have not created a team!")]}
            )

        if transfer_type == TransferTypeChoices.BUY:
            if team.team_players.filter(is_deleted=False).count() >= 15:
                raise serializers.ValidationError(
                    code="full_team",
                    detail={"team": [_("You can transfer players upto 15.")]}
                )

            if team.team_players.filter(player__club_id=player.club.id).count() >= 3:
                raise serializers.ValidationError(
                    code="club_limit_reached",
                    detail={"player": [_("You can transfer upto 3 players from one club.")]}
                )

            if team.team_players.filter(player_id=player.id).exists():
                raise serializers.ValidationError(
                    code="player_already_transferred",
                    detail={"player": [_("You have already transferred this player.")]}
                )

            if not player.market_value or player.market_value > team.user.balance:
                raise serializers.ValidationError(
                    code="insufficient_balance",
                    detail={"player": [_("You do not have enough balance to buy this player.")]}
                )
            try:
                del attrs["swapped_player"]
            except KeyError:
                pass
        elif transfer_type == TransferTypeChoices.SELL:
            if not team.team_players.filter(player_id=player.id).exists():
                raise serializers.ValidationError(
                    code="team_player_doesnt_exists",
                    detail={"player": [_("This player is not your team player.")]}
                )
            if not player.market_value:
                raise serializers.ValidationError(
                    code="no_market_value",
                    detail={"player": [_("This player has no market value.")]}
                )
            try:
                del attrs["swapped_player"]
            except KeyError:
                pass
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
