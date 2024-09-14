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


@admin.register(models.CoinTariff)
class CoinTariffAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "coin_amount",
        "price",
        "discount_price",
        "ordering",
        "created_at",
        "id",
    )
    list_display_links = ("title", "id",)
    list_editable = ("ordering",)
    ordering = ("ordering",)
    exclude = ("is_deleted", "deleted_at", "title",)
    search_fields = ("title", "coin_amount", "price", "discount_price", "id",)


@admin.register(models.CoinOrder)
class CoinOrderAdmin(admin.ModelAdmin):
    list_display = ("user", "coin_tariff", "status", "payment_type", "price", "coin_amount", "created_at", "id",)
    list_display_links = ("user", "id",)
    list_filter = ("status", "payment_type", "created_at",)
    search_fields = (
        "user__phone_number",
        "user__first_name",
        "coin_tariff__title",
        "status",
        "payment_type",
        "price",
        "coin_amount",
        "id",
    )
    autocomplete_fields = ("user", "coin_tariff",)
    exclude = ("is_deleted", "deleted_at",)


@admin.register(models.Transaction)
class TransactionAmin(admin.ModelAdmin):
    pass


@admin.register(models.PaymentMerchantRequestLog)
class PaymentMerchantRequestLogAdmin(admin.ModelAdmin):
    pass
