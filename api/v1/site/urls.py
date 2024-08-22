from django.urls import path, include

urlpatterns = [
    # Football
    path("football/", include("api.v1.site.football.urls")),

]
