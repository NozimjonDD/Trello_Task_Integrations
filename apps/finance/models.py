from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from apps.common.data import TariffTypeChoices, TariffOrderStatusChoices
from apps.common.models import BaseModel
from apps.football import models as football_models


class Tariff(BaseModel):
    class Meta:
        db_table = "tariff"
        verbose_name = "Tariff"
        verbose_name_plural = "Tariffs"

    title = models.CharField(max_length=200, verbose_name=_("Title"), null=True)
    description = models.TextField(verbose_name=_("description"))
    type = models.CharField(choices=TariffTypeChoices.choices, max_length=100, unique=True, verbose_name=_("Type"))

    def __str__(self):
        return f"{self.title}"


class TariffOption(BaseModel):
    class Meta:
        db_table = "tariff_option"
        verbose_name = "Tariff option"
        verbose_name_plural = "Tariff options"

    tariff = models.ForeignKey(to="Tariff", on_delete=models.CASCADE, related_name="tariff_options", null=True)
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
        return f"{self.title}"


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
    tariff_option = models.ForeignKey(
        to="TariffOption",
        on_delete=models.SET_NULL,
        related_name="user_tariffs",
        verbose_name=_("Tariff option"),
        null=True,
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

    def __str__(self):
        return f"{self.user} - {self.tariff}"


class TariffOrder(BaseModel):
    class Meta:
        db_table = "tariff_order"
        verbose_name = _("Tariff Order")
        verbose_name_plural = _("Tariff Orders")

    user = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="tariff_orders",
        verbose_name=_("User"),
    )
    tariff = models.ForeignKey(
        to="Tariff",
        on_delete=models.CASCADE,
        related_name="tariff_orders",
        verbose_name=_("Tariff"),
    )
    tariff_option = models.ForeignKey(
        to="TariffOption",
        on_delete=models.SET_NULL,
        related_name="tariff_orders",
        verbose_name=_("Tariff option"),
        null=True,
    )
    status = models.CharField(
        max_length=100,
        choices=TariffOrderStatusChoices.choices,
        default=TariffOrderStatusChoices.PENDING,
        verbose_name=_("Status"),
    )
    price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        help_text=_("Prices are in coins."),
    )
    discount_price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Prices are in coins."),
    )

    def __str__(self):
        return f"{self.user} - {self.tariff}"

    def apply_tariff_order(self):
        if self.discount_price:
            self.user.coin_balance -= self.discount_price
        else:
            self.user.coin_balance -= self.price
        self.user.save(update_fields=["coin_balance"])

        UserTariff.objects.create(
            user_id=self.user_id,
            tariff_id=self.tariff_id,
            tariff_option_id=self.tariff_option_id,
            amount=self.tariff_option.amount,
            season_id=football_models.Round.get_coming_gw().season_id,
        )

        self.status = TariffOrderStatusChoices.SUCCESS
        self.save(update_fields=["status"])


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
