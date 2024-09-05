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


class PlayerImageFormetion(serializers.ModelSerializer):
    class Meta:
        model = football_models.Club
        fields = (
            "kit_home",
            "kit_away",
        )


class CommonClubSerializer(serializers.ModelSerializer):
    logo = serializers.URLField(source="logo_path")
    kit = serializers.ImageField(source="kit_home")

    class Meta:
        model = football_models.Club
        fields = (
            "id",
            "name",
            "short_name",
            "logo",
            "kit",
            # "kit_home",
            # "kit_away",
            "founded_year",
        )

    def to_representation(self, instance: football_models.Club):
        data = super().to_representation(instance)

        # if Round.objects.filter(fixtures__away_club)
        # if instance.kit_home:
        #     data['kit'] = PlayerImageFormetion(instance, context=self.context, many=False).data
        # else:
        #     pass

        data['game_location'] = "home"

        return data


class CommonFormationSerializer(serializers.ModelSerializer):
    scheme = serializers.ListField(source="scheme_as_list")

    class Meta:
        model = fantasy_models.Formation
        fields = (
            "id",
            "title",
            "scheme",
        )


class CommonFormationPositionSerializer(serializers.ModelSerializer):
    position = CommonPositionSerializer()

    class Meta:
        model = fantasy_models.FormationPosition
        fields = (
            "id",
            "position",
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
            "pretty_market_value",
        )


class CommonFixtureStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = football_models.FixtureState
        fields = (
            "id",
            "state",
            "title",
        )


class CommonRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = football_models.Round
        fields = (
            "id",
            "name",
            "is_finished",
            "is_current",
            "starting_at",
            "ending_at",
        )


class CommonLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = fantasy_models.Level
        fields = (
            "id",
            "title",
            "icon",
            "level_point",
            "description",
        )
