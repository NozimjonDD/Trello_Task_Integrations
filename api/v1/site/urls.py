from django.urls import path, include

from api.v1.site.football.views import AStat

urlpatterns = [
    # Football
    path("football/", include("api.v1.site.football.urls")),
    path("stat/", AStat.as_view()),

]
