from django.contrib import admin

from . import models


@admin.register(models.League)
class LeagueAdmin(admin.ModelAdmin):
    pass


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
