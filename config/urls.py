from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("guide.urls")),              # páginas (home, detail)
    path("api/", include("guide.api_urls")),      # API (health, search)
]