from django.conf import settings

from rest_framework import generics, permissions
from rest_framework import views
from rest_framework.response import Response
from apps.football.utils import update_premierleague_status_by_players
from . import serializers
from apps.football import models


class PlayerListAPIView(generics.ListAPIView):
    queryset = models.Player.objects.filter(is_deleted=False, club__league__remote_id=settings.PREMIER_LEAGUE_ID)
    serializer_class = serializers.PlayerListSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ("first_name", "last_name", "common_name", "full_name",)

    filterset_fields = {
        "position": ["exact", "in"],
        "club": ["exact", "in"],
        "position__remote_id": ["exact", "in"]
    }

    def get_queryset(self):
        qs = self.queryset

        if hasattr(self.request.user, "team"):
            qs = qs.exclude(team_players__team_id=self.request.user.team.id)
        qs = qs.select_related("club", "position")
        return qs


class PlayerDetailAPIView(generics.RetrieveAPIView):
    queryset = models.Player.objects.filter(is_deleted=False, club__league__remote_id=settings.PREMIER_LEAGUE_ID)
    serializer_class = serializers.PlayerDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class UpdatePremierLeagueStat(views.APIView):
    def post(self, request, *args, **kwargs):
        count = update_premierleague_status_by_players()

        return Response({"message": "class A", "count": count})


class ClubListAPIView(generics.ListAPIView):
    queryset = models.Club.objects.filter(is_deleted=False, league__remote_id=settings.PREMIER_LEAGUE_ID)
    serializer_class = serializers.ClubListSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ("name", "short_name",)


class RoundListAPIView(generics.ListAPIView):
    queryset = models.Round.objects.filter(is_deleted=False, league__remote_id=settings.PREMIER_LEAGUE_ID)
    serializer_class = serializers.RoundListSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = (
        "name",
    )
    pagination_class = None

    def get_queryset(self):
        qs = self.queryset
        return qs.order_by("starting_at", )
