from django.urls import path, include

urlpatterns = [
    path("auth/", include("api.v1.auth.urls")),
    path("finance/", include("api.v1.finance.urls")),
    path("users/", include("api.v1.users.urls")),
    path("fantasy/", include("api.v1.fantasy.urls")),
    path("football/", include("api.v1.football.urls")),
]
