from django.urls import path
from .views import home, title_detail

urlpatterns = [
    path("", home, name="home"),
    path("title/<str:tmdb_type>/<int:tmdb_id>/", title_detail, name="title_detail"),
]