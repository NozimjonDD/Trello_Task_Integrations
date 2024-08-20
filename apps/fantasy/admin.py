from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from . import models


class FormationPositionInline(admin.StackedInline):
    extra = 0
    model = models.FormationPosition
    autocomplete_fields = ("position",)
    exclude = ("is_deleted", "deleted_at",)


@admin.register(models.Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ("title", "scheme", "ordering", "id",)
    list_display_links = ("title",)
    search_fields = ("title", "scheme", "id",)
    list_editable = ("ordering",)
    ordering = ("ordering",)
    exclude = ("is_deleted", "deleted_at",)
    inlines = (FormationPositionInline,)


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TeamPlayer)
class TeamPlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Squad)
class SquadAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SquadPlayer)
class SquadPlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FantasyLeague)
class FantasyLeagueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LeagueParticipant)
class LeagueParticipantAdmin(admin.ModelAdmin):
    pass
