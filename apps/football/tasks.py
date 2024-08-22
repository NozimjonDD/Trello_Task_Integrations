from celery import shared_task

from . import utils


@shared_task
def update_players_task():
    utils.update_players()
    print("=" * 200)
    print(" ======       PLAYERS UPDATED!       ===============")
    print("=" * 200)
