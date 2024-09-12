from modeltranslation.translator import register, TranslationOptions

from . import models


@register(models.NotificationType)
class NotificationTypeTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(models.NotificationTemplate)
class NotificationTemplateTranslationOptions(TranslationOptions):
    fields = ("title", "body", "button_name",)


@register(models.Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ("title", "description",)
