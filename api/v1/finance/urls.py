from django.urls import path

from . import views

urlpatterns = [
    # path("tariff-list/", views.TariffListAPIView.as_view(), name="tariff-list"),
    path("tariff-option-list/", views.TariffOptionListAPIView.as_view(), name="tariff-option-list"),

    # Subscription
    # path("subscription/", views.SubscriptionAPIView.as_view(), name="subscription-join"),

]
