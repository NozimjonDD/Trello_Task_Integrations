from django.urls import path

from . import views

urlpatterns = [
    path("account/", views.AccountDetailAPIView.as_view(), name="account_detail")
]
