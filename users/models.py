from django.conf import settings

from django.contrib.auth.models import AbstractUser, Group as AbstractGroup
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django.db import models
from common.models import BaseModel
from . import utils


class User(AbstractUser, BaseModel):
    phone_number = models.CharField(
        verbose_name=_("phone number"),
        unique=True,
        error_messages={
            "unique": _("A user with that phone number already exists."),
        },
        max_length=13,
        validators=[utils.phone_number_validator]
    )
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=True,
        blank=True
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    middle_name = models.CharField(_("middle name"), max_length=150, blank=True)

    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    profile_picture = models.ImageField(
        verbose_name=_("profile picture"),
        upload_to="profile_pictures/",
        null=True,
        blank=True,
    )

    EMAIL_FIELD = None
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "user"
        ordering = ["-date_joined"]
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.phone_number

    def generate_otp(self):
        otp = self.user_otps.filter(
            is_deleted=False,
            is_confirmed=False,
            created_at__gt=timezone.now() - timezone.timedelta(seconds=settings.OTP_EXPIRATION_TIME)
        ).first()

        if otp:
            return otp

        otp = UserOTP.objects.create(user=self, code=utils.generate_otp())
        return otp


class AccountSettings(BaseModel):
    class Meta:
        db_table = "account_settings"
        verbose_name = _("Account settings")
        verbose_name_plural = _("Account settings")

    class LangChoices(models.TextChoices):
        UZ = "uz", _("O'zbekcha")
        RU = "ru", _("Русский")

    user = models.OneToOneField(
        to="User", on_delete=models.CASCADE, related_name="_account_settings", verbose_name=_("user")
    )
    lang = models.CharField(
        verbose_name=_("language"),
        max_length=2,
        choices=LangChoices.choices,
        default=LangChoices.UZ
    )
    push_notifications = models.BooleanField(
        verbose_name=_("push notifications"),
        default=True
    )

    def __str__(self):
        return f"{self.user} - account settings"


class GroupProxyModel(AbstractGroup):
    class Meta:
        proxy = True
        verbose_name = _("group")
        verbose_name_plural = _("groups")
        ordering = ["name"]


class UserOTP(BaseModel):
    class Meta:
        db_table = "user_otp"
        verbose_name = _("user OTP")
        verbose_name_plural = _("user OTPs")

    user = models.ForeignKey(
        to="User", on_delete=models.CASCADE, related_name="user_otps", verbose_name=_("user")
    )
    code = models.CharField(verbose_name=_("code"), max_length=10)
    secret = models.CharField(verbose_name=_("secret"), max_length=50, unique=True, default=utils.generate_secret)
    is_confirmed = models.BooleanField(verbose_name=_("is confirmed"), default=False)

    def __str__(self):
        return str(self.created_at)

    def is_expired(self):
        if self.is_confirmed or self.is_deleted:
            return True
        if timezone.now() - self.created_at > timezone.timedelta(seconds=settings.OTP_EXPIRATION_TIME):
            return True
        return False
