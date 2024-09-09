from django.contrib import admin

from apps.finance import models


class TariffOptionInline(admin.StackedInline):
    model = models.TariffOption
    extra = 1
    exclude = ("is_deleted", "deleted_at",)
    autocomplete_fields = ("tariff",)


@admin.register(models.Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "created_at", "id",)
    list_display_links = ("title", "id",)
    search_fields = ("title", "type", "id",)
    exclude = ("is_deleted", "deleted_at",)
    inlines = (TariffOptionInline,)


@admin.register(models.TariffOption)
class TariffOptionAdmin(admin.ModelAdmin):
    list_display = ("title", "tariff", "amount", "price", "discount_price", "ordering", "created_at", "id",)
    list_display_links = ("title", "id",)
    list_editable = ("ordering",)
    search_fields = ("title", "tariff__title", "amount", "price", "discount_price", "id",)
    list_filter = ("tariff", "created_at",)
    autocomplete_fields = ("tariff",)
    ordering = ("ordering",)


@admin.register(models.UserTariff)
class UserTariffAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TariffOrder)
class TariffOrderAdmin(admin.ModelAdmin):
    pass
