from rest_framework import generics, permissions
from rest_framework.generics import ListAPIView

from apps.finance.models import Tariff, Subscription
from . import serializers
from .serializers import SubscriptionListSerilalizer


class AccountDetailAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.AccountDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserTariffListAPIView(generics.ListAPIView):
    queryset = Tariff.objects.all()
    serializer_class = serializers.UserTariffListSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubscriptionListAPIView(ListAPIView):
    queryset = Subscription.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubscriptionListSerilalizer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
