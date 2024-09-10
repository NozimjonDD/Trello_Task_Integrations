from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.data import (
    TariffTypeChoices,
    TariffOrderStatusChoices,
    OrderPaymentTypeChoices,
    TransactionStatusChoices
)
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


# ============================= COIN MODELS =============================

class CoinTariff(BaseModel):
    class Meta:
        db_table = "coin_tariff"
        verbose_name = _("Coin Tariff")
        verbose_name_plural = _("Coin Tariffs")

    title = models.CharField(max_length=200, verbose_name=_("Title"))
    image = models.ImageField(upload_to="coin_tariff", verbose_name=_("Image"), null=True, blank=True)

    coin_amount = models.IntegerField(default=0, verbose_name=_("Coin Amount"))
    price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        verbose_name=_("Price"),
        help_text=_("uzs"),
    )
    discount_price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Discount Price"),
        help_text=_("uzs"),
    )
    ordering = models.IntegerField(default=1, verbose_name=_("Ordering"))

    def __str__(self):
        return f"{self.title}"


class CoinOrder(BaseModel):
    class Meta:
        db_table = "coin_order"
        verbose_name = _("Coin Order")
        verbose_name_plural = _("Coin Orders")

    user = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="coin_orders",
        verbose_name=_("User"),
    )
    coin_tariff = models.ForeignKey(
        to="CoinTariff",
        on_delete=models.SET_NULL,
        related_name="coin_orders",
        verbose_name=_("Coin Tariff"),
        null=True,
    )
    payment_type = models.CharField(
        max_length=100,
        verbose_name=_("Payment Type"),
        choices=OrderPaymentTypeChoices.choices
    )
    status = models.CharField(
        max_length=100,
        verbose_name=_("Status"),
        choices=TariffOrderStatusChoices.choices,
        default=TariffOrderStatusChoices.PENDING,
    )
    price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        verbose_name=_("Price"),
    )
    coin_amount = models.IntegerField(default=0, verbose_name=_("Coin Amount"))

    def __str__(self):
        return f"{self.user} - {self.coin_tariff}"


class Transaction(BaseModel):
    class Meta:
        db_table = "transaction"
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    order = models.ForeignKey(
        to="CoinOrder",
        on_delete=models.CASCADE,
        verbose_name=_("Order"),
        related_name="transactions",
        null=True,
        blank=True,
    )
    click_trans_id = models.CharField(max_length=255, null=True, blank=True)
    click_paydoc_id = models.CharField(verbose_name=_('Номер платежа в системе CLICK'), max_length=255, blank=True)
    merchant_trans_id = models.CharField(
        verbose_name=_('Номер транзакции в системе магазина'), max_length=255, blank=True
    )
    amount = models.DecimalField(verbose_name=_('Сумма оплаты (в сумах)'), max_digits=9, decimal_places=2,
                                 default="0.0")
    action = models.CharField(verbose_name=_("Выполняемое действие"), max_length=255, blank=True, null=True)
    sign_string = models.CharField(max_length=255, null=True, blank=True)
    sign_time = models.DateTimeField(max_length=255, null=True, blank=True)
    error = models.IntegerField(verbose_name=_("Код ошибки"), null=True, blank=True)
    error_note = models.CharField(verbose_name=_("Описание ошибки"), max_length=255, null=True, blank=True)

    status = models.CharField(
        verbose_name=_("Статус"),
        max_length=25,
        choices=TransactionStatusChoices.choices,
        default=TransactionStatusChoices.PROCESSING
    )

    def __str__(self):
        return f"{self.id}. {self.order} - {self.amount} - {self.status}"


class PaymentMerchantRequestLog(BaseModel):
    header = models.TextField(verbose_name=_("Header"))
    body = models.TextField(verbose_name=_("Body"))
    method = models.CharField(verbose_name=_("Method"), max_length=32)
    response = models.TextField(null=True, blank=True)
    response_status_code = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "payment_merchant_request_log"
        verbose_name = _("Payment Merchant Request Log")
        verbose_name_plural = _("Payment Merchant Request Logs")

    def __str__(self):
        return f"{self.id}"
# ============================= COIN MODELS END =============================
