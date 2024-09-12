from django.conf import settings

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import transaction

from firebase_admin.exceptions import InvalidArgumentError

from apps.common.models import BaseModel
from apps.users import models as user_models
from apps.common.data import NotificationTypeChoices, NotificationDetailedEventTypes
from . import utils


class NotificationType(BaseModel):
    class Meta:
        db_table = "notification_type"
        verbose_name = _("Notification Type")
        verbose_name_plural = _("Notification Types")

    name = models.CharField(_("Name"), max_length=255, null=True, blank=True)
    type = models.CharField(_("Type"), max_length=255, choices=NotificationTypeChoices.choices, unique=True)
    icon = models.ImageField(verbose_name=_("Icon"), upload_to="notification_type/icons/", null=True, blank=True)
    image = models.ImageField(verbose_name=_("Image"), upload_to="notification_type/images/", null=True, blank=True)

    def __str__(self):
        return self.get_type_display()


class NotificationTemplate(BaseModel):
    class Meta:
        db_table = "notification_template"
        verbose_name = _("Notification template")
        verbose_name_plural = _("Notification templates")

    type = models.CharField(
        verbose_name=_("Template type"), max_length=100, choices=NotificationDetailedEventTypes.choices
    )
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    body = models.TextField(verbose_name=_("body"))
    route = models.CharField(verbose_name=_("mobile route"), max_length=200, null=True, blank=True)
    button_name = models.CharField(verbose_name=_("route button name"), null=True, blank=True)

    def __str__(self):
        return self.get_type_display()


class Notification(BaseModel):
    class Meta:
        db_table = "notification"
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    type = models.ForeignKey(to="NotificationType", verbose_name=_("Type"), on_delete=models.CASCADE, related_name="+")
    template = models.ForeignKey(
        to="NotificationTemplate",
        on_delete=models.SET_NULL,
        verbose_name=_("Notification template"),
        related_name="+",
        null=True,
        blank=True,
    )
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"), null=True, blank=True)
    context = models.JSONField(verbose_name=_("Context"), null=True, blank=True)

    redirect_url = models.URLField(_("Redirect URL"), null=True, blank=True)
    target_id = models.PositiveIntegerField(verbose_name=_("Target id"), null=True, blank=True)

    send_to_all = models.BooleanField(_("Send to all"), default=False)
    receivers = models.ManyToManyField(
        to="users.User",
        verbose_name=_("Receivers"),
        related_name="+",
        blank=True
    )

    is_sent = models.BooleanField(_("Is Sent"), default=False)
    sent_at = models.DateTimeField(_("Sent At"), null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.title}"

    @classmethod
    def make(cls, typ, event_type, context, target_id=None):
        try:
            template = NotificationTemplate.objects.get(type=event_type)
        except cls.DoesNotExist:
            return None
        instance = cls(
            type=NotificationType.objects.get(type=typ),
            template=template,
            title_uz=template.title_uz,
            description_uz=template.body_uz.format(**context),
            title_ru=template.title_ru,
            description_ru=template.body_ru.format(**context),
            context=context,
            redirect_url=None,
            target_id=target_id,
        )
        instance.save()
        return instance

    @transaction.atomic
    def send(self, receivers):
        objs = []
        for receiver in receivers:
            obj = UserNotification(
                user=receiver,
                notification=self
            )
            objs.append(obj)
        UserNotification.objects.bulk_create(objs)

        self.is_sent = True
        self.sent_at = timezone.now()
        self.save()
        self.send_push_notification(receivers)

    def send_push_notification(self, receivers):
        user_devices = user_models.Device.objects.filter(
            user___account_settings__push_notifications=True,
            is_deleted=False,
            user__in=receivers,
        )
        for device in user_devices:
            try:
                utils.send_push_notification(
                    fcm_token=device.fcm_token,
                    title=self.title,
                    body=self.description,
                    data={
                        "route": self.template.route if self.template and self.template.route else "",
                        "target_id": str(self.target_id) if self.target_id else "",
                    }
                )
            except InvalidArgumentError:
                continue

    @property
    def short_description(self):
        if self.description:
            return self.description[:100]
        return None

    def save(self, *args, **kwargs):
        if self.template.type == NotificationDetailedEventTypes.APP_VERSION_UPDATED:
            self.title_uz = self.template.title_uz
            self.description_uz = self.template.body_uz.format(**self.context)
            self.title_ru = self.template.title_ru
            self.description_ru = self.template.body_ru.format(**self.context)
        super().save(*args, **kwargs)


class UserNotification(BaseModel):
    class Meta:
        db_table = "user_notification"
        verbose_name = _("User Notification")
        verbose_name_plural = _("User Notifications")

    user = models.ForeignKey(
        to="users.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="notifications"
    )
    notification = models.ForeignKey(
        to="Notification",
        verbose_name=_("Notification"),
        on_delete=models.CASCADE,
        related_name="user_notifications",
    )
    is_read = models.BooleanField(_("Is Read"), default=False)
    read_at = models.DateTimeField(_("Read At"), null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.notification}"

    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save(update_fields=["is_read", "read_at"])
