from rest_framework import generics, permissions

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
