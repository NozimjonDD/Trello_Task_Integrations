from django.db import models


class LeagueStatusType(models.TextChoices):
    PUBLIC = 'Public', 'public',
    PRIVATE = 'Private', 'private',


class TeamStatusChoices(models.TextChoices):
    ACTIVE = 'Active', 'active',
    INACTIVE = 'Inactive', 'inactive',


class UserRoleChoices(models.TextChoices):
    USER = 'User', 'user',
    ADMIN = 'Admin', 'admin',
    MODERATOR = 'Moderator', 'moderator',
