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
    list_display = ("name", "user", "status", "created_at", "id",)
    list_display_links = ("name", "id",)
    search_fields = ("name", "user__phone_number", "id",)
    list_filter = ("status", "created_at",)
    exclude = ("is_deleted", "deleted_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related("user")
        return qs


@admin.register(models.TeamPlayer)
class TeamPlayerAdmin(admin.ModelAdmin):
    list_display = ("team", "player", "position", "created_at", "id",)
    list_display_links = ("team", "id",)
    search_fields = (
        "team__name",
        "player__first_name",
        "player__full_name",
        "player__common_name",
        "position__name",
        "position__short_name",
    )
    list_filter = ("team", "created_at",)
    autocomplete_fields = ("team", "player", "position",)
    exclude = ("is_deleted", "deleted_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related("team", "player", "position", )
        return qs


@admin.register(models.Squad)
class SquadAdmin(admin.ModelAdmin):
    list_display = ("team", "round", "formation", "is_default", "created_at", "id",)
    list_display_links = ("team", "id",)
    list_filter = ("team", "is_default",)
    search_fields = ("team__name", "formation__title",)
    autocomplete_fields = ("team", "round", "formation",)
    exclude = ("is_deleted", "deleted_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related("team", "round", "formation", )
        return qs


@admin.register(models.SquadPlayer)
class SquadPlayerAdmin(admin.ModelAdmin):
    list_display = ("squad", "player", "position", "is_captain", "is_substitution", "created_at", "id",)
    list_display_links = ("squad", "id",)
    autocomplete_fields = ("squad", "player",)
    search_fields = ("squad__team__name", "player__player__full_name",)
    list_filter = ("squad", "is_captain", "is_substitution", "created_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related("squad", "player", "position", )
        return qs


@admin.register(models.Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ("team", "transfer_type", "player", "swapped_player", "fee", "created_at", "id",)
    list_display_links = ("team", "id",)
    search_fields = ("team__name", "player__first_name", "player__full_name", "player__common_name", "fee", "id",)
    list_filter = ("transfer_type", "created_at",)
    autocomplete_fields = ("team", "player", "swapped_player",)
    exclude = ("is_deleted", "deleted_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related("team", "player", "swapped_player", )
        return qs


@admin.register(models.FantasyLeague)
class FantasyLeagueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LeagueParticipant)
class LeagueParticipantAdmin(admin.ModelAdmin):
    pass
