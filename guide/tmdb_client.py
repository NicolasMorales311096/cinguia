import os
import requests

TMDB_BASE = "https://api.themoviedb.org/3"


def _headers():
    token = os.getenv("TMDB_READ_TOKEN", "")
    return {"Authorization": f"Bearer {token}"}


def search_movie(query, region="CL"):
    r = requests.get(
        f"{TMDB_BASE}/search/movie",
        headers=_headers(),
        params={"query": query, "region": region, "include_adult": "false"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def search_tv(query):
    r = requests.get(
        f"{TMDB_BASE}/search/tv",
        headers=_headers(),
        params={"query": query, "include_adult": "false"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def movie_watch_providers(movie_id):
    r = requests.get(
        f"{TMDB_BASE}/movie/{movie_id}/watch/providers",
        headers=_headers(),
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def tv_watch_providers(tv_id):
    r = requests.get(
        f"{TMDB_BASE}/tv/{tv_id}/watch/providers",
        headers=_headers(),
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


# ✅ Detalles (para la página de detalle)
def movie_details(movie_id):
    r = requests.get(
        f"{TMDB_BASE}/movie/{movie_id}",
        headers=_headers(),
        params={"language": "es-ES"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def tv_details(tv_id):
    r = requests.get(
        f"{TMDB_BASE}/tv/{tv_id}",
        headers=_headers(),
        params={"language": "es-ES"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


# ✅ Videos (trailer)
def movie_videos(movie_id):
    r = requests.get(
        f"{TMDB_BASE}/movie/{movie_id}/videos",
        headers=_headers(),
        params={"language": "es-ES"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def tv_videos(tv_id):
    r = requests.get(
        f"{TMDB_BASE}/tv/{tv_id}/videos",
        headers=_headers(),
        params={"language": "es-ES"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()