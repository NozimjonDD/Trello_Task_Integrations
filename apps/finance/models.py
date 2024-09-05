from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

# Create your models here.
from apps.common.data import TariffTypeChoices
from apps.common.models import BaseModel


class Tariff(BaseModel):
    class Meta:
        db_table = "tariff"
        verbose_name = "Tariff"
        verbose_name_plural = "Tariffs"

    title = models.CharField(max_length=200, verbose_name=_("Title"), null=True)
    description = models.TextField(verbose_name=_("description"))
    type = models.CharField(choices=TariffTypeChoices.choices, default=TariffTypeChoices.FREE, max_length=100)
    price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

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
