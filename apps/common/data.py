from django.db import models


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
