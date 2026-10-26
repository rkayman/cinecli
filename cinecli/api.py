# cinecli/api.py

import time
import requests

BASE_URL = "https://movies-api.accel.li/api/v2"

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://yts.gg/",
    "Origin": "https://yts.gg",
}

_RETRY_STATUSES = {502, 503, 504, 521}


def _get(path: str, params: dict):
    url = f"{BASE_URL}/{path}"
    for attempt in range(3):
        response = requests.get(url, params=params, headers=_HEADERS, timeout=10)
        if response.status_code not in _RETRY_STATUSES:
            break
        if attempt < 2:
            time.sleep(0.5 * (attempt + 1))
    response.raise_for_status()
    return response.json()


def search_movies(query: str, limit: int = 10):
    data = _get("list_movies.json", {"query_term": query, "limit": limit})
    return data["data"].get("movies", [])


def get_movie_details(movie_id: int):
    data = _get("movie_details.json", {
        "movie_id": movie_id,
        "with_images": True,
        "with_cast": True,
    })
    return data["data"]["movie"]
