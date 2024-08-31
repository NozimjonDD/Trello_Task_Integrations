import environ  # noqa
from celery import Celery
from celery.schedules import crontab

from django.apps import apps
from django.conf import settings

env = environ.Env()
env.read_env(".env")

app = Celery("EPL_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.config_from_object(settings)
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

app.conf.beat_schedule = {
    "check_and_update_fixture_detail": {
        "task": "check_and_update_fixture_detail",
        "schedule": crontab(minute="*/1"),
        'args': (),
    },
}
