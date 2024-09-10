from modeltranslation.translator import register, TranslationOptions

from . import models


@register(models.CoinTariff)
class CoinTariffTranslationOptions(TranslationOptions):
    fields = ("title",)
