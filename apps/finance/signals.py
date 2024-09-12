from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.finance import models
from apps.common.data import TariffOrderStatusChoices

COIN_ORDER_STATUS = {}


@receiver(pre_save, sender=models.CoinOrder)
def coin_order_pre_save(sender, instance, **kwargs):
    if instance.pk:
        COIN_ORDER_STATUS[instance.pk] = sender.objects.get(pk=instance.pk).status


@receiver(post_save, sender=models.CoinOrder)
def coin_order_post_save(sender, instance, created, **kwargs):
    if COIN_ORDER_STATUS.get(instance.pk) == instance.status:
        return None

    if instance.status == TariffOrderStatusChoices.SUCCESS:
        instance.apply_coin_order()
