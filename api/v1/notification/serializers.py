from rest_framework import serializers
from apps.notification import models
from api.v1 import common_serializers


class _NotificationSerializer(serializers.ModelSerializer):
    type = common_serializers.NotificationTypeSerializer()

    class Meta:
        model = models.Notification
        fields = (
            "type",
            "title",
            "short_description",
        )


class UserNotificationListSerializer(serializers.ModelSerializer):
    notification = _NotificationSerializer()

    class Meta:
        model = models.UserNotification
        fields = (
            "id",
            "notification",
            "is_read",
            "read_at",
            "created_at",
        )


class _UserNDetailNotificationSerializer(serializers.ModelSerializer):
    type = common_serializers.NotificationTypeSerializer()
    template = common_serializers.NotificationTemplateSerializer()

    class Meta:
        model = models.Notification
        fields = (
            "type",
            "template",
            "title",
            "short_description",
            "description",
            "redirect_url",
            "target_id",
        )
        ref_name = "NotificationDetail"


class UserNotificationDetailUpdateSerializer(serializers.ModelSerializer):
    notification = _UserNDetailNotificationSerializer(read_only=True)

    class Meta:
        model = models.UserNotification
        fields = (
            "id",
            "notification",
            "is_read",
            "read_at",
            "created_at",
        )
        extra_kwargs = {
            "notification": {"read_only": True},
            "read_at": {"read_only": True},
            "is_read": {"required": True, "allow_null": False},
        }

    def update(self, instance, validated_data):
        is_read = validated_data["is_read"]

        if is_read:
            instance.mark_as_read()
            return instance
        return super().update(instance, validated_data)
