from django.urls import path

from . import views

urlpatterns = [
    path("news-category/", views.NewsCategoryListAPIView.as_view(), name="news-category-list"),
    path("breaking-news/", views.BreakingNewsListAPIView.as_view(), name="breaking-news-list"),
    path("news/", views.NewsListAPIView.as_view(), name="news-list"),
    path("news/<int:pk>/", views.NewsDetailAPIView.as_view(), name="news-detail"),
]
