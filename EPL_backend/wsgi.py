import environ  # noqa
from django.core.wsgi import get_wsgi_application

environ.Env().read_env(".env")

application = get_wsgi_application()
