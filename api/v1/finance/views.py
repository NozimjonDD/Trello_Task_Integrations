from rest_framework import generics, permissions

from apps.fantasy import models
from . import serializers


class FormationListAPIView(generics.ListAPIView):
    queryset = models.Formation.objects.filter(is_deleted=False)
    serializer_class = serializers.FormationListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = (
        "title",
    )

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
