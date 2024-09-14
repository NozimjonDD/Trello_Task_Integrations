import random

from django.db.models import Value, BooleanField

import django_filters
from django_filters import rest_framework as filters

from apps.common import models


class NewsFilter(filters.FilterSet):
    is_recommended = django_filters.BooleanFilter(method="filter_is_recommended")

    class Meta:
        model = models.News
        fields = {
            'category': ['exact', 'in'],
        }

    def filter_is_recommended(self, queryset, name, value):
        if value is None:
            return queryset

        # TODO: add logic for recommended news
        queryset = queryset.annotate(
            is_recommended=Value(True, output_field=BooleanField())
        )

        if value:
            queryset = queryset.filter(
                is_recommended=True
            )
        else:
            queryset = queryset.filter(
                is_recommended=False
            )
        return queryset
