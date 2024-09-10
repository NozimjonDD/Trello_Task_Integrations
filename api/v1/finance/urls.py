from django.urls import path

from . import views

urlpatterns = [
    # path("tariff-list/", views.TariffListAPIView.as_view(), name="tariff-list"),
    path("tariff-option-list/", views.TariffOptionListAPIView.as_view(), name="tariff-option-list"),
    path("tariff-order/", views.TariffOrderAPIView.as_view(), name="tariff-order"),

    # COIN
    path("coin-tariff/", views.CoinTariffListAPIView.as_view(), name="coin-tariff-list"),
    path("coin-order/", views.CoinOrderAPIView.as_view(), name="coin-order"),
]
