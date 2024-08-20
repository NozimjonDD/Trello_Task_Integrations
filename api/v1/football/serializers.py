from rest_framework import serializers

from apps.football import models


class _ClubSerializer(serializers.ModelSerializer):
    logo = serializers.URLField(source="logo_path")

    class Meta:
        model = models.Club
        fields = (
            "id",
            "name",
            "short_name",
            "logo",
        )


class _PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = (
            "id",
            "name",
            "short_name",
        )


class PlayerListSerializer(serializers.ModelSerializer):
    profile_picture = serializers.URLField(source="profile_picture_path")
    club = _ClubSerializer()
    position = _PositionSerializer()

    class Meta:
        model = models.Player
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
            "common_name",

            "profile_picture",
            "date_of_birth",

            "club",
            "position",

            "height",
            "weight",

            "market_value",
        )
