from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # HTML (páginas)
    path("", include("guide.urls")),

    # API (endpoints)
    path("api/", include("guide.api_urls")),
]