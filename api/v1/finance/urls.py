from django.urls import path

from . import views

urlpatterns = [
    path("tariff-list/", views.TariffListAPIView.as_view(), name="tariff-list"),
    path("tariff-join/", views.TariffJoinAPIView.as_view(), name="tariff-join"),

    #
    # path("subscription/", views.SubscriptionAPIView.as_view(), name="subscription-join"),

]
