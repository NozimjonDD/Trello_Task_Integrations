from rest_framework import serializers

from apps.fantasy import models


class _FormationPositionSerializer(serializers.ModelSerializer):
    position__id = serializers.IntegerField(source="position.pk")
    position__name = serializers.StringRelatedField(source="position.name")
    position__short_name = serializers.StringRelatedField(source="position.short_name")

    class Meta:
        model = models.FormationPosition
        fields = (
            "id",
            "index",
            "position__id",
            "position__name",
            "position__short_name",
        )


class FormationListSerializer(serializers.ModelSerializer):
    positions = _FormationPositionSerializer(many=True)

    class Meta:
        model = models.Formation
        fields = (
            "id",
            "title",
            "positions",
        )
