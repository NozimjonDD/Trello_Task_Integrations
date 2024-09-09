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


class _FixtureEventSerializer(serializers.ModelSerializer):
    player = common_serializers.CommonPlayerSerializer(many=False)
    related_player = common_serializers.CommonPlayerSerializer(many=False)
    type = common_serializers.CommonSportMonksTypeSerializer()
    sub_type = common_serializers.CommonSportMonksTypeSerializer()

    class Meta:
        model = models.FixtureEvent
        fields = (
            "id",
            "club",
            "player",
            "related_player",
            "type",
            "sub_type",

            "minute",
            "extra_minute",
        )


class _FixtureStatisticSerializer(serializers.ModelSerializer):
    type = common_serializers.CommonSportMonksTypeSerializer()

    class Meta:
        model = models.FixtureStatistic
        fields = (
            "id",
            "club",
            "type",
            "value",
        )


class FixtureDetailSerializer(serializers.ModelSerializer):
    home_club = common_serializers.CommonClubSerializer()
    away_club = common_serializers.CommonClubSerializer()
    state = common_serializers.CommonFixtureStateSerializer()

    home_club_goals = serializers.SerializerMethodField()
    away_club_goals = serializers.SerializerMethodField()

    home_club_assists = serializers.SerializerMethodField()
    away_club_assists = serializers.SerializerMethodField()

    home_club_yellow_cards = serializers.SerializerMethodField()
    away_club_yellow_cards = serializers.SerializerMethodField()

    home_club_red_cards = serializers.SerializerMethodField()
    away_club_red_cards = serializers.SerializerMethodField()

    home_club_saves = serializers.SerializerMethodField()
    away_club_saves = serializers.SerializerMethodField()

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

            "home_club_goals",
            "away_club_goals",
            "home_club_assists",
            "away_club_assists",
            "home_club_yellow_cards",
            "away_club_yellow_cards",
            "home_club_red_cards",
            "away_club_red_cards",
            "home_club_saves",
            "away_club_saves",
        )

    @staticmethod
    def get_home_club_goals(obj):
        events = obj.events.filter(
            type__developer_name__in=["GOAL", "OWNGOAL"],
            club=obj.home_club,
        )
        serializer = _FixtureEventSerializer(events, many=True)
        return serializer.data

    @staticmethod
    def get_away_club_goals(obj):
        events = obj.events.filter(
            type__developer_name__in=["GOAL", "OWNGOAL"],
            club=obj.away_club,
        )
        serializer = _FixtureEventSerializer(events, many=True)
        return serializer.data

    @staticmethod
    def get_home_club_assists(obj):
        events = obj.events.filter(
            type__developer_name="GOAL",
            club=obj.home_club,
        )
        serializer = _FixtureEventSerializer(events, many=True)
        return serializer.data

    @staticmethod
    def get_away_club_assists(obj):
        events = obj.events.filter(
            type__developer_name="GOAL",
            club=obj.away_club,
        )
        serializer = _FixtureEventSerializer(events, many=True)
        return serializer.data

    @staticmethod
    def get_home_club_yellow_cards(obj):
        events = obj.events.filter(
            type__developer_name="YELLOWCARD",
            club=obj.home_club,
        )
        serializer = _FixtureEventSerializer(events, many=True)
        return serializer.data

    @staticmethod
    def get_away_club_yellow_cards(obj):
        events = obj.events.filter(
            type__developer_name="YELLOWCARD",
            club=obj.away_club,
        )
        serializer = _FixtureEventSerializer(events, many=True)
        return serializer.data

    @staticmethod
    def get_home_club_red_cards(obj):
        events = obj.events.filter(
            type__developer_name__in=["YELLOWREDCARD", "REDCARD"],
            club=obj.home_club,
        )
        serializer = _FixtureEventSerializer(events, many=True)
        return serializer.data

    @staticmethod
    def get_away_club_red_cards(obj):
        events = obj.events.filter(
            type__developer_name__in=["YELLOWREDCARD", "REDCARD"],
            club=obj.away_club,
        )
        serializer = _FixtureEventSerializer(events, many=True)
        return serializer.data

    @staticmethod
    def get_home_club_saves(obj):
        stats = obj.statistics.filter(
            type__developer_name="SAVES",
            club=obj.home_club,
        ).last()
        serializer = _FixtureStatisticSerializer(stats, many=False)
        return serializer.data

    @staticmethod
    def get_away_club_saves(obj):
        stats = obj.statistics.filter(
            type__developer_name="SAVES",
            club=obj.away_club,
        ).last()
        serializer = _FixtureStatisticSerializer(stats, many=False)
        return serializer.data
