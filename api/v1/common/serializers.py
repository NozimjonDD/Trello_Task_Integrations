from rest_framework import serializers

from apps.common import models
from api.v1 import common_serializers


class NewsListSerializer(serializers.ModelSerializer):
    category = common_serializers.CommonNewsCategorySerializer()

    class Meta:
        model = models.News
        fields = (
            "id",
            "category",
            "title",
            "image",
            "published_at",
        )


class NewsDetailSerializer(serializers.ModelSerializer):
    category = common_serializers.CommonNewsCategorySerializer()

    class Meta:
        model = models.News
        fields = (
            "id",
            "category",
            "title",
            "image",
            "content",
            "published_at",
        )
