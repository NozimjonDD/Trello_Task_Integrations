from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import utils, tasks


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


@admin.action(description=_("Update fixtures by season"))
def update_fixtures_by_season_action(model_admin, request, queryset):
    for season in queryset:
        utils.update_fixtures_by_season(season.remote_id)
    model_admin.message_user(request, _("Fixtures updated!"))


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
    tasks.update_players_task.apply_async()
    model_admin.message_user(request, _("Players update task started!"))


@admin.action(description=_("Update types(positions included)"))
def update_types_action(model_admin, request, queryset):
    utils.update_types()
    model_admin.message_user(request, _("Types(positions included) updated!"))


@admin.action(description=_("Update fixture states"))
def update_fixture_states_action(model_admin, request, queryset):
    utils.update_fixture_states()
    model_admin.message_user(request, _("Fixture states updated!"))


@admin.action(description=_("Update PremierLeague players Statistics"))
def update_premierleague_players_action(model_admin, request, queryset):
    """ Update PremierLeague Player Statistics """
    utils.update_premierleague_status_by_players()
    model_admin.message_user(request, _("Update PremierLeague Player Statistics!"))
