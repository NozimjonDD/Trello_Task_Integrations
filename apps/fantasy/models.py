from django.db import models

# Create your models here.
from apps.common.models import BaseModel
from apps.users.models import User


class Formation(BaseModel):
    title = models.CharField(max_length=255, null=True)
    schame = models.CharField(max_length=255, null=True)
    ordering = models.IntegerField(blank=True, null=True)


class Position(BaseModel):
    title = models.CharField(max_length=500, null=True)
    short_title = models.CharField(max_length=255, null=True)


class League(BaseModel):
    owner = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255, null=True)
    description = models.TextField()
    # type = models.CharField(choices=)
    invite_code = models.CharField(max_length=50, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Team(BaseModel):
    title = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(to=User, on_delete=models.DO_NOTHING)
    # status = models.CharField()
    formation = models.ForeignKey(to=Formation, on_delete=models.DO_NOTHING)


class TeamPlayer(BaseModel):
    team = models.ForeignKey(to=Team, on_delete=models.DO_NOTHING)
    # player = models.ForeignKey(to=Player, on_delete=models.DO_NOTHING)
    position = models.ForeignKey(to=Position, on_delete=models.DO_NOTHING)
    is_captain = models.BooleanField(default=False)
    is_substitution = models.BooleanField(default=False)
