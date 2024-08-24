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
            "jersey_number",

            "height",
            "weight",

            "market_value",
            "pretty_market_value",
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
            "jersey_number",

            "date_of_birth",
            "age",
            "height",
            "weight",

            "market_value",
            "pretty_market_value",
            "club_contract_until",

            "match_count",
            "goal_count",
            "assist_count",
            "yellow_card_count",
        )


class ClubListSerializer(serializers.ModelSerializer):
    logo = serializers.URLField(source="logo_path")

    class Meta:
        model = models.Club
        fields = (
            "id",
            "name",
            "short_name",
            "logo",
        )


class RoundListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Round
        fields = (
            "id",
            "name",
            "is_finished",
            "is_current",
            "starting_at",
            "ending_at",
        )


class FixtureListSerializer(serializers.ModelSerializer):
    home_club = common_serializers.CommonClubSerializer()
    away_club = common_serializers.CommonClubSerializer()
    state = common_serializers.CommonFixtureStateSerializer()

    class Meta:
        model = models.Fixture
        fields = (
            "id",
            "title",
            "round",
            "home_club",
            "away_club",
            "home_club_score",
            "away_club_score",
            "state",
            "match_date",
        )
