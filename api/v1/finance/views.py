from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView

from api.v1.finance.serializers import *
from apps.finance.models import *


class TariffListAPIView(ListAPIView):
    queryset = Tariff.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TariffListSerializer


class TariffJoinAPIView(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TariffJoinSerializer


class SubscriptionListAPIView(ListAPIView):
    queryset = Subscription.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = Subscription


class SubscriptionAPIView(CreateAPIView):
    queryset = Subscription.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = Subscription
