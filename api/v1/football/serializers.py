from rest_framework import serializers

from apps.football import models
from api.v1 import common_serializers


class PlayerListSerializer(serializers.ModelSerializer):
    profile_picture = serializers.URLField(source="profile_picture_path")
    club = common_serializers.CommonClubSerializer()
    position = common_serializers.CommonPositionSerializer()

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


class PlayerDetailSerializer(serializers.ModelSerializer):
    profile_picture = serializers.URLField(source="profile_picture_path")
    club = common_serializers.CommonClubSerializer()
    position = common_serializers.CommonPositionSerializer()

    match_count = serializers.IntegerField(default=0)
    goal_count = serializers.IntegerField(default=0)
    assist_count = serializers.IntegerField(default=0)
    yellow_card_count = serializers.IntegerField(default=0)

    class Meta:
        model = models.Player
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
            "common_name",

            "profile_picture",

            "club",
            "position",

            "date_of_birth",
            "age",
            "height",
            "weight",

            "market_value",
            "club_contract_until",

            "match_count",
            "goal_count",
            "assist_count",
            "yellow_card_count",
        )
