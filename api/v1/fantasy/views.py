from django.db.models import Exists, Q, OuterRef
from rest_framework import generics, permissions

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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


round_param = openapi.Parameter(
    "round",
    openapi.IN_QUERY,
    description="Round number",
    type=openapi.TYPE_INTEGER,
)


class TeamDetailAPIView(generics.RetrieveAPIView):
    queryset = models.Team.objects.filter(is_deleted=False)
    serializer_class = serializers.TeamDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = self.queryset.filter(user_id=self.request.user.pk)
        return qs

    @swagger_auto_schema(manual_parameters=[round_param])
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["round"] = self.request.query_params.get("round")
        return context


# ========================== SQUAD START ==========================
class SquadDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = models.Squad.objects.filter(is_deleted=False)
    serializer_class = serializers.SquadDetailUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = self.queryset.filter(team__user_id=self.request.user.pk)
        return qs


class SquadPlayerDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = models.SquadPlayer.objects.filter(is_deleted=False)
    serializer_class = serializers.SquadPlayerDetailUpdateSerializer
    permission_classes = [api_permissions.TeamCompleteUserPermission]
    http_method_names = ["get", "put"]

    def get_queryset(self):
        qs = self.queryset.filter(
            squad__team__user_id=self.request.user.pk
        )
        return qs


class SquadSubstituteAPIView(generics.CreateAPIView):
    queryset = models.SquadPlayer
    serializer_class = serializers.SquadSubstituteSerializer
    permission_classes = (api_permissions.TeamCompleteUserPermission,)


# ========================== SQUAD END ==========================


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


class PrivateLeagueDetailAPIView(generics.RetrieveAPIView):
    queryset = models.FantasyLeague.objects.filter(
        is_deleted=False,
        type=data.LeagueStatusType.PRIVATE,
        status=data.LeagueStatusChoices.ACTIVE,
    )
    serializer_class = serializers.PrivateLeagueDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "invite_code"
