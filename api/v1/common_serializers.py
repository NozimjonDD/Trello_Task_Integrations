from rest_framework import serializers

from apps.fantasy import models as fantasy_models
from apps.football import models as football_models


class CommonPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = football_models.Position
        fields = (
            "id",
            "name",
            "short_name",
        )


class CommonClubSerializer(serializers.ModelSerializer):
    logo = serializers.URLField(source="logo_path")

    class Meta:
        model = football_models.Club
        fields = (
            "id",
            "name",
            "short_name",
            "logo",
            "kit",
            "founded_year",
        )


class CommonFormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = fantasy_models.Formation
        fields = (
            "id",
            "title",
        )


class CommonFormationPositionSerializer(serializers.ModelSerializer):
    position = CommonPositionSerializer()

    class Meta:
        model = fantasy_models.FormationPosition
        fields = (
            "id",
            "position",
            "index",
        )


class CommonPlayerSerializer(serializers.ModelSerializer):
    club = CommonClubSerializer()
    position = CommonPositionSerializer()
    profile_picture = serializers.URLField(source="profile_picture_path")

    class Meta:
        model = football_models.Player
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
            "common_name",
            "profile_picture",

            "club",
            "position",

            "market_value",
        )
