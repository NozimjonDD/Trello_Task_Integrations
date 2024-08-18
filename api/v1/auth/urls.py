from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("register/", views.UserRegisterAPIView.as_view(), name="register"),
    path("register/confirm/", views.UserRegisterConfirmAPIView.as_view(), name="register_confirm"),

    # path("reset-password/", views.ResetPasswordAPIView.as_view(), name="reset_password"),
    path("change-password/", views.ChangePasswordAPIView.as_view(), name="change_password"),
]
