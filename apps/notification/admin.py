from django.contrib import admin
from django.utils.html import format_html

from . import models


@admin.register(models.NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "icon_html",
    )
    list_display_links = ("name",)
    exclude = ("is_deleted", "deleted_at", "name",)

    def icon_html(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" />', obj.icon.url)
        return None

    icon_html.short_description = "icon"
    search_fields = ("name", "type",)


@admin.register(models.NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ("type", "title", "created_at", "id",)
    list_display_links = ("type", "id",)
    search_fields = ("title", "id",)
    list_filter = ("type",)
    exclude = ("is_deleted", "deleted_at", "title", "body", "button_name",)


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "title",
        "is_sent",
        "created_at",
    )
    list_display_links = ("id", "title",)
    search_fields = ("title",)
    list_filter = ("type", "is_sent",)
    autocomplete_fields = ("type", "template",)
    exclude = ("is_deleted", "deleted_at", "title", "description",)


@admin.register(models.UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "notification", "is_read", "read_at", "created_at")
    list_display_links = ("id", "user", "notification",)
    search_fields = ("notification__title",)
    list_filter = ("is_read", "user", "notification",)
    autocomplete_fields = ("user", "notification",)
    exclude = ("is_deleted", "deleted_at",)
