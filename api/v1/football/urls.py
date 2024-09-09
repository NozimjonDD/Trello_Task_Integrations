from django.urls import path

from . import views

urlpatterns = [
    path("player/", views.PlayerListAPIView.as_view(), name="player-list"),
    path("player/<int:pk>/", views.PlayerDetailAPIView.as_view(), name="player-detail"),

    # UpdatePremierLeague
    path("player-stat/", views.UpdatePremierLeagueStat.as_view(), name="premier-league-player-statics"),

    path("club/", views.ClubListAPIView.as_view(), name="club-list"),
    path("round/", views.RoundListAPIView.as_view(), name="round-list"),
    path("fixture/", views.FixtureListAPIView.as_view(), name="fixture-list"),
    path("fixture/<int:pk>/", views.FixtureDetailAPIView.as_view(), name="fixture-detail"),
]
