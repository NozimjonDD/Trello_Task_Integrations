from django.urls import path, include

urlpatterns = [
    path("auth/", include("api.v1.auth.urls")),
    path("users/", include("api.v1.users.urls")),
    path("common/", include("api.v1.common.urls")),
    path("fantasy/", include("api.v1.fantasy.urls")),
    path("football/", include("api.v1.football.urls")),
    path("finance/", include("api.v1.finance.urls")),
    path("notification/", include("api.v1.notification.urls")),
]
