from rest_framework import permissions
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView

from api.v1 import permissions as api_permissions
from api.v1.finance import serializers
from apps.finance import models


class TariffListAPIView(ListAPIView):
    queryset = models.Tariff.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.TariffListSerializer


class TariffOptionListAPIView(ListAPIView):
    queryset = models.TariffOption.objects.filter(is_deleted=False).order_by("ordering")
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.TariffOptionListSerializer
    filterset_fields = {
        "tariff__type": ["exact"],
    }
    pagination_class = None


class TariffOrderAPIView(CreateAPIView):
    model = models.TariffOrder
    permission_classes = (api_permissions.TeamCompleteUserPermission,)
    serializer_class = serializers.TariffOrderSerializer
