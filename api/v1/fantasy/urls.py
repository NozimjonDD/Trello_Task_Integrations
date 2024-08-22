from django.urls import path
from . import views

urlpatterns = [
    path("formation/", views.FormationListAPIView.as_view(), name="formation-list"),
    path("team-create/", views.TeamCreateAPIView.as_view(), name="team-create"),
    path("team/<int:pk>/", views.TeamDetailAPIView.as_view(), name="team-detail"),
    path(
        "squad/<int:pk>/", views.SquadDetailUpdateAPIView.as_view(), name="squad-detail-update"
    ),

    path("transfer/", views.TransferAPIView.as_view(), name="player-transfer"),
]
