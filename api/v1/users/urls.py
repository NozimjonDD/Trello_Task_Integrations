from django.urls import path

from . import views

urlpatterns = [
    path("account/", views.AccountDetailAPIView.as_view(), name="account_detail"),
    path("tariff-list/", views.UserTariffListAPIView.as_view(), name="user-tariff-list"),
    path("subscription/list/", views.SubscriptionListAPIView.as_view(), name="subscription-list"),

]
