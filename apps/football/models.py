from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.common import utils as common_utils


class FootballBaseModel(BaseModel):
    class Meta:
        abstract = True

    remote_id = models.PositiveIntegerField(verbose_name=_("remote id"), unique=True)


class League(FootballBaseModel):
    class Meta:
        db_table = "league"
        verbose_name = _("League")
        verbose_name_plural = _("Leagues")

    name = models.CharField(max_length=200, verbose_name=_("Name"))
    short_code = models.CharField(max_length=50, verbose_name=_("Short code"), null=True, blank=True)
    image_path = models.URLField(verbose_name=_("Image path"))
    type = models.CharField(verbose_name=_("Type"), max_length=100)
    sub_type = models.CharField(verbose_name=_("Sub type"), max_length=100)
    category_id = models.IntegerField()
    has_jerseys = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Season(FootballBaseModel):
    class Meta:
        db_table = "season"

    name = models.CharField(max_length=200, verbose_name=_("Name"))
    league = models.ForeignKey(
        to="League",
        on_delete=models.CASCADE,
        related_name="seasons",
        verbose_name=_("League"),
    )
    is_finished = models.BooleanField(verbose_name=_("Is finished"), default=False)
    pending = models.BooleanField(verbose_name=_("Pending"), default=False)
    is_current = models.BooleanField(verbose_name=_("Is current"), default=False)
    starting_at = models.DateField(verbose_name=_("Starting at"))
    ending_at = models.DateField(verbose_name=_("Ending at"))
    games_in_current_week = models.BooleanField(verbose_name=_("Games in current week"), default=False)

    def __str__(self):
        return f"{self.league} - {self.name}"


class Round(FootballBaseModel):
    class Meta:
        db_table = "round"

    name = models.CharField(max_length=200, verbose_name=_("Name"))
    league = models.ForeignKey(
        to="League",
        on_delete=models.CASCADE,
        related_name="rounds",
        verbose_name=_("League"),
    )
    season = models.ForeignKey(
        to="Season",
        on_delete=models.CASCADE,
        related_name="rounds",
        verbose_name=_("Season"),
    )
    is_finished = models.BooleanField(verbose_name=_("Is finished"), default=False)
    is_current = models.BooleanField(verbose_name=_("Is current"), default=False)
    starting_at = models.DateField(verbose_name=_("Starting at"))
    ending_at = models.DateField(verbose_name=_("Ending at"))
    games_in_current_week = models.BooleanField(verbose_name=_("Games in current week"), default=False)

    def __str__(self):
        return self.name


class FixtureState(FootballBaseModel):
    class Meta:
        db_table = "fixture_state"

    state = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    short_title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Fixture(FootballBaseModel):
    class Meta:
        db_table = "fixture"

    season = models.ForeignKey(
        to="Season",
        on_delete=models.CASCADE,
        related_name="fixtures",
        verbose_name=_("Season"),
    )
    round = models.ForeignKey(
        to="Round",
        on_delete=models.CASCADE,
        related_name="fixtures",
        verbose_name=_("Round")
    )
    venue_id = models.IntegerField(null=True, blank=True)

    title = models.CharField(max_length=100)
    home_club = models.ForeignKey(
        to="Club", on_delete=models.CASCADE, related_name="home_matches", verbose_name=_("Home club")
    )
    away_club = models.ForeignKey(
        to="Club", on_delete=models.CASCADE, related_name="away_matches", verbose_name=_("Away club")
    )
    state = models.ForeignKey(
        to="FixtureState", on_delete=models.SET_NULL, related_name="+", verbose_name=_("State"), null=True, blank=True
    )
    home_club_score = models.IntegerField(null=True, blank=True)
    away_club_score = models.IntegerField(null=True, blank=True)

    result_info = models.CharField(verbose_name=_("Result info"), null=True, blank=True)
    match_date = models.DateTimeField()
    length = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class Club(FootballBaseModel):
    class Meta:
        db_table = "football_club"

    name = models.CharField(max_length=200, verbose_name=_("Name"))
    league = models.ForeignKey(
        to="football.League",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("League"),
        null=True,
        blank=True,
    )
    short_name = models.CharField(max_length=50, verbose_name=_("Short name"), null=True, blank=True)
    country_id = models.IntegerField()
    venue_id = models.IntegerField()
    logo = models.ImageField(upload_to="football/club/logo/", null=True, blank=True)
    logo_path = models.URLField()
    kit = models.ImageField(upload_to="football/club/kit/", null=True, blank=True)
    founded_year = models.PositiveSmallIntegerField()
    type = models.CharField(verbose_name=_("Club type"), max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Position(FootballBaseModel):
    class Meta:
        db_table = "position"

    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=20, null=True)
    code = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Player(FootballBaseModel):
    class Meta:
        db_table = "player"

    club = models.ForeignKey(
        to="Club", on_delete=models.CASCADE, related_name="players", verbose_name=_("Club"), null=True
    )
    position = models.ForeignKey(to="Position", on_delete=models.SET_NULL, related_name="players", null=True)
    country_id = models.IntegerField(null=True)
    nationality_id = models.IntegerField(null=True)
    profile_picture = models.ImageField(upload_to="football/player/profile_picture/", null=True, blank=True)
    profile_picture_path = models.URLField()

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    common_name = models.CharField(max_length=200)

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)

    club_contract_until = models.DateField(null=True, blank=True)
    market_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.full_name

    @property
    def age(self):
        from datetime import date

        if not self.date_of_birth:
            return None
        today = date.today()
        age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

    @property
    def pretty_market_value(self):
        if not self.market_value:
            return None

        return common_utils.pretty_price(self.market_value)


class ClubPlayer(FootballBaseModel):
    class Meta:
        db_table = "club_player"

    club = models.ForeignKey(to="Club", on_delete=models.CASCADE, related_name="club_players", verbose_name=_("Club"))
    player = models.ForeignKey(to="Player", on_delete=models.CASCADE, related_name="club_players")
    position = models.ForeignKey(to="Position", on_delete=models.SET_NULL, related_name="+", null=True)

    transfer_id = models.IntegerField(null=True)
    start_date = models.DateField(verbose_name=_("Start date"), null=True)
    end_date = models.DateField(verbose_name=_("End date"), null=True)
    is_captain = models.BooleanField(default=False)
    kit_number = models.IntegerField(null=True, blank=True)
    is_current_club = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player} - {self.club}"
