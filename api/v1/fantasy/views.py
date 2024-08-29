from django.db.models import Exists, Q, OuterRef
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny

from apps.fantasy import models
from apps.common import data
from api.v1 import permissions as api_permissions, common_serializers
from . import serializers


class FormationListAPIView(generics.ListAPIView):
    queryset = models.Formation.objects.filter(is_deleted=False)
    serializer_class = common_serializers.CommonFormationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = (
        "title",
    )
    pagination_class = None

    def get_queryset(self):
        qs = self.queryset.prefetch_related("positions")
        return qs.order_by("ordering")


class TeamCreateAPIView(generics.CreateAPIView):
    model = models.Team
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.TeamCreateSerializer


class TeamDetailAPIView(generics.RetrieveAPIView):
    queryset = models.Team.objects.filter(is_deleted=False)
    serializer_class = serializers.TeamDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = self.queryset.filter(user_id=self.request.user.pk)
        return qs


class SquadDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = models.Squad.objects.filter(is_deleted=False)
    serializer_class = serializers.SquadDetailUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = self.queryset.filter(team__user_id=self.request.user.pk)
        return qs


class SquadSubstituteAPIView(generics.CreateAPIView):
    queryset = models.SquadPlayer
    serializer_class = serializers.SquadSubstituteSerializer
    permission_classes = (api_permissions.TeamCompleteUserPermission,)


class TransferAPIView(generics.CreateAPIView):
    model = models.Transfer
    serializer_class = serializers.TransferSerializer
    permission_classes = [permissions.IsAuthenticated]


class PublicLeagueListAPIView(generics.ListAPIView):
    queryset = models.FantasyLeague.objects.filter(
        is_deleted=False,
        type=data.LeagueStatusType.PUBLIC,
        status=data.LeagueStatusChoices.ACTIVE,
    )
    serializer_class = serializers.PublicLeagueListSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = (
        "title",
    )

    def get_queryset(self):
        qs = self.queryset.annotate(
            joined=Exists(models.LeagueParticipant.objects.filter(
                league_id=OuterRef("pk"),
                team__user_id=self.request.user.pk,
            ))
        )
        return qs


class LeagueCreateAPIView(generics.CreateAPIView):
    model = models.FantasyLeague
    permission_classes = [api_permissions.TeamCompleteUserPermission]
    serializer_class = serializers.LeagueCreateSerializer


class LeagueJoinAPIView(generics.CreateAPIView):
    model = models.LeagueParticipant
    permission_classes = [api_permissions.TeamCompleteUserPermission]
    serializer_class = serializers.LeagueJoinSerializer
