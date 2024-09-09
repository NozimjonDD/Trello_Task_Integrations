from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from django.db.models import Q

from . import models, utils
from apps.football import models as football_models, choices as football_choices
from apps.football import utils as football_utils


@shared_task(name="check_and_update_fixture_detail")
def check_and_update_fixture_detail():
    updatable_fixtures = football_models.Fixture.objects.filter(
        match_date__lte=timezone.now() + timedelta(minutes=10),
    ).exclude(state__state=football_choices.FixtureStateChoices.FT)

    print(updatable_fixtures)

    for fixture in updatable_fixtures:
        football_utils.update_fixture_by_id(fixture.remote_id)
        fixture.refresh_from_db()

        utils.update_fixture_player_rnd_points(fixture)
