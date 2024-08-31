from django.db import models
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from apps.common.data import (
    LeagueStatusType, TeamStatusChoices, TransferTypeChoices, LeagueStatusChoices,
    LeagueParticipantStatusChoices
)
from apps.common.models import BaseModel
from apps.common import utils as common_utils
from . import utils


class Formation(BaseModel):
    class Meta:
        db_table = "formation"
        verbose_name = _("Squad formation")
        verbose_name_plural = _("Squad formations")

    title = models.CharField(max_length=255, null=True)
    scheme = models.CharField(
        max_length=50, unique=True, validators=[common_utils.formation_validator], null=True
    )
    ordering = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        from apps.football import models as football_models

        if self.pk and not self.positions.exists():
            # default scheme 4-3-3

            position = None
            is_substitution = False
            for i in range(1, 16):
                if i >= 12:
                    is_substitution = True

                if i == 1 or i == 12:
                    position = football_models.Position.objects.get(remote_id=24)
                elif 1 < i <= 5 or i == 13:
                    position = football_models.Position.objects.get(remote_id=25)
                elif 5 < i <= 8 or i in [14, 15]:
                    position = football_models.Position.objects.get(remote_id=26)
                elif 8 < i <= 11:
                    position = football_models.Position.objects.get(remote_id=27)

                FormationPosition.objects.create(
                    formation_id=self.pk,
                    position=position,
                    is_substitution=is_substitution,
                    ordering=i,
                )

    @property
    def scheme_as_list(self):
        return [int(i) for i in self.scheme.split("-")]


class FormationPosition(BaseModel):
    class Meta:
        db_table = "formation_position"
        verbose_name = _("Squad formation position")
        verbose_name_plural = _("Squad formation positions")

    formation = models.ForeignKey(
        to="fantasy.Formation",
        on_delete=models.CASCADE,
        related_name="positions",
        verbose_name=_("Formation")
    )
    position = models.ForeignKey(
        to="football.Position",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("Position"),
    )
    is_substitution = models.BooleanField(default=False, verbose_name=_("Is substitution"))
    ordering = models.IntegerField(verbose_name=_("Ordering"), default=1)

    def __str__(self):
        return f"{self.formation} - {self.ordering}"


class Team(BaseModel):
    class Meta:
        db_table = "fantasy_team"
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    user = models.OneToOneField(to="users.User", on_delete=models.CASCADE, related_name="team")
    name = models.CharField(verbose_name=_("Name"), max_length=255, null=True)
    status = models.CharField(choices=TeamStatusChoices.choices, default=TeamStatusChoices.DRAFT, max_length=100)

    def __str__(self):
        return str(self.name)

    @property
    def default_squad(self):
        squad = self.squads.filter(is_default=True).last()
        return squad


class TeamPlayer(BaseModel):
    class Meta:
        db_table = "fantasy_team_player"
        verbose_name = _("Team player")
        verbose_name_plural = _("Team players")
        unique_together = ("team", "player",)

    team = models.ForeignKey(to="fantasy.Team", on_delete=models.CASCADE, related_name="team_players")
    player = models.ForeignKey(
        to="football.Player",
        on_delete=models.CASCADE,
        related_name="team_players",
    )
    position = models.ForeignKey(to="football.Position", on_delete=models.SET_NULL, null=True)
    is_captain = models.BooleanField(default=False)
    is_substitution = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team} - {self.player}"


class Squad(BaseModel):
    class Meta:
        db_table = "fantasy_squad"
        verbose_name = _("Squad")
        verbose_name_plural = _("Squads")
        unique_together = ("team", "round",)

    team = models.ForeignKey(to="fantasy.Team", on_delete=models.CASCADE, related_name="squads", verbose_name=_("Team"))
    round = models.ForeignKey(
        to="football.Round", on_delete=models.CASCADE, related_name="+", verbose_name=_("Round"), null=True, blank=True
    )
    formation = models.ForeignKey(
        to="fantasy.Formation", on_delete=models.SET_NULL, null=True, verbose_name=_("Formation"), related_name="+"
    )
    is_default = models.BooleanField(verbose_name=_("Is default squad"), default=False)

    @classmethod
    @transaction.atomic
    def get_or_create_gw_squad(cls, team, rnd):
        """ If squad doesn't exists then duplicate current_squad to new round. """

        from apps.football import models as football_models

        try:
            squad = cls.objects.get(team=team, round=rnd)
            return squad
        except cls.DoesNotExist:
            pass

        try:
            current_squad = cls.objects.get(team=team, round=football_models.Round.get_coming_gw())
        except cls.DoesNotExist:
            current_squad = None

        if current_squad:
            formation = current_squad.formation
        else:
            formation = Formation.objects.get(scheme="4-3-3")

        squad = cls.objects.create(
            team=team,
            round=rnd,
            formation=formation,
        )
        cls.objects.filter(
            team_id=team.pk,
            round_id=football_models.Round.get_coming_gw().pk,
        ).update(is_default=True)
        cls.objects.filter(team_id=team.pk).exclude(
            round_id=football_models.Round.get_coming_gw().pk,
        ).update(is_default=False)

        if current_squad:
            for player in current_squad.players.all():
                SquadPlayer.objects.create(
                    squad=squad,
                    player=player.player,
                    position=player.position,
                    is_captain=player.is_captain,
                    is_substitution=player.is_substitution,
                )
        else:
            for position in formation.positions.all():
                SquadPlayer.objects.create(
                    squad=squad,
                    position=position,
                    is_substitution=position.is_substitution,
                )
        return squad

    def __str__(self):
        return f"{self.team} - {self.round}"


class SquadPlayer(BaseModel):
    class Meta:
        db_table = "fantasy_squad_player"
        verbose_name = _("Squad player")
        verbose_name_plural = _("Squad players")
        unique_together = ("squad", "player", "position")

    squad = models.ForeignKey(
        to="fantasy.Squad",
        on_delete=models.CASCADE,
        related_name="players",
        verbose_name=_("Squad"),
    )
    player = models.ForeignKey(
        to="fantasy.TeamPlayer",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Team player"),
        null=True,
        blank=True,
    )
    position = models.ForeignKey(
        to="fantasy.FormationPosition",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("Formation position"),
    )
    is_captain = models.BooleanField(default=False)
    is_substitution = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player} - {self.position}"


class Transfer(BaseModel):
    class Meta:
        db_table = "fantasy_player_transfer"
        verbose_name = _("Fantasy transfer")
        verbose_name_plural = _("Fantasy transfers")

    transfer_type = models.CharField(
        verbose_name=_("Transfer type"),
        max_length=100,
        choices=TransferTypeChoices.choices,
    )
    team = models.ForeignKey(
        to="fantasy.Team",
        on_delete=models.CASCADE,
        related_name="transfers",
        verbose_name=_("Team"),
    )
    player = models.ForeignKey(
        to="football.Player",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("Player"),
    )
    swapped_player = models.ForeignKey(
        to="football.Player",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Swapped player"),
        null=True, blank=True,
    )

    squad_player = models.ForeignKey(
        to="fantasy.SquadPlayer",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Squad player"),
        null=True,
        blank=True,
    )

    fee = models.DecimalField(
        verbose_name=_("Fee"),
        max_digits=18,
        decimal_places=2,
        help_text="£(pound sterling)"
    )

    def __str__(self):
        return f"{self.team} - {self.transfer_type} - £{self.fee}"

    def apply(self):
        if self.transfer_type == TransferTypeChoices.BUY:
            self.team.user.balance -= self.fee
            team_player = TeamPlayer.objects.create(
                team_id=self.team_id,
                player_id=self.player_id,
                position_id=self.player.position_id,
            )

            if self.squad_player:
                self.squad_player.player = team_player
                self.squad_player.save(update_fields=["player"])

        elif self.transfer_type == TransferTypeChoices.SELL:
            self.team.user.balance += self.fee
            try:
                team_player = TeamPlayer.objects.get(team_id=self.team_id, player_id=self.player_id)
                team_player.delete()
            except TeamPlayer.DoesNotExist:
                pass

        elif self.transfer_type == TransferTypeChoices.SWAP:
            self.team.user.balance -= self.fee

            try:
                team_player = TeamPlayer.objects.get(team_id=self.team_id, player_id=self.swapped_player_id)
                team_player.player = self.player
                team_player.save(update_fields=["player"])
            except TeamPlayer.DoesNotExist:
                pass

        self.team.user.save(update_fields=["balance"])


class FantasyLeague(BaseModel):
    class Meta:
        db_table = "fantasy_league"
        verbose_name = _("Fantasy league")
        verbose_name_plural = _("Fantasy leagues")

    owner = models.ForeignKey(
        to="users.User", verbose_name=_("Owner"), on_delete=models.CASCADE, related_name="fantasy_leagues"
    )
    title = models.CharField(verbose_name=_("Title"), max_length=255, null=True)
    description = models.TextField(verbose_name=_("Description"))
    type = models.CharField(verbose_name=_("Type"), choices=LeagueStatusType.choices, max_length=100)
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=50,
        choices=LeagueStatusChoices.choices,
        default=LeagueStatusChoices.PENDING,
    )
    invite_code = models.CharField(max_length=20, blank=True, null=True, unique=True)
    starting_round = models.ForeignKey(
        to="football.Round",
        verbose_name=_("Starting round"),
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )
    ending_round = models.ForeignKey(
        to="football.Round",
        verbose_name=_("Ending round"),
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk and self.type == LeagueStatusType.PRIVATE and not self.invite_code:
            self.generate_new_invite_code()
        super().save(*args, **kwargs)

    def generate_new_invite_code(self):
        self.invite_code = utils.generate_league_invite_code()
        self.save(update_fields=["invite_code"])


class LeagueParticipant(BaseModel):
    class Meta:
        db_table = "fantasy_league_participant"
        verbose_name = _("Fantasy league participant")
        verbose_name_plural = _("Fantasy league participant")
        unique_together = ("league", "team",)

    league = models.ForeignKey(
        to="fantasy.FantasyLeague",
        on_delete=models.CASCADE,
        related_name="league_participants",
        verbose_name=_("League"),
    )
    team = models.ForeignKey(
        to="fantasy.Team",
        on_delete=models.CASCADE,
        related_name="league_participants",
        verbose_name=_("Team"),
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=50,
        choices=LeagueParticipantStatusChoices.choices,
        default=LeagueParticipantStatusChoices.ACTIVE,
    )

    def __str__(self):
        return f"{self.league} - {self.team}"


# POINTS
class PlayerRoundPoint(BaseModel):
    class Meta:
        db_table = "fantasy_player_round_point"
        verbose_name = _("Fantasy player round point")
        verbose_name_plural = _("Fantasy player round points")
        unique_together = ("player", "round",)

    player = models.ForeignKey(
        to="football.Player",
        on_delete=models.CASCADE,
        related_name="round_points",
        verbose_name=_("Player"),
    )
    round = models.ForeignKey(
        to="football.Round",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("Round"),
    )
    total_point = models.DecimalField(
        verbose_name=_("Total points"),
        max_digits=18,
        decimal_places=2,
        default=0,
    )

    clean_sheet = models.DecimalField(
        verbose_name=_("clean sheet"),
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )
    minutes_played = models.DecimalField(
        verbose_name=_("Minutes played"),
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )
    goal = models.DecimalField(
        verbose_name=_("Goal"),
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )
    goal_conceded = models.DecimalField(
        verbose_name=_("Goal conceded"),
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )
    assist = models.DecimalField(
        verbose_name=_("Assist"),
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )
    saves = models.DecimalField(
        verbose_name=_("Saves"),
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )
    penalty_save = models.DecimalField(
        verbose_name=_("Penalty save"),
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )
    penalty_miss = models.DecimalField(
        verbose_name=_("Penalty miss"),
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )
    yellow_card = models.DecimalField(
        verbose_name=_("Yellow card"),
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )
    red_card = models.DecimalField(
        verbose_name=_("Red card"),
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.player} - {self.round} - {self.total_point}"

    def calculate_total_point(self):
        total_point = 0
        total_point += self.clean_sheet if self.clean_sheet else 0
        total_point += self.minutes_played if self.minutes_played else 0
        total_point += self.goal if self.goal else 0
        total_point += self.goal_conceded if self.goal_conceded else 0
        total_point += self.assist if self.assist else 0
        total_point += self.saves if self.saves else 0
        total_point += self.penalty_save if self.penalty_save else 0
        total_point += self.penalty_miss if self.penalty_miss else 0
        total_point += self.yellow_card if self.yellow_card else 0
        total_point += self.red_card if self.red_card else 0
        return total_point


class SquadPlayerRoundPoint(BaseModel):
    class Meta:
        db_table = "squad_player_round_point"
        verbose_name = _("Squad player round point")
        verbose_name_plural = _("Squad player round points")

    squad_player = models.OneToOneField(
        to="fantasy.SquadPlayer",
        verbose_name=_("Squad player"),
        on_delete=models.CASCADE,
        related_name="round_point",
    )
    round = models.ForeignKey(
        to="football.Round",
        verbose_name=_("Round"),
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )
    player_point = models.ForeignKey(
        to="fantasy.PlayerRoundPoint",
        verbose_name=_("Player round point"),
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )
    total_point = models.DecimalField(
        verbose_name=_("Points"),
        max_digits=18,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        return f"{self.squad_player} - {self.total_point}"


class TeamRoundPoint(BaseModel):
    class Meta:
        db_table = "fantasy_team_round_point"
        verbose_name = _("Fantasy team round point")
        verbose_name_plural = _("Fantasy team round points")
        unique_together = ("team", "round",)

    team = models.ForeignKey(
        to="fantasy.Team",
        on_delete=models.CASCADE,
        related_name="round_points",
        verbose_name=_("Team"),
    )
    squad = models.OneToOneField(
        to="fantasy.Squad",
        on_delete=models.SET_NULL,
        related_name="round_point",
        verbose_name=_("Squad"),
        null=True,
    )
    round = models.ForeignKey(
        to="football.Round",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("Round"),
    )
    total_point = models.DecimalField(
        verbose_name=_("Points"),
        max_digits=18,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        return f"{self.team} - {self.round} - {self.total_point}"

    def calculate_total_point(self):
        data = SquadPlayerRoundPoint.objects.filter(
            squad_player__squad_id=self.squad_id,
            round_id=self.round_id,
        ).aggregate(
            total_point=models.Sum("total_point")
        )
        return data["total_point"] or 0
