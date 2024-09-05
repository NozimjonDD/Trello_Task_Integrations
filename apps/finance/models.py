from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from apps.common.data import TariffTypeChoices
from apps.common.models import BaseModel


class Tariff(BaseModel):
    class Meta:
        db_table = "tariff"
        verbose_name = "Tariff"
        verbose_name_plural = "Tariffs"

    title = models.CharField(max_length=200, verbose_name=_("Title"), null=True)
    description = models.TextField(verbose_name=_("description"))
    type = models.CharField(choices=TariffTypeChoices.choices, max_length=100)

    # TODO: move prices from tariff to tariff cases
    price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title


class TariffCase(BaseModel):
    class Meta:
        db_table = "tariff_case"
        verbose_name = "Tariff Case"
        verbose_name_plural = "Tariff Cases"

    tariff = models.ForeignKey(to="Tariff", on_delete=models.CASCADE, related_name="tariff_cases", null=True)
    title = models.CharField(max_length=200, verbose_name=_("Title"), null=True)
    amount = models.IntegerField(default=0, verbose_name=_("Amount"))

    price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        help_text=_("Prices must be in coins."),
    )
    discount_price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Prices must be in coins."),
    )
    ordering = models.IntegerField(default=1, verbose_name=_("Ordering"))

    def __str__(self):
        return self.title


class UserTariff(BaseModel):
    class Meta:
        db_table = "user_tariff"
        verbose_name = _("User Tariff")
        verbose_name_plural = _("User Tariff")

    user = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="user_tariffs",
        verbose_name=_("User"),
    )
    tariff = models.ForeignKey(
        to="Tariff",
        on_delete=models.CASCADE,
        related_name="user_tariffs",
        verbose_name=_("Tariff"),
    )
    tariff_case = models.ForeignKey(
        to="TariffCase",
        on_delete=models.CASCADE,
        related_name="user_tariffs",
        verbose_name=_("Tariff Case"),
    )
    season = models.ForeignKey(
        to="football.Season",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Season"),
        null=True,
        blank=True,
    )
    round = models.ForeignKey(
        to="football.Round",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Round"),
        null=True,
        blank=True,
    )
    amount = models.IntegerField(default=0, verbose_name=_("Amount"))

    price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Tariff cases price when user bought it."),
    )
    discount_price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Tariff cases discount price when user bought it."),
    )

    def __str__(self):
        return f"{self.user} - {self.tariff}"


class Subscription(BaseModel):
    class Meta:
        db_table = "subscription"
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    user = models.OneToOneField(to="users.User", on_delete=models.CASCADE, related_name="subscriptions", null=True)
    tariff = models.ManyToManyField(to="Tariff", related_name="subscription_tariffs", blank=True)
    total_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    @property
    def calculate_total_price(self):
        if self.tariff:
            self.total_price = self.tariff.all().aggregate(total=Sum("price")).get("total", 0)
            self.save()
            return self.total_price
        return None
