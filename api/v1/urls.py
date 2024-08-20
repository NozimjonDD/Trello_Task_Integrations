from django.urls import path, include

urlpatterns = [
    path("auth/", include("api.v1.auth.urls")),
    path("users/", include("api.v1.users.urls")),
    path("fantasy/", include("api.v1.fantasy.urls")),
    path("site/", include("api.v1.site.urls")),
]
