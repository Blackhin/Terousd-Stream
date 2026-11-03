import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock
import time

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from database import init_db
from services.omdb import get_movie_details, search_movies


# --------------------------------------------------
# Configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "FLASK_SECRET_KEY",
    "development-secret-key"
)


# --------------------------------------------------
# Movie collections
# --------------------------------------------------

FEATURED_MOVIE_IDS = [
    "tt1375666",   # Inception
    "tt0816692",   # Interstellar
    "tt4154796",   # Avengers: Endgame
    "tt7286456",   # Joker
    "tt0133093",   # The Matrix
    "tt1160419",   # Dune
]


HOME_MOVIE_IDS = [
    "tt1375666",   # Inception
    "tt0816692",   # Interstellar
    "tt4154796",   # Avengers: Endgame
    "tt7286456",   # Joker
    "tt0133093",   # The Matrix
    "tt1160419",   # Dune
    "tt0111161",   # The Shawshank Redemption
    "tt0068646",   # The Godfather
    "tt0468569",   # The Dark Knight
    "tt0109830",   # Forrest Gump
    "tt0133093",   # The Matrix
    "tt0080684",   # Star Wars: The Empire Strikes Back
    "tt0120737",   # The Lord of the Rings
    "tt0167260",   # The Lord of the Rings: Return of the King
    "tt0102926",   # The Silence of the Lambs
    "tt0137523",   # Fight Club
    "tt0120815",   # Saving Private Ryan
    "tt0110912",   # Pulp Fiction
    "tt0114369",   # Se7en
    "tt0816692",   # Interstellar
    "tt0103064",   # Terminator 2
    "tt0099685",   # Goodfellas
    "tt0245429",   # Spirited Away
    "tt4154796",   # Avengers: Endgame
]


# Remove accidental duplicate IMDb IDs while preserving order.
HOME_MOVIE_IDS = list(dict.fromkeys(HOME_MOVIE_IDS))


# --------------------------------------------------
# Simple in-memory cache
# --------------------------------------------------

CACHE_DURATION = 30 * 60  # 30 minutes

_cache = {
    "home": None,
    "home_timestamp": 0,
    "featured": None,
    "featured_timestamp": 0,
}

_cache_lock = Lock()


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def get_cached_movie(imdb_id):
    """
    Fetch movie details from OMDb.

    The result is cached for the current server session so that
    refreshing the homepage does not repeatedly hit the API.
    """

    cache_key = f"movie_{imdb_id}"

    with _cache_lock:
        cached = _cache.get(cache_key)

        if cached:
            return cached

    result = get_movie_details(imdb_id)

    if result.get("success"):
        movie = result.get("data")

        with _cache_lock:
            _cache[cache_key] = movie

        return movie

    return None


def fetch_movies_parallel(movie_ids):
    """
    Fetch several movies concurrently.

    This keeps the homepage considerably faster than making
    every OMDb request one after another.
    """

    movies = []

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(get_cached_movie, imdb_id): imdb_id
            for imdb_id in movie_ids
        }

        for future in as_completed(futures):
            imdb_id = futures[future]

            try:
                movie = future.result()

                if movie:
                    movies.append(movie)

            except Exception as error:
                print(
                    f"Failed to load movie {imdb_id}: {error}"
                )

    # Restore the original order.
    movie_map = {
        movie.get("imdbID"): movie
        for movie in movies
    }

    return [
        movie_map[imdb_id]
        for imdb_id in movie_ids
        if imdb_id in movie_map
    ]


def clean_movie(movie):
    """
    Return only the fields required by the frontend.
    """

    if not movie:
        return None

    return {
        "imdbID": movie.get("imdbID", ""),
        "Title": movie.get("Title", "Unknown"),
        "Year": movie.get("Year", "N/A"),
        "Rated": movie.get("Rated", "N/A"),
        "Released": movie.get("Released", "N/A"),
        "Runtime": movie.get("Runtime", "N/A"),
        "Genre": movie.get("Genre", "N/A"),
        "Director": movie.get("Director", "N/A"),
        "Actors": movie.get("Actors", "N/A"),
        "Plot": movie.get("Plot", "No description available."),
        "Poster": movie.get("Poster", "N/A"),
        "imdbRating": movie.get("imdbRating", "N/A"),
        "imdbVotes": movie.get("imdbVotes", "N/A"),
        "Metascore": movie.get("Metascore", "N/A"),
        "Runtime": movie.get("Runtime", "N/A"),
        "Language": movie.get("Language", "N/A"),
        "Country": movie.get("Country", "N/A"),
    }


# --------------------------------------------------
# Page
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# API health check
# --------------------------------------------------

@app.route("/api/test")
def api_test():
    return jsonify({
        "success": True,
        "message": "MovieHub API is running."
    })


# --------------------------------------------------
# Homepage API
# --------------------------------------------------

@app.route("/api/home")
def home_api():
    current_time = time.time()

    with _cache_lock:
        cached_home = _cache.get("home")
        cached_timestamp = _cache.get("home_timestamp", 0)

        if (
            cached_home
            and current_time - cached_timestamp < CACHE_DURATION
        ):
            return jsonify(cached_home)

    featured_movies = fetch_movies_parallel(
        FEATURED_MOVIE_IDS
    )

    poster_movies = fetch_movies_parallel(
        HOME_MOVIE_IDS
    )

    response = {
        "success": True,
        "featured": [
            clean_movie(movie)
            for movie in featured_movies
        ],
        "movies": [
            clean_movie(movie)
            for movie in poster_movies
        ],
    }

    with _cache_lock:
        _cache["home"] = response
        _cache["home_timestamp"] = current_time

    return jsonify(response)


# --------------------------------------------------
# Movie search
# --------------------------------------------------

@app.route("/api/movies")
def movies():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "success": False,
            "error": "Please enter a movie title."
        }), 400

    result = search_movies(query)

    if not result.get("success"):
        return jsonify(result), 404

    data = result.get("data", {})

    search_results = data.get("Search", [])

    return jsonify({
        "success": True,
        "movies": search_results
    })


# --------------------------------------------------
# Movie details
# --------------------------------------------------

@app.route("/api/movie/<imdb_id>")
def movie_details(imdb_id):
    imdb_id = imdb_id.strip()

    if not imdb_id:
        return jsonify({
            "success": False,
            "error": "IMDb ID is required."
        }), 400

    movie = get_cached_movie(imdb_id)

    if not movie:
        return jsonify({
            "success": False,
            "error": "Movie details could not be loaded."
        }), 404

    return jsonify({
        "success": True,
        "movie": clean_movie(movie)
    })


# --------------------------------------------------
# Featured endpoint
# --------------------------------------------------

@app.route("/api/featured")
def featured():
    current_time = time.time()

    with _cache_lock:
        cached_featured = _cache.get("featured")
        cached_timestamp = _cache.get(
            "featured_timestamp",
            0
        )

        if (
            cached_featured
            and current_time - cached_timestamp < CACHE_DURATION
        ):
            return jsonify(cached_featured)

    featured_movies = fetch_movies_parallel(
        FEATURED_MOVIE_IDS
    )

    response = {
        "success": True,
        "movies": [
            clean_movie(movie)
            for movie in featured_movies
        ]
    }

    with _cache_lock:
        _cache["featured"] = response
        _cache["featured_timestamp"] = current_time

    return jsonify(response)


# --------------------------------------------------
# Startup
# --------------------------------------------------

init_db()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )