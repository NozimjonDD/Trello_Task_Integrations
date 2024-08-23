from django.db import models
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

    team = models.ForeignKey(to="fantasy.Team", on_delete=models.CASCADE, related_name="squads", verbose_name=_("Team"))
    round = models.ForeignKey(
        to="football.Round", on_delete=models.CASCADE, related_name="+", verbose_name=_("Round"), null=True, blank=True
    )
    formation = models.ForeignKey(
        to="fantasy.Formation", on_delete=models.SET_NULL, null=True, verbose_name=_("Formation"), related_name="+"
    )
    is_default = models.BooleanField(verbose_name=_("Is default squad"), default=False)

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
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

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
