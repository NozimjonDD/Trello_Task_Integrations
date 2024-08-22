from rest_framework import generics, permissions
from rest_framework import views
from rest_framework.response import Response
from apps.football.utils import update_premierleague_status_by_players
from . import serializers
from apps.football import models


class PlayerListAPIView(generics.ListAPIView):
    queryset = models.Player.objects.filter(is_deleted=False, club__league__remote_id=271)
    serializer_class = serializers.PlayerListSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ("first_name", "last_name", "common_name", "full_name",)

    filterset_fields = {
        "position": ["exact", "in"],
        "club": ["exact", "in"],
        "position__remote_id": ["exact", "in"]
    }

    def get_queryset(self):
        qs = self.queryset.select_related("club", "position")
        return qs


class PlayerDetailAPIView(generics.RetrieveAPIView):
    queryset = models.Player.objects.filter(is_deleted=False, club__league__remote_id=271)
    serializer_class = serializers.PlayerDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class UpdatePremierLeagueStat(views.APIView):
    def post(self, request, *args, **kwargs):
        count = update_premierleague_status_by_players()

        return Response({"message": "class A", "count": count})