from modeltranslation.translator import register, TranslationOptions

from . import models


@register(models.NewsCategory)
class NewsCategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(models.News)
class NewsTranslationOptions(TranslationOptions):
    fields = ("title", "content", "image",)
