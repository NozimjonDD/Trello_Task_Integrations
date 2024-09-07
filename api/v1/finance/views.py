from rest_framework import permissions
from rest_framework.generics import ListAPIView, GenericAPIView

from api.v1.finance import serializers
from apps.finance.models import *


class TariffListAPIView(ListAPIView):
    queryset = Tariff.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.TariffListSerializer


class TariffOptionListAPIView(ListAPIView):
    queryset = TariffOption.objects.filter(is_deleted=False).order_by("ordering")
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.TariffOptionListSerializer
    filterset_fields = {
        "tariff__type": ["exact"],
    }
    pagination_class = None
