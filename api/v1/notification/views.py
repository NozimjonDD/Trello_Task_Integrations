from rest_framework import generics, permissions

from . import serializers
from apps.notification import models


class UserNotificationListAPIView(generics.ListAPIView):
    queryset = models.UserNotification.objects.filter(is_deleted=False)
    serializer_class = serializers.UserNotificationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["notification__title", "notification__short_description"]
    filterset_fields = {
        "is_read": ["exact"],
    }
    ordering_fields = ["created_at", "is_read"]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-created_at")


class UserNotificationDetailUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.UserNotification.objects.all()
    serializer_class = serializers.UserNotificationDetailUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "put", "delete"]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, is_deleted=False)

    def get_object(self):
        instance = super().get_object()

        if not instance.is_read:
            instance.mark_as_read()
        return instance

    def perform_destroy(self, instance):
        instance.soft_delete()
