from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from . import models, utils


@admin.action(description=_("Update leagues"))
def update_leagues_action(model_admin, request, queryset):
    utils.update_leagues()
    model_admin.message_user(request, _("Leagues updated!"))


@admin.action(description=_("Update seasons"))
def update_seasons_action(model_admin, request, queryset):
    utils.update_seasons()
    model_admin.message_user(request, _("Seasons updated!"))


@admin.action(description=_("Update players"))
def update_players_action(model_admin, request, queryset):
    utils.update_players()
    model_admin.message_user(request, _("Players updated!"))


@admin.register(models.League)
class LeagueAdmin(admin.ModelAdmin):
    actions = (update_leagues_action,)


@admin.register(models.Season)
class SeasonAdmin(admin.ModelAdmin):
    actions = (update_seasons_action,)


@admin.register(models.Round)
class RoundAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FixtureState)
class FixtureStateAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Fixture)
class FixtureAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Club)
class ClubAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    actions = (update_players_action,)


@admin.register(models.ClubPlayer)
class ClubPlayerAdmin(admin.ModelAdmin):
    pass
