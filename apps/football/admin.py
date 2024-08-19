from django.contrib import admin
from django.utils.html import format_html

from django.utils.translation import gettext_lazy as _

from . import models, utils


@admin.action(description=_("Update leagues"))
def update_leagues_action(model_admin, request, queryset):
    utils.update_leagues()
    model_admin.message_user(request, _("Leagues updated!"))


@admin.action(description=_("Update seasons by league"))
def update_seasons_by_league_action(model_admin, request, queryset):
    for league in queryset:
        utils.update_seasons_by_league(league.remote_id)
    model_admin.message_user(request, _("Seasons updated!"))


@admin.action(description=_("Update rounds by season"))
def update_rounds_by_season_action(model_admin, request, queryset):
    for season in queryset:
        utils.update_rounds_by_season(season.remote_id)
    model_admin.message_user(request, _("Rounds updated!"))


@admin.action(description=_("Update clubs by season"))
def update_clubs_by_season_action(model_admin, request, queryset):
    for season in queryset:
        utils.update_clubs_by_season(season.remote_id)
    model_admin.message_user(request, _("Clubs updated!"))


@admin.action(description=_("Update club details (info, players)"))
def update_club_action(model_admin, request, queryset):
    for club in queryset:
        utils.update_club_details(club.remote_id)
    model_admin.message_user(request, _("Club details updated!"))


@admin.action(description=_("Update players"))
def update_players_action(model_admin, request, queryset):
    utils.update_players()
    model_admin.message_user(request, _("Players updated!"))


@admin.action(description=_("Update positions"))
def update_positions_action(model_admin, request, queryset):
    utils.update_positions()
    model_admin.message_user(request, _("Positions updated!"))


@admin.register(models.League)
class LeagueAdmin(admin.ModelAdmin):
    actions = (update_leagues_action, update_seasons_by_league_action,)

    list_display = ("name", "short_code", "type", "sub_type", "is_active", "id",)
    list_display_links = ("name",)
    list_filter = ("is_active",)
    search_fields = ("name", "short_code", "type", "sub_type", "remote_id",)


@admin.register(models.Season)
class SeasonAdmin(admin.ModelAdmin):
    actions = (update_rounds_by_season_action, update_clubs_by_season_action,)
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
    pass


@admin.register(models.Fixture)
class FixtureAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "logo_html", "founded_year", "type", "id",)
    list_display_links = ("name", "id",)
    search_fields = ("name", "short_name", "type", "remote_id", "founder_year",)

    actions = (update_club_action,)

    def logo_html(self, obj):
        if obj.logo_path:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.logo_path))
        return None

    logo_html.short_description = _("Logo")


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "code", "id",)
    list_display_links = ("name", "id",)
    search_fields = ("name", "short_name", "code", "id", "remote_id",)
    actions = (update_positions_action,)


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    actions = (update_players_action,)

    list_display = (
        "first_name",
        "last_name",
        "common_name",
        "profile_pic",
        "club",
        "club_contract_until",
        "position",
        "date_of_birth",
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


@admin.register(models.ClubPlayer)
class ClubPlayerAdmin(admin.ModelAdmin):
    list_display = ("club", "player", "is_captain", "is_current_club", "kit_number", "start_date", "end_date", "id",)
    list_display_links = ("club", "player", "id",)
    search_fields = ("club__name", "player__full_name",)
    list_filter = ("is_captain", "is_current_club", "start_date", "end_date",)
    autocomplete_fields = ("club", "player",)
