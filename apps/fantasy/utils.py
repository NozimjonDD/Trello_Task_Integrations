import secrets
import string

from django.conf import settings

from . import models
from apps.football import models as football_models


def generate_league_invite_code(length=6):
    chars = string.ascii_uppercase + string.digits

    code = "".join(secrets.choice(chars) for _ in range(length))
    return code


def calculate_player_round_points(rnd):
    players = football_models.Player.objects.filter(
        is_deleted=False,
        club__league__remote_id=settings.PREMIER_LEAGUE_ID,
    )

    for player in players:
        round_point, _ = models.PlayerRoundPoint.objects.update_or_create(
            player_id=player.pk,
            round_id=rnd.pk,
            defaults={
                "point": 0,
            }
        )


def calculate_gk_round_points(rnd, player):
    fixture_events = football_models.FixtureEvent.objects.filter(fixture__round_id=rnd.pk)

    points = 0

    # 70 min
    subs = fixture_events.filter(
        type=football_models.SportMonksType.objects.get(developer_name="SUBSTITUTION"),
        related_player_id=player.pk,
    )
    if subs:
        if subs.minute <= 70:
            points += 1
        else:
            points += 2
    else:
        points += 2

    # goals
    points += fixture_events.filter(player_id=player.pk, type__developer_name="GOAL").count() * 10

    # assists
    points += fixture_events.filter(related_player_id=player.pk, type__developer_name="GOAL").count() * 10

    return points
