from django.urls import path
from .views import home, title_detail, HealthView, SearchView

urlpatterns = [
    path("", home, name="home"),
    path("title/<str:tmdb_type>/<int:tmdb_id>/", title_detail, name="title_detail"),
    path("health", HealthView.as_view()),
    path("search", SearchView.as_view()),
]