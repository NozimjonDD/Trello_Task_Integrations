from rest_framework import generics, permissions
from . import serializers
from apps.users import models
from apps.finance import models as finance_models


class AccountDetailAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.AccountDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserTariffListAPIView(generics.ListAPIView):
    queryset = finance_models.UserTariff.objects.filter(is_deleted=False)
    serializer_class = serializers.UserTariffListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user)
        qs = qs.select_related("tariff", "tariff_option", "season")
        return qs


class UserDeviceCreateAPIView(generics.CreateAPIView):
    queryset = models.Device.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.DeviceCreateSerializer
