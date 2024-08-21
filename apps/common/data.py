from django.db import models
from django.utils.translation import gettext_lazy as _


class LeagueStatusType(models.TextChoices):
    PUBLIC = 'public', 'Public',
    PRIVATE = 'private', 'Private',


class TeamStatusChoices(models.TextChoices):
    ACTIVE = 'active', 'Active',
    INACTIVE = 'inactive', 'Inactive',
    DRAFT = "draft", "Draft"


class UserRoleChoices(models.TextChoices):
    USER = 'user', 'User',
    ADMIN = 'admin', 'Admin',
    MODERATOR = 'moderator', 'Moderator',


class TransferTypeChoices(models.TextChoices):
    SELL = "sell", _("Sell")
    BUY = "buy", _("Buy")
    SWAP = "swap", _("Swap")
