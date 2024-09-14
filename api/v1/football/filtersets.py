from django.utils import timezone
from django.db.models import Q
from django.conf import settings

import django_filters
from django_filters import rest_framework as filters

from apps.football import models, choices


class FixtureListFilter(filters.FilterSet):
    is_upcoming = django_filters.BooleanFilter(method="filter_is_upcoming")
    club = django_filters.NumberFilter(method="filter_club")
    match_date = django_filters.ChoiceFilter(
        choices=[
            ("last_gw", "Last Gameweek"),
            ("last_month", "Last Month"),
            ("last_season", "Last Season"),
        ],
        method="filter_match_date"
    )

    class Meta:
        model = models.Fixture
        fields = (
            "is_upcoming",
            "club",
            "match_date",
        )

    def filter_is_upcoming(self, queryset, name, value):
        if value is None:
            return queryset

        if value:
            queryset = queryset.filter(
                state__state__in=[
                    choices.FixtureStateChoices.NS,

                    choices.FixtureStateChoices.INPLAY_1ST_HALF,
                    choices.FixtureStateChoices.HT,
                    choices.FixtureStateChoices.BREAK,
                    choices.FixtureStateChoices.INPLAY_ET,
                    choices.FixtureStateChoices.AET,
                    choices.FixtureStateChoices.FT_PEN,
                    choices.FixtureStateChoices.INPLAY_PENALTIES,

                    choices.FixtureStateChoices.PEN_BREAK,
                    choices.FixtureStateChoices.INPLAY_ET_2ND_HALF,
                    choices.FixtureStateChoices.INPLAY_2ND_HALF,
                    choices.FixtureStateChoices.EXTRA_TIME_BREAK,
                ]
            )
        else:
            queryset = queryset.filter(
                state__state__in=[
                    choices.FixtureStateChoices.FT,
                ]
            )
        return queryset

    def filter_club(self, queryset, name, value):
        if value is None:
            return queryset

        return queryset.filter(
            Q(home_club_id=value) | Q(away_club_id=value)
        )

    def filter_match_date(self, queryset, name, value):
        if value is None:
            return queryset

        last_month_year = timezone.now().date().year
        last_month_month = timezone.now().date().month - 1

        if last_month_month == 0:
            last_month_year -= 1
            last_month_month = 12

        if value == "last_gw":
            return queryset.filter(round=models.Round.get_last_gw())
        elif value == "last_month":
            return queryset.filter(match_date__year=last_month_year, match_date__month=last_month_month)
        elif value == "last_season":
            return queryset.filter(
                round__season=models.League.objects.get(remote_id=settings.PREMIER_LEAGUE_ID).get_last_season()
            )
        return queryset
