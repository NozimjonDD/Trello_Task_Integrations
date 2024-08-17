from django.urls import path, include

urlpatterns = [
    path("auth/", include("api.v1.auth.urls")),
    path("site/", include("api.v1.site.urls")),
    path("admin/", include("api.v1.admin.urls")),
]
