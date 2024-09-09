import django_filters
from django_filters import rest_framework as filters

from apps.football import models, choices


class FixtureListFilter(filters.FilterSet):
    is_upcoming = django_filters.BooleanFilter(method="filter_is_upcoming")

    class Meta:
        model = models.Fixture
        fields = (
            "is_upcoming",
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
