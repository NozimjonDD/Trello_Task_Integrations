from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from apps.common.data import TariffTypeChoices
from apps.common.models import BaseModel


class Tariff(BaseModel):
    class Meta:
        db_table = "tariff"
        verbose_name = "Tariff"
        verbose_name_plural = "Tariffs"

    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE, related_name="tariff", null=True)
    title = models.CharField(max_length=200, verbose_name=_("Title"), null=True)
    description = models.TextField(verbose_name=_("description"))
    type = models.CharField(choices=TariffTypeChoices.choices, default=TariffTypeChoices.FREE, max_length=100)
    annual_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    monthly_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title


class TariffCase(BaseModel):
    class Meta:
        db_table = "tariff_case"
        verbose_name = "Tariff Case"
        verbose_name_plural = "Tariff Cases"

    tariff = models.ForeignKey(to="Tariff", on_delete=models.DO_NOTHING, related_name="tariff_cases", null=True)
    title = models.CharField(max_length=200, verbose_name=_("Title"), null=True)
    ordering = models.IntegerField(default=1)
    amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class Subscription(BaseModel):
    class Meta:
        db_table = "subscription"
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE, related_name="subscriptions", null=True)
    tariff = models.ForeignKey(to="Tariff", on_delete=models.DO_NOTHING, related_name="subscription_tariffs", null=True)
    total_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

