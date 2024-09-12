from rest_framework import generics, permissions
from apps.finance.models import Tariff
from . import serializers
from apps.users import models


class AccountDetailAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.AccountDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserTariffListAPIView(generics.ListAPIView):
    queryset = Tariff.objects.all()
    serializer_class = serializers.UserTariffListSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDeviceCreateAPIView(generics.CreateAPIView):
    queryset = models.Device.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.DeviceCreateSerializer
