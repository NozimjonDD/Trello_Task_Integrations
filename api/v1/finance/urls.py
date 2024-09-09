from django.urls import path

from . import views

urlpatterns = [
    # path("tariff-list/", views.TariffListAPIView.as_view(), name="tariff-list"),
    path("tariff-option-list/", views.TariffOptionListAPIView.as_view(), name="tariff-option-list"),
    path("tariff-order/", views.TariffOrderAPIView.as_view(), name="tariff-order"),

]
