from rest_framework import generics, permissions

from apps.finance.models import Tariff
from . import serializers


class AccountDetailAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.AccountDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserTariffListAPIView(generics.ListAPIView):
    queryset = Tariff.objects.all()
    serializer_class = serializers.UserTariffListSerializer
    permission_classes = [permissions.IsAuthenticated]


