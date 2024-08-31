from django.db import transaction
from django.conf import settings

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.fantasy import models
from apps.football import models as football_models
from apps.common.data import TransferTypeChoices, LeagueStatusType, LeagueStatusChoices

from api.v1 import common_serializers
from api.v1.football.serializers import PlayerDetailSerializer


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
            round=football_models.Round.get_coming_gw(),
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


class _SquadPRoundPointSerializer(serializers.ModelSerializer):
    total_point = serializers.IntegerField()

    class Meta:
        model = models.SquadPlayerRoundPoint
        fields = (
            "id",
            "round",
            "total_point",
        )


class _SquadRoundPointSerializer(serializers.ModelSerializer):
    total_point = serializers.IntegerField()

    class Meta:
        model = models.TeamRoundPoint
        fields = (
            "id",
            "round",
            "total_point",
        )


class _DefaultSquadPlayerSerializer(serializers.ModelSerializer):
    team_player = _TeamPlayerSerializer(source="player")
    team_position = common_serializers.CommonFormationPositionSerializer(source="position")
    round_point = _SquadPRoundPointSerializer()

    class Meta:
        model = models.SquadPlayer
        fields = (
            "id",
            "team_position",
            "team_player",
            "is_captain",
            "is_substitution",
            "round_point",
        )


class _DefaultSquadSerializer(serializers.ModelSerializer):
    formation = common_serializers.CommonFormationSerializer()

    gk = serializers.SerializerMethodField()
    squad_players = serializers.SerializerMethodField()
    substitutes = serializers.SerializerMethodField()
    round_point = _SquadRoundPointSerializer()
    transfer_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Squad
        fields = (
            "id",
            "formation",
            "gk",
            "squad_players",
            "substitutes",

            "round_point",
            "transfer_count",
        )

    def get_squad_players(self, obj):
        squad_players = obj.players.filter(
            is_substitution=False
        ).exclude(position__position__short_name="GK").order_by("position__position__remote_id", "position__ordering")

        squad_players = list(squad_players)

        scheme = obj.formation.scheme

        result = []
        cnt = 0
        for i in scheme.split("-"):
            section = []
            for j in range(int(i)):
                section.append(_DefaultSquadPlayerSerializer(squad_players[cnt], many=False, context=self.context).data)
                cnt += 1
            result.append(section)

        return result

    def get_gk(self, obj):
        gk = obj.players.filter(
            is_substitution=False,
            position__position__short_name="GK"
        ).first()
        return _DefaultSquadPlayerSerializer(gk, many=False, context=self.context).data

    def get_substitutes(self, obj):
        substitutes = obj.players.filter(
            is_substitution=True
        ).order_by("position__position__remote_id", "position__ordering")
        return _DefaultSquadPlayerSerializer(substitutes, many=True, context=self.context).data

    @staticmethod
    def get_transfer_count(obj):
        total_count = models.Transfer.objects.filter(squad_player__squad_id=obj.id).count()
        return total_count


class TeamDetailSerializer(serializers.ModelSerializer):
    default_squad = serializers.SerializerMethodField()

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

    def get_default_squad(self, obj):
        rnd_id = self.context["round"]
        try:
            rnd = football_models.Round.objects.get(id=int(rnd_id))
        except (TypeError, football_models.Round.DoesNotExist):
            rnd = football_models.Round.get_coming_gw()

        if rnd.starting_at > football_models.Round.get_coming_gw().starting_at:
            rnd = football_models.Round.get_coming_gw()

        squad = models.Squad.get_or_create_gw_squad(obj, rnd)

        return _DefaultSquadSerializer(squad, many=False, context=self.context).data


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

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        scheme = instance.formation.scheme

        squad_players = instance.players.filter(
            is_substitution=False
        ).exclude(position__position__short_name="GK").order_by("position__position__remote_id", "position__ordering")

        squad_players = list(squad_players)

        cnt = 0
        for index, i in enumerate(scheme.split("-")):
            for j in range(int(i)):
                if index == 0:
                    if squad_players[cnt].position.position.short_name != "DF":
                        swap_squad_player = instance.players.filter(
                            is_substitution=True,
                            position__position__short_name="DF"
                        ).order_by("position__ordering").first()

                        swap_squad_player.is_substitution = False
                        squad_players[cnt].is_substitution = True
                        squad_players[cnt].save(update_fields=["is_substitution"])
                        swap_squad_player.save(update_fields=["is_substitution"])

                elif index == 1:
                    if squad_players[cnt].position.position.short_name != "MF":
                        swap_squad_player = instance.players.filter(
                            is_substitution=True,
                            position__position__short_name="MF"
                        ).order_by("position__ordering").first()

                        swap_squad_player.is_substitution = False
                        squad_players[cnt].is_substitution = True
                        squad_players[cnt].save(update_fields=["is_substitution"])
                        swap_squad_player.save(update_fields=["is_substitution"])
                elif index in [2, 3]:
                    if squad_players[cnt].position.position.short_name != "ATK":
                        swap_squad_player = instance.players.filter(
                            is_substitution=True,
                            position__position__short_name="ATK"
                        ).order_by("position__ordering").first()

                        swap_squad_player.is_substitution = False
                        squad_players[cnt].is_substitution = True
                        squad_players[cnt].save(update_fields=["is_substitution"])
                        swap_squad_player.save(update_fields=["is_substitution"])
                cnt += 1

        return instance


class _SquadPlayerDetailTMPlayerSerializer(serializers.ModelSerializer):
    player = PlayerDetailSerializer()

    class Meta:
        model = models.TeamPlayer
        fields = (
            "id",
            "player",
        )


class SquadPlayerDetailUpdateSerializer(serializers.ModelSerializer):
    team_player = _SquadPlayerDetailTMPlayerSerializer(read_only=True, source="player")

    class Meta:
        model = models.SquadPlayer
        fields = (
            "id",
            "is_captain",
            "team_player",
        )
        extra_kwargs = {
            "is_captain": {"required": True, "allow_null": False},
            "team_player": {"read_only": True, },
        }

    def validate(self, attrs):
        if not attrs["is_captain"]:
            raise serializers.ValidationError(
                code="invalid_value",
                detail={"is_captain": [_("You can only mark as is_captain.")]}
            )
        if self.instance.is_substitution:
            raise serializers.ValidationError(
                code="not_allowed",
                detail={"is_captain": [_("You can't mark as captain substitute players.")]}
            )
        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.squad.players.exclude(id=instance.pk).update(is_captain=False)
        return instance


class SquadSubstituteSerializer(serializers.ModelSerializer):
    taken_off_player = serializers.CharField()
    subbed_on_player = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["taken_off_player"] = serializers.PrimaryKeyRelatedField(
            queryset=models.SquadPlayer.objects.filter(
                is_deleted=False,
                squad__team__user_id=self.context["request"].user.id,
                is_substitution=False,
            ),
            write_only=True,
        )
        self.fields["subbed_on_player"] = serializers.PrimaryKeyRelatedField(
            queryset=models.SquadPlayer.objects.filter(
                is_deleted=False,
                squad__team__user_id=self.context["request"].user.id,
                is_substitution=True,
            ),
            write_only=True,
        )

    class Meta:
        model = models.SquadPlayer
        fields = (
            "taken_off_player",
            "subbed_on_player",
        )

    def validate(self, attrs):
        taken_off_player = attrs["taken_off_player"]
        subbed_on_player = attrs["subbed_on_player"]

        if taken_off_player.squad_id != subbed_on_player.squad_id:
            raise serializers.ValidationError(
                code="same_squad_required",
                detail={"squad": [_("You can only swap squad players in same squad.")]}
            )

        if taken_off_player.position.position != taken_off_player.position.position:
            raise serializers.ValidationError(
                code="same_position_required",
                detail={"position": [_("You can only swap squad players in same position for now.")]}
            )

        if taken_off_player.is_captain:
            raise serializers.ValidationError(
                code="choose_other_captain_first",
                detail={"taken_off_player": [_("First you should choose other captain.")]}
            )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        taken_off_player = validated_data.pop("taken_off_player")
        subbed_on_player = validated_data.pop("subbed_on_player")

        temp_player = subbed_on_player.player
        subbed_on_player.player = taken_off_player.player
        taken_off_player.player = temp_player

        subbed_on_player.save(update_fields=["player"])
        taken_off_player.save(update_fields=["player"])
        return subbed_on_player


class TransferSerializer(serializers.ModelSerializer):
    player = serializers.PrimaryKeyRelatedField(
        queryset=football_models.Player.objects.filter(
            is_deleted=False,
            club__league__remote_id=settings.PREMIER_LEAGUE_ID,
        )
    )
    squad_player = serializers.PrimaryKeyRelatedField(
        queryset=models.SquadPlayer.objects.filter(
            is_deleted=False, squad__is_default=True
        ),
        required=False,
        allow_null=True,
    )
    swapped_player = serializers.PrimaryKeyRelatedField(
        queryset=football_models.Player.objects.filter(
            is_deleted=False,
            club__league__remote_id=settings.PREMIER_LEAGUE_ID,
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
            if not swapped_player:
                raise serializers.ValidationError(
                    code="required",
                    detail={"swapped_player": [_("This field is required.")]}
                )
            if not team.team_players.filter(player_id=swapped_player.id).exists():
                raise serializers.ValidationError(
                    code="team_player_doesnt_exists",
                    detail={"swapped_player": [_("This player is not your team player.")]}
                )

            if team.team_players.filter(player_id=player.id).exists():
                raise serializers.ValidationError(
                    code="already_exists",
                    detail={"player": [_("This player is already in your team.")]}
                )

            if player.club_id != swapped_player.club_id and team.team_players.filter(
                    player__club_id=player.club.id).count() >= 3:
                raise serializers.ValidationError(
                    code="club_limit_reached",
                    detail={"player": [_("You can transfer upto 3 players from one club.")]}
                )

            if not player.market_value or player.market_value - swapped_player.market_value > team.user.balance:
                raise serializers.ValidationError(
                    code="insufficient_balance",
                    detail={"player": [_("You do not have enough balance to buy this player.")]}
                )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        team = self.context["request"].user.p_team
        transfer_type = validated_data["transfer_type"]

        validated_data["team"] = team
        validated_data["fee"] = 0
        if transfer_type in [TransferTypeChoices.BUY, TransferTypeChoices.SELL]:
            validated_data["fee"] = validated_data["player"].market_value
        elif transfer_type == TransferTypeChoices.SWAP:
            validated_data["fee"] = validated_data["player"].market_value - validated_data[
                "swapped_player"].market_value

        instance = super().create(validated_data)

        instance.apply()
        return instance


class PublicLeagueListSerializer(serializers.ModelSerializer):
    joined = serializers.BooleanField()

    class Meta:
        model = models.FantasyLeague
        fields = (
            "id",
            "title",
            "description",
            "type",
            "status",
            "joined",
            "created_at",
        )


class LeagueCreateSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=[LeagueStatusType.PRIVATE])
    starting_round = serializers.PrimaryKeyRelatedField(
        queryset=football_models.Round.objects.filter(
            is_deleted=False,
            is_finished=False,
            season__league_id=settings.PREMIER_LEAGUE_ID,
        )
    )
    ending_round = serializers.PrimaryKeyRelatedField(
        queryset=football_models.Round.objects.filter(
            is_deleted=False,
            is_finished=False,
            season__league_id=settings.PREMIER_LEAGUE_ID,
        )
    )

    class Meta:
        model = models.FantasyLeague
        fields = (
            "id",
            "title",
            "type",
            "description",
            "status",
            "starting_round",
            "ending_round",
            "invite_code",
        )
        extra_kwargs = {
            "status": {"read_only": True},
            "invite_code": {"read_only": True},
            "title": {"required": True},
        }

    @transaction.atomic
    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        instance = super().create(validated_data)
        instance.generate_new_invite_code()

        models.LeagueParticipant.objects.create(
            league_id=instance.pk,
            team_id=self.context["request"].user.team.pk,
        )
        return instance


class LeagueJoinSerializer(serializers.ModelSerializer):
    league_type = serializers.ChoiceField(choices=LeagueStatusType.choices, write_only=True)
    league = serializers.PrimaryKeyRelatedField(
        queryset=models.FantasyLeague.objects.filter(
            is_deleted=False, type=LeagueStatusType.PUBLIC, status=LeagueStatusChoices.ACTIVE,
        ),
        required=False,
        allow_null=True,
    )
    invite_code = serializers.CharField(required=False, allow_null=True, min_length=4, max_length=50, write_only=True)

    class Meta:
        model = models.LeagueParticipant
        fields = (
            "id",
            "league_type",
            "league",
            "invite_code",
        )

    def validate(self, attrs):
        league_type = attrs["league_type"]
        league = attrs.get("league", None)
        invite_code = attrs.get("invite_code", None)

        team = self.context["request"].user.p_team

        if league_type == LeagueStatusType.PUBLIC:
            if not league:
                raise serializers.ValidationError(
                    code="league_required",
                    detail={"league": [_("League is required to join a public league.")]}
                )
            if models.LeagueParticipant.objects.filter(league_id=league.pk, team_id=team.pk).exists():
                raise serializers.ValidationError(
                    code="already_joined",
                    detail={"league": [_("You have already joined to this public league.")]}
                )
        elif league_type == LeagueStatusType.PRIVATE:
            if not invite_code:
                raise serializers.ValidationError(
                    code="invite_code_required",
                    detail={"invite_code": [_("Invite code is required to join a private league.")]}
                )
            try:
                private_l = models.FantasyLeague.objects.get(
                    type=LeagueStatusType.PRIVATE,
                    status=LeagueStatusChoices.ACTIVE,
                    invite_code=invite_code,
                )
            except models.FantasyLeague.DoesNotExist:
                raise serializers.ValidationError(
                    code="invite_code_invalid",
                    detail={"invite_code": [_("Invalid invite code entered.")]}
                )

            if models.LeagueParticipant.objects.filter(league_id=private_l.pk, team_id=team.pk).exists():
                raise serializers.ValidationError(
                    code="already_joined",
                    detail={"invite_code": [_("You have already joined to this private league.")]}
                )
            attrs["league"] = private_l

        try:
            del attrs["invite_code"]
        except KeyError:
            pass
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop("league_type")
        validated_data["team"] = self.context["request"].user.p_team
        return super().create(validated_data)
