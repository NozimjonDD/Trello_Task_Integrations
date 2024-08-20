from django.urls import path

from . import views

urlpatterns = [
    path("player/", views.PlayerListAPIView.as_view(), name="player-list"),
]
