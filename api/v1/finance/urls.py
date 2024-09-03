from django.urls import path

from . import views

urlpatterns = [
    path("tariff-list/", views.TariffListAPIView.as_view(), name="tariff-list"),

    #
    path("subscription/list/", views.SubscriptionListAPIView.as_view(), name="subscription-list"),
    path("subscription/", views.SubscriptionAPIView.as_view(), name="subscription-join"),

]
