from django.urls import path

from . import views

urlpatterns = [
    path("player/", views.PlayerListAPIView.as_view(), name="player-list"),
    path("player/<int:pk>/", views.PlayerDetailAPIView.as_view(), name="player-detail"),

    path("club/", views.ClubListAPIView.as_view(), name="club-list"),
]
