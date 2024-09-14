from rest_framework import generics, permissions

from . import serializers, filtersets
from api.v1 import common_serializers
from apps.common import models


class NewsCategoryListAPIView(generics.ListAPIView):
    queryset = models.NewsCategory.objects.filter(is_deleted=False)
    serializer_class = common_serializers.CommonNewsCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['title']
    pagination_class = None


class BreakingNewsListAPIView(generics.ListAPIView):
    queryset = models.News.objects.filter(is_deleted=False).order_by('-published_at')[:5]
    serializer_class = serializers.NewsListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    search_fields = ['title']
    filterset_fields = {
        'category': ['exact', "in"],
    }


class NewsListAPIView(generics.ListAPIView):
    queryset = models.News.objects.filter(is_deleted=False)
    serializer_class = serializers.NewsListSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['title']
    filterset_class = filtersets.NewsFilter

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.select_related('category')
        return queryset.order_by('-published_at')


class NewsDetailAPIView(generics.RetrieveAPIView):
    queryset = models.News.objects.all()
    serializer_class = serializers.NewsDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
