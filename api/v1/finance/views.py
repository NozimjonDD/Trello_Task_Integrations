from rest_framework import permissions
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response

from api.v1.finance.serializers import *
from apps.finance.models import *


class TariffListAPIView(ListAPIView):
    queryset = Tariff.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TariffListSerializer


class SubscriptionAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        tariff = int(self.request.data['tariff'])

        sub, _ = Subscription.objects.update_or_create(
            user_id=user.id,
            defaults={
                "user_id": user.id,
            }

        )
        sub.tariff.add(tariff)
        # calc = sub.calculate_total_price

        return Response({"user_id": user.id, "plans": sub.tariff.all().values(), "subscription_id": sub.id})
