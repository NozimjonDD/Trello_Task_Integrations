from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView, ListCreateAPIView
from rest_framework.response import Response

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
    serializer_class = SubscriptionListSerilalizer

    def get_queryset(self):
        queryset = self.queryset.all()
        print(55555555555)
        return queryset


class SubscriptionAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if not self.request.user.subscriptions:
            # sub = Subscription.objects.update_or_create(
            #     user_id=season["id"],
            #     defaults={
            #         "league": models.League.objects.get(remote_id=season["league_id"]),
            #         "name": season["name"],
            #
            # )

            print(self.request.user.subscriptions)

        return Response({"message": "class A", "count": 33333})
