from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from . import models, utils


@admin.action(description=_("Update leagues"))
def update_leagues_action(model_admin, request, queryset):
    utils.update_leagues()
    model_admin.message_user(request, _("Leagues updated!"))


@admin.register(models.League)
class LeagueAdmin(admin.ModelAdmin):
    actions = (update_leagues_action,)


@admin.register(models.Season)
class SeasonAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Round)
class RoundAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MatchState)
class MatchStateAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Match)
class MatchAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Club)
class ClubAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ClubPlayer)
class ClubPlayerAdmin(admin.ModelAdmin):
    pass
