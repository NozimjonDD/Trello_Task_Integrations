from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from . import models


@admin.register(models.NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "ordering", "created_at", "id",)
    list_display_links = ("title", "id",)

    list_editable = ("ordering",)
    search_fields = ("title",)
    exclude = ("is_deleted", "deleted_at", "title",)
    ordering = ("ordering",)


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "image_preview", "published_at", "created_at", "id",)
    list_display_links = ("title", "id",)

    search_fields = ("title", "content",)
    exclude = ("is_deleted", "deleted_at", "title", "content", "image",)
    list_filter = ("category",)
    date_hierarchy = "created_at"
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        return format_html(f'<img src="{obj.image.url}" style="max-width: 200px; max-height: 200px;" />')

    image_preview.short_description = "Image Preview"
    image_preview.allow_tags = True
