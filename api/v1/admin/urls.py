from django.urls import path, include

urlpatterns = [
    # Fantasy
    path("fantasy/", include("api.v1.site.fantasy.urls")),

    # Football
    path("football/", include("api.v1.site.football.urls")),

]
