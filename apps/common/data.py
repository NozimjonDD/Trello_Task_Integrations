from django.db import models
from django.utils.translation import gettext_lazy as _


class LeagueStatusType(models.TextChoices):
    PUBLIC = 'public', 'Public',
    PRIVATE = 'private', 'Private',


class LeagueStatusChoices(models.TextChoices):
    PENDING = "pending", _("Pending")
    ACTIVE = "active", _("Active")
    INACTIVE = "inactive", _("Inactive")
    SUSPENDED = "suspended", _("Suspended")
    FINISHED = "finished", _("Finished")


class LeagueParticipantStatusChoices(models.TextChoices):
    ACTIVE = "active", _("Active")
    SUSPENDED = "suspended", _("Suspended")


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


class TariffTypeChoices(models.TextChoices):
    TRIPLE_CAPTAIN = 'triple_captain', _("Triple captain")
    TRANSFER = 'transfer', _("Transfer")
    JOIN_LEAGUE = "join_league", _("League join")


class TariffOrderStatusChoices(models.TextChoices):
    PENDING = "pending", _("Pending")
    PAYMENT_PROCESSING = "payment_processing", _("Payment processing")
    SUCCESS = "success", _("Success")
    CANCELED = "canceled", _("Canceled")
    REJECTED = "rejected", _("Rejected")


class OrderPaymentTypeChoices(models.TextChoices):
    CLICK = "click", _("Click")
    PAYME = "payme", _("Payme")
    UZUM_BANK = "uzum_bank", _("Uzum bank")


class TransactionStatusChoices(models.TextChoices):
    PROCESSING = "processing", _("Processing")
    FINISHED = "finished", _("Finished")
    CANCELED = "canceled", _("Canceled")
    ERROR = "error", _("Error")


class NotificationTypeChoices(models.TextChoices):
    INFORMATIONAL = "INFORMATIONAL", _("Informational")
    USER_ENGAGEMENT = "USER_ENGAGEMENT", _("User Engagement")
    TRANSACTIONAL = "TRANSACTIONAL", _("Transactional")
    PROMOTIONAL = "PROMOTIONAL", _("Promotional")


class NotificationDetailedEventTypes(models.TextChoices):
    APP_VERSION_UPDATED = "APP_VERSION_UPDATED", _("App version updated")
    COIN_ORDER_CREATED = "COIN_ORDER_CREATED", _("Coin order created")
    COIN_ORDER_PAYMENT_PROCESSING = "COIN_ORDER_PAYMENT_PROCESSING", _("Coin order payment processing")
    COIN_ORDER_PAYMENT_RECEIVED = "COIN_ORDER_PAYMENT_RECEIVED", _("Coin order payment received")
    COIN_ORDER_COMPLETED = "COIN_ORDER_COMPLETED", _("Coin Order Completed")
    COIN_ORDER_CANCELED = "COIN_ORDER_CANCELED", _("Coin Order Canceled")
    COIN_ORDER_FAILED = "COIN_ORDER_FAILED", _("Coin Order Failed")
