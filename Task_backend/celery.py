import environ  # noqa
from celery import Celery
from django.apps import apps
from django.conf import settings

env = environ.Env()
env.read_env(".env")

app = Celery("Task_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.config_from_object(settings)
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
