from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.data import LeagueStatusType, TeamStatusChoices
from apps.common.models import BaseModel
from apps.common import utils as common_utils


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
    index = models.IntegerField(verbose_name=_("Index"), default=0)
    coordinate_x = models.IntegerField(verbose_name=_("Coordinate X"), default=0)
    coordinate_y = models.IntegerField(verbose_name=_("Coordinate Y"), default=0)

    def __str__(self):
        return f"{self.formation} - [{self.coordinate_x}:{self.coordinate_y}]"


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


class TeamPlayer(BaseModel):
    class Meta:
        db_table = "fantasy_team_player"
        verbose_name = _("Team player")
        verbose_name_plural = _("Team players")

    team = models.ForeignKey(to="fantasy.Team", on_delete=models.CASCADE, related_name="team_players")
    player = models.ForeignKey(to="football.Player", on_delete=models.CASCADE, related_name="+")
    position = models.ForeignKey(to="football.Position", on_delete=models.SET_NULL, null=True)
    formation_position = models.ForeignKey(
        to="fantasy.FormationPosition",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Formation position"),
        null=True,
        blank=True,
    )
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

    squad = models.ForeignKey(
        to="fantasy.Squad",
        on_delete=models.CASCADE,
        related_name="players",
        verbose_name=_("Squad"),
    )
    player = models.ForeignKey(
        to="fantasy.TeamPlayer",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("Team player")
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
    invite_code = models.CharField(max_length=50, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title


class LeagueParticipant(BaseModel):
    class Meta:
        db_table = "fantasy_league_participant"
        verbose_name = _("Fantasy league participant")
        verbose_name_plural = _("Fantasy league participant")

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

    def __str__(self):
        return f"{self.league} - {self.team}"
