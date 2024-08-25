from django.contrib import admin
from django.conf import settings

from django.utils.html import format_html

from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from . import models, actions


@admin.register(models.League)
class LeagueAdmin(admin.ModelAdmin):
    actions = (actions.update_leagues_action, actions.update_seasons_by_league_action,)

    list_display = ("name", "short_code", "type", "sub_type", "is_active", "id",)
    list_display_links = ("name",)
    list_filter = ("is_active",)
    search_fields = ("name", "short_code", "type", "sub_type", "remote_id",)


@admin.register(models.Season)
class SeasonAdmin(admin.ModelAdmin):
    actions = (
        actions.update_rounds_by_season_action,
        actions.update_clubs_by_season_action,
        actions.update_fixtures_by_season_action,
    )
    list_display = ("name", "league", "is_finished", "pending", "is_current", "starting_at", "ending_at", "id",)
    list_display_links = ("name",)
    list_filter = ("league", "is_finished", "pending", "is_current",)
    search_fields = ("name", "league__name", "remote_id",)
    autocomplete_fields = ("league",)
    ordering = ("-starting_at",)


@admin.register(models.Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = (
        "name", "league", "season", "is_finished", "is_current", "starting_at", "ending_at", "id",
    )
    list_display_links = ("name",)
    list_filter = ("league", "season", "is_finished", "is_current",)
    search_fields = ("name", "league__name", "season__name", "remote_id",)
    autocomplete_fields = ("league", "season",)
    ordering = ("starting_at",)


@admin.register(models.FixtureState)
class FixtureStateAdmin(admin.ModelAdmin):
    list_display = ("title", "short_title", "state", "id",)
    list_display_links = ("title", "id",)
    search_fields = ("state", "title", "short_title", "id", "remote_id",)
    actions = (actions.update_fixture_states_action,)


@admin.register(models.Fixture)
class FixtureAdmin(admin.ModelAdmin):
    list_display = (
        "title", "result_score", "season", "round", "state", "result_info", "match_date", "id",)
    list_display_links = ("title", "id",)
    search_fields = ("title", "season__name", "round__name", "state__title", "remote_id", "id",)
    autocomplete_fields = ("season", "round", "state", "home_club", "away_club",)

    def result_score(self, obj):
        if obj.home_club_score and obj.away_club_score:
            return f"{obj.home_club_score}:{obj.away_club_score}"
        return "-:-"

    result_score.short_description = _("Result score")


@admin.register(models.Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "logo_html", "league", "founded_year", "type", "id",)
    list_display_links = ("name", "id",)
    search_fields = ("name", "short_name", "type", "remote_id", "founder_year",)
    list_filter = ("league",)
    autocomplete_fields = ("league",)

    actions = (actions.update_club_action,)

    def logo_html(self, obj):
        if obj.logo_path:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.logo_path))
        return None

    logo_html.short_description = _("Logo")


@admin.register(models.SportMonksType)
class SportMonksTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "model_type", "code", "developer_name", "remote_id", "id",)
    list_display_links = ("name", "id",)
    search_fields = ("name", "model_type", "code", "developer_name", "id", "remote_id",)
    actions = (actions.update_types_action,)


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "code", "id",)
    list_display_links = ("name", "id",)
    search_fields = ("name", "short_name", "code", "id", "remote_id",)
    actions = (actions.update_types_action,)


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    actions = (actions.update_players_action,)

    list_display = (
        "first_name",
        "last_name",
        "common_name",
        "profile_pic",
        "club",
        "club_contract_until",
        "position",
        "pretty_market_value",
        "date_of_birth",
        "age",
        "gender",
        "height",

        "market_value",
        "id",
    )
    list_display_links = ("first_name", "id",)
    search_fields = ("first_name", "last_name", "common_name", "club__name", "position__name",)
    autocomplete_fields = ("club", "position",)

    def profile_pic(self, obj):
        if obj.profile_picture_path:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.profile_picture_path))
        return None

    profile_pic.short_description = _("Profile picture")

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related("club", "position", )
        qs = qs.filter(club__league__remote_id=settings.PREMIER_LEAGUE_ID)
        return qs


@admin.register(models.ClubPlayer)
class ClubPlayerAdmin(admin.ModelAdmin):
    list_display = ("club", "player", "is_captain", "is_current_club", "kit_number", "start_date", "end_date", "id",)
    list_display_links = ("club", "player", "id",)
    search_fields = ("club__name", "player__full_name",)
    list_filter = ("is_captain", "is_current_club", "start_date", "end_date",)
    autocomplete_fields = ("club", "player",)


@admin.register(models.PremierLeagueStatusByPlayer)
class PremierLeagueStatusByPlayerAdmin(admin.ModelAdmin):
    actions = (actions.update_premierleague_players_action,)

    list_display = ("image_tag", "now_cost", "first_name", "second_name",
                    "web_name", "total_points", "selected_by_percent", "goals_scored", "team", "threat",
                    "own_goals", "penalties_saved", "bonus",)

    search_fields = ("web_name", "first_name", "second_name",)

    def image_tag(self, obj):
        if obj.photo_url:
            return mark_safe('<img class="image" src="%s" width="50" height="50" />' % (obj.photo_url))
        return None

    image_tag.short_description = _("Profile picture")


@admin.register(models.CommonPlayer)
class CommonPlayerAdmin(admin.ModelAdmin):
    list_display = ("fantasy_player", "sportmonks_player")
    autocomplete_fields = ("sportmonks_player", "fantasy_player",)