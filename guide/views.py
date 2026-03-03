import os
from django.shortcuts import render
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import SearchHistory
from .tmdb_client import (
    search_movie,
    search_tv,
    movie_watch_providers,
    tv_watch_providers,
    movie_details,
    tv_details,
    movie_videos,
    tv_videos,
)

# ✅ Página principal con historial (NO revienta si faltan migraciones/tablas)
def home(request):
    try:
        last_searches = SearchHistory.objects.order_by("-created_at")[:10]
    except Exception:
        last_searches = []
    return render(request, "guide/home.html", {"last_searches": last_searches})


class HealthView(APIView):
    def get(self, request):
        return Response({"status": "ok", "app": "CinGuia"})


def _pick_providers(region_data: dict) -> dict:
    out = {"link": region_data.get("link", ""), "flatrate": [], "rent": [], "buy": []}

    for offer_type in ["flatrate", "rent", "buy"]:
        for p in (region_data.get(offer_type) or []):
            out[offer_type].append(
                {
                    "provider_id": p.get("provider_id"),
                    "provider_name": p.get("provider_name"),
                    "logo_path": p.get("logo_path"),
                }
            )
    return out


class SearchView(APIView):
    def get(self, request):
        q = (request.query_params.get("q") or "").strip()
        tmdb_type = (request.query_params.get("type") or "movie").strip().lower()
        region = (request.query_params.get("region") or os.getenv("TMDB_REGION", "CL")).strip().upper()

        if not q:
            return Response({"error": "Falta el parámetro 'q'."}, status=status.HTTP_400_BAD_REQUEST)

        if tmdb_type not in ["movie", "tv"]:
            return Response(
                {"error": "El parámetro 'type' debe ser 'movie' o 'tv'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        raw = search_tv(q) if tmdb_type == "tv" else search_movie(q, region)
        results = (raw.get("results") or [])[:5]
        formatted = []

        for item in results:
            tmdb_id = item.get("id")

            if tmdb_type == "tv":
                name = item.get("name") or ""
                year = (item.get("first_air_date") or "")[:4]
                prov = tv_watch_providers(tmdb_id)
            else:
                name = item.get("title") or ""
                year = (item.get("release_date") or "")[:4]
                prov = movie_watch_providers(tmdb_id)

            region_data = ((prov.get("results") or {}).get(region)) or {}
            offers = _pick_providers(region_data)

            formatted.append(
                {
                    "tmdb_id": tmdb_id,
                    "type": tmdb_type,
                    "name": name,
                    "year": year,
                    "poster_path": item.get("poster_path") or "",
                    "offers": offers,
                }
            )

        # Guardar historial (si DB está ok)
        try:
            SearchHistory.objects.create(
                query=q,
                type=tmdb_type,
                region=region,
                results_count=len(formatted),
            )
        except Exception:
            pass

        return Response({"query": q, "region": region, "results": formatted})


def title_detail(request, tmdb_type, tmdb_id):
    region = (request.GET.get("region") or os.getenv("TMDB_REGION", "CL")).strip().upper()

    if tmdb_type not in ["movie", "tv"]:
        raise Http404("Tipo no válido")

    if tmdb_type == "tv":
        detail = tv_details(tmdb_id)
        prov = tv_watch_providers(tmdb_id)
        vids = tv_videos(tmdb_id)

        name = detail.get("name", "")
        year = (detail.get("first_air_date") or "")[:4]
        overview = detail.get("overview", "")
        rating = detail.get("vote_average", 0)
        poster_path = detail.get("poster_path", "")
        genres = [g.get("name") for g in (detail.get("genres") or [])]
        extra = {
            "seasons": detail.get("number_of_seasons"),
            "episodes": detail.get("number_of_episodes"),
        }
    else:
        detail = movie_details(tmdb_id)
        prov = movie_watch_providers(tmdb_id)
        vids = movie_videos(tmdb_id)

        name = detail.get("title", "")
        year = (detail.get("release_date") or "")[:4]
        overview = detail.get("overview", "")
        rating = detail.get("vote_average", 0)
        poster_path = detail.get("poster_path", "")
        genres = [g.get("name") for g in (detail.get("genres") or [])]
        extra = {"runtime": detail.get("runtime")}

    region_data = ((prov.get("results") or {}).get(region)) or {}
    offers = _pick_providers(region_data)

    trailer = None
    for v in (vids.get("results") or []):
        if v.get("site") == "YouTube" and v.get("type") in ["Trailer", "Teaser"]:
            trailer = v.get("key")
            break

    ctx = {
        "tmdb_type": tmdb_type,
        "tmdb_id": tmdb_id,
        "region": region,
        "name": name,
        "year": year,
        "overview": overview,
        "rating": rating,
        "poster_path": poster_path,
        "genres": genres,
        "offers": offers,
        "trailer_key": trailer,
        "extra": extra,
    }
    return render(request, "guide/detail.html", ctx)