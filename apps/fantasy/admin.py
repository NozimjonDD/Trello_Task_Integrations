from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ("title", "scheme", "ordering", "id",)
    list_display_links = ("title",)
    search_fields = ("title", "scheme", "id",)
    list_editable = ("ordering",)
    ordering = ("ordering",)


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TeamPlayer)
class TeamPlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FantasyLeague)
class FantasyLeagueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LeagueParticipant)
class LeagueParticipantAdmin(admin.ModelAdmin):
    pass
