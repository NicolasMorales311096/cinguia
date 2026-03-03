from django.urls import path
from .views import home, title_detail, HealthView, SearchView

urlpatterns = [
    # Web
    path("", home, name="home"),
    path("title/<str:tmdb_type>/<int:tmdb_id>/", title_detail, name="title_detail"),

    # API
    path("api/health/", HealthView.as_view(), name="health"),
    path("api/search/", SearchView.as_view(), name="search"),
]