from django.urls import path

from . import views

urlpatterns = [
    path("notification/", views.UserNotificationListAPIView.as_view(), name="user-notification-list"),
    path(
        "notification/<int:pk>/",
        views.UserNotificationDetailUpdateDestroyAPIView.as_view(),
        name="user-notification-detail-update-destroy",
    ),
]
