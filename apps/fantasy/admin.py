from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from . import models


class FormationPositionInline(admin.StackedInline):
    extra = 0
    model = models.FormationPosition
    autocomplete_fields = ("position",)
    exclude = ("is_deleted", "deleted_at",)
    ordering = ("is_substitution", "ordering",)


@admin.register(models.Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ("title", "scheme", "ordering", "id",)
    list_display_links = ("title",)
    search_fields = ("title", "scheme", "id",)
    list_editable = ("ordering",)
    ordering = ("ordering",)
    exclude = ("is_deleted", "deleted_at",)
    inlines = (FormationPositionInline,)


@admin.register(models.FormationPosition)
class FormationPositionAdmin(admin.ModelAdmin):
    search_fields = ("formation__title", "position__name", "position__short_name",)


@admin.register(models.Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "icon", "level_point", "id",)
    list_display_links = ("title",)
    search_fields = ("title", "description", "icon", "level_point", "id",)
    list_editable = ("level_point",)
    ordering = ("level_point",)
    exclude = ("is_deleted", "deleted_at",)


@admin.register(models.TeamLevel)
class TeamLevelAdmin(admin.ModelAdmin):
    list_display = ("team", "level", "created_at", "id",)
    list_display_links = ("team", "id",)
    search_fields = ("team__name", "level__title", "level__description", "id",)
    list_filter = ("level", "created_at",)
    autocomplete_fields = ("team", "level",)
    exclude = ("is_deleted", "deleted_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related("team", "level", )
        return qs


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


class SquadPlayerInline(admin.StackedInline):
    extra = 0
    model = models.SquadPlayer
    autocomplete_fields = ("player", "position",)
    exclude = ("is_deleted", "deleted_at",)


@admin.register(models.Squad)
class SquadAdmin(admin.ModelAdmin):
    list_display = ("team", "round", "formation", "is_default", "created_at", "id",)
    list_display_links = ("team", "id",)
    list_filter = ("team", "is_default",)
    search_fields = ("team__name", "formation__title",)
    autocomplete_fields = ("team", "round", "formation",)
    exclude = ("is_deleted", "deleted_at",)
    inlines = (SquadPlayerInline,)

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


@admin.register(models.PlayerRoundPoint)
class PlayerRoundPointAdmin(admin.ModelAdmin):
    list_display = (
        "player",
        "get_player_club",
        "round",
        "fixture",
        "total_point",

        "clean_sheet",
        "minutes_played",
        "goal",
        "goal_conceded",
        "assist",
        "saves",
        "penalty_save",
        "penalty_miss",
        "yellow_card",
        "red_card",

        "created_at",
        "id",
    )
    list_display_links = ("player", "id",)
    search_fields = (
        "player__first_name", "player__full_name", "player__common_name", "round__name", "total_point", "id",
    )
    list_filter = ("round", "player__position", "player__club", "created_at",)
    autocomplete_fields = ("player", "round", "fixture",)
    exclude = ("is_deleted", "deleted_at",)

    def get_player_club(self, obj):
        return obj.player.club

    get_player_club.short_description = _("Club")

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related("player", "round", "fixture", )
        return qs


@admin.register(models.SquadPlayerRoundPoint)
class SquadPlayerRoundPointAdmin(admin.ModelAdmin):
    list_display = (
        "squad_player",
        "round",
        "total_point",
        "created_at",
        "id",
    )
    list_display_links = ("squad_player", "id",)
    search_fields = (
        "squad_player__squad__team__name", "squad_player__player__player__full_name", "round__title", "total_point",
        "id",
        "remote_id",
    )
    autocomplete_fields = ("squad_player", "round", "player_point",)
    exclude = ("is_deleted", "deleted_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related("squad_player", "round", )
        return qs


@admin.register(models.TeamRoundPoint)
class TeamRoundPointAdmin(admin.ModelAdmin):
    list_display = ("team", "round", "total_point", "created_at", "id",)
    list_display_links = ("team", "id",)
    search_fields = ("team__name", "round__title", "total_point", "id",)
    list_filter = ("round", "created_at",)
    autocomplete_fields = ("team", "round", "squad",)
    exclude = ("is_deleted", "deleted_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related("team", "round", )
        return qs
