from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.common import utils as common_utils
from apps.common.models import BaseModel


class FootballBaseModel(BaseModel):
    class Meta:
        abstract = True

    remote_id = models.BigIntegerField(verbose_name=_("remote id"), unique=True)


class SportMonksType(FootballBaseModel):
    class Meta:
        db_table = "sportmonks_type"
        verbose_name = _("SportMonks Type")
        verbose_name_plural = _("SportMonks Types")

    name = models.CharField(max_length=200, verbose_name=_("Name"))
    code = models.CharField(max_length=100, verbose_name=_("Code"))
    developer_name = models.CharField(max_length=100, verbose_name=_("Developer name"))
    model_type = models.CharField(max_length=100, verbose_name=_("Model type"))

    def __str__(self):
        return self.name


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

    @classmethod
    def get_current_gw(cls):
        gw = cls.objects.filter(is_current=True).first()
        return gw

    @classmethod
    def get_coming_gw(cls):
        gw = cls.objects.filter(starting_at__gt=timezone.now().today()).order_by("starting_at").first()
        return gw


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


class FixtureEvent(FootballBaseModel):
    class Meta:
        db_table = "fixture_event"
        verbose_name = _("Fixture event")
        verbose_name_plural = _("Fixture events")

    fixture = models.ForeignKey(
        to="football.Fixture",
        verbose_name=_("Fixture"),
        on_delete=models.CASCADE,
        related_name="events",
    )
    type = models.ForeignKey(
        to="football.SportMonksType",
        verbose_name=_("Type"),
        on_delete=models.CASCADE,
        related_name="+",
    )
    sub_type = models.ForeignKey(
        to="football.SportMonksType",
        verbose_name=_("Sub type"),
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True
    )
    club = models.ForeignKey(
        to="football.Club",
        verbose_name=_("Club"),
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
    )
    player = models.ForeignKey(
        to="football.Player",
        verbose_name=_("Player"),
        on_delete=models.CASCADE,
        related_name="fixture_events",
    )
    related_player = models.ForeignKey(
        to="football.Player",
        verbose_name=_("Related Player"),
        on_delete=models.SET_NULL,
        related_name="related_fixture_events",
        null=True,
        blank=True,
    )
    minute = models.IntegerField(verbose_name=_("Minute"))
    extra_minute = models.IntegerField(verbose_name=_("Extra minute"), null=True, blank=True)
    injured = models.BooleanField(verbose_name=_("Injured"), null=True, blank=True)
    on_bench = models.BooleanField(verbose_name=_("On bench"), null=True, blank=True)
    result = models.CharField(verbose_name=_("Result"), null=True, blank=True)
    info = models.CharField(verbose_name=_("Info"), null=True, blank=True)

    def __str__(self):
        return f"{self.fixture} - {self.type}"


class FixtureStatistic(FootballBaseModel):
    class Meta:
        db_table = "fixture_statistic"
        verbose_name = _("Fixture statistic")
        verbose_name_plural = _("Fixture statistics")

    fixture = models.ForeignKey(
        to="Fixture", on_delete=models.CASCADE, related_name="statistics", verbose_name=_("Fixture")
    )
    type = models.ForeignKey(
        to="SportMonksType", on_delete=models.CASCADE, related_name="+", verbose_name=_("Type")
    )
    club = models.ForeignKey(
        to="Club", on_delete=models.CASCADE, related_name="+", verbose_name=_("Club")
    )
    value = models.IntegerField(verbose_name=_("Value"))
    location = models.CharField(max_length=100, verbose_name=_("Location"))
    data = models.JSONField(verbose_name=_("Data"), null=True, blank=True)

    def __str__(self):
        return f"{self.fixture} - {self.type}"


class Lineup(FootballBaseModel):
    class Meta:
        db_table = "lineup"
        verbose_name = _("Fixture lineup")
        verbose_name_plural = _("Fixture lineups")
        unique_together = ("fixture", "player",)

    fixture = models.ForeignKey(
        to="Fixture", on_delete=models.CASCADE, related_name="lineups", verbose_name=_("Fixture")
    )
    club = models.ForeignKey(
        to="football.Club",
        verbose_name=_("Club"),
        on_delete=models.CASCADE,
        related_name="+",
    )
    player = models.ForeignKey(
        to="football.Player",
        verbose_name=_("Player"),
        on_delete=models.CASCADE,
        related_name="+",
    )
    type = models.ForeignKey(
        to="football.SportMonksType",
        verbose_name=_("Type"),
        on_delete=models.CASCADE,
        related_name="+",
    )

    def __str__(self):
        return f"{self.player} - {self.fixture} - {self.type}"


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
    jersey_number = models.IntegerField(verbose_name=_("Jersey number"), null=True, blank=True)
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

    def calculate_round_points(self, rnd):
        p_short_name = self.position.short_name

        if p_short_name == "GK":
            pass
        elif p_short_name == "DF":
            pass
        elif p_short_name == "MF":
            pass
        elif p_short_name == "ATK":
            pass
        else:
            return


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


class PremierLeagueStatusByPlayer(FootballBaseModel):
    """ PremierLeague Player Statistics """

    class Meta:
        db_table = "premier_league_player"
        verbose_name = _("Premier League Player")
        verbose_name_plural = _("Premier League Players")

    code = models.IntegerField(null=True)
    dreamteam_count = models.IntegerField(null=True)
    in_dreamteam = models.BooleanField(default=False)
    element_type = models.IntegerField(null=True)
    ep_next = models.CharField(max_length=255, null=True)
    ep_this = models.CharField(max_length=255, null=True)
    form = models.CharField(max_length=255, null=True)
    value_form = models.CharField(max_length=255, null=True)
    value_season = models.CharField(max_length=255, null=True)
    selected_by_percent = models.CharField(max_length=255, null=True)
    points_per_game = models.CharField(max_length=255, null=True)
    now_cost = models.IntegerField(null=True, blank=True)
    web_name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    second_name = models.CharField(max_length=255, null=True)
    special = models.CharField(max_length=255, null=True)
    squad_number = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    photo = models.CharField(max_length=255, null=True)
    photo_url = models.URLField()
    event_points = models.IntegerField(null=True)
    team = models.IntegerField(null=True)
    team_code = models.IntegerField(null=True)
    total_points = models.IntegerField(null=True)
    transfers_in = models.IntegerField(null=True)
    transfers_out = models.IntegerField(null=True)
    goals_scored = models.IntegerField(null=True)
    clean_sheets = models.IntegerField(null=True)
    goals_conceded = models.IntegerField(null=True)
    own_goals = models.IntegerField(null=True)
    penalties_saved = models.IntegerField(null=True)
    penalties_missed = models.IntegerField(null=True)
    yellow_cards = models.IntegerField(null=True)
    red_cards = models.IntegerField(null=True)
    saves = models.IntegerField(null=True)
    bonus = models.IntegerField(null=True)
    bps = models.IntegerField(null=True)
    influence_rank = models.IntegerField(null=True)
    creativity_rank = models.IntegerField(null=True)
    threat_rank = models.IntegerField(null=True)
    ict_index_rank = models.IntegerField(null=True)
    now_cost_rank = models.IntegerField(null=True)
    form_rank = models.IntegerField(null=True)
    selected_rank = models.IntegerField(null=True)
    direct_freekicks_order = models.IntegerField(null=True)
    penalties_order = models.IntegerField(null=True)
    influence = models.CharField(max_length=255, null=True)
    creativity = models.CharField(max_length=255, null=True)
    threat = models.CharField(max_length=255, null=True)
    ict_index = models.CharField(max_length=255, null=True)
    expected_goals = models.CharField(max_length=255, null=True)

    def __str__(self):
        if self.first_name and self.second_name:
            mark = False
            if self.fantasy_player.all():
                mark = True
            return f"{mark}: {self.first_name} - {self.second_name}"
        return f"{self.code} - {self.web_name}"


class CommonPlayer(BaseModel):
    fantasy_player = models.ForeignKey(to="PremierLeagueStatusByPlayer", on_delete=models.CASCADE,
                                       related_name="fantasy_player")
    sportmonks_player = models.ForeignKey(to="Player", on_delete=models.CASCADE, related_name="sportmonks_player")


# STATISTICS
class PlayerStatistic(FootballBaseModel):
    class Meta:
        db_table = "player_statistic"
        verbose_name = _("Player statistic")
        verbose_name_plural = _("Player statistics")

    player = models.ForeignKey(
        to="Player", on_delete=models.CASCADE, related_name="statistics", verbose_name=_("Player")
    )
    club = models.ForeignKey(
        to="Club", on_delete=models.CASCADE, related_name="player_statistics", verbose_name=_("Club")
    )
    season = models.ForeignKey(
        to="Season", on_delete=models.CASCADE, related_name="+", verbose_name=_("Season")
    )
    has_values = models.BooleanField(default=False, verbose_name=_("Has values"))

    def __str__(self):
        return f"{self.player} - {self.season}"


class PlayerStatisticDetail(FootballBaseModel):
    class Meta:
        db_table = "player_statistic_detail"
        verbose_name = _("Player statistic")
        verbose_name_plural = _("Player statistics")

    statistic = models.ForeignKey(to="PlayerStatistic", on_delete=models.CASCADE, related_name="details")
    type = models.ForeignKey(to="SportMonksType", on_delete=models.CASCADE, related_name="+", verbose_name=_("Type"))
    value = models.JSONField()

    def __str__(self):
        return f"{self.type} - {self.value}"
