from django.urls import path, include

from api.v1.site.football.views import *

urlpatterns = [
    # Football
    path("football/", include("api.v1.site.football.urls")),
    path("stat/", UpgadePremierLeagueStat.as_view(),  name="premier-league-player-statics"),

]
