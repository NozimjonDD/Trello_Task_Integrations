from django.contrib import admin

# Register your models here.
from apps.finance import models


@admin.register(models.TariffCase)
class TariffCaseAdmin(admin.ModelAdmin):
    list_display = ("title", "tariff", "amount", "ordering",)


@admin.register(models.Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "description", "type", "annual_price", "monthly_price",)
