from django.db.models import Exists, Q, OuterRef
from rest_framework import generics, permissions
from rest_framework.generics import ListAPIView, CreateAPIView

from api.v1.finance.serializers import *
from apps.finance.models import Tariff


class TariffListAPIView(ListAPIView):
    queryset = Tariff.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TariffListSerializer


class TariffJoinAPIView(CreateAPIView):
    queryset = Tariff.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TariffJoinSerializer
