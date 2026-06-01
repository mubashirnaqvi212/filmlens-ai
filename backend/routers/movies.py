from fastapi import APIRouter, HTTPException, Query
from backend.recommender.engine import engine as ml_engine
from typing import Optional
import pandas as pd

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", summary="Get paginated movie list")
def get_movies(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    genre: Optional[str] = None
):
    movies = ml_engine.movies.copy()
    if genre:
        movies = movies[movies['genres'].str.contains(genre, case=False)]
    total = len(movies)
    start = (page - 1) * limit
    end = start + limit
    page_movies = movies.iloc[start:end]
    results = []
    for _, row in page_movies.iterrows():
        results.append({
            'movie_id': int(row['movieId']),
            'title': row['title_clean'],
            'year': int(row['year']) if not pd.isna(row['year']) else None,
            'genres': row['genres']
        })
    return {'total': total, 'page': page, 'limit': limit, 'results': results}


@router.get("/search", summary="Search movies by title")
def search_movies(
    query: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50)
):
    matches = ml_engine.movies[
        ml_engine.movies['title_clean'].str.contains(query, case=False, na=False)
    ].head(limit)
    results = []
    for _, row in matches.iterrows():
        results.append({
            'movie_id': int(row['movieId']),
            'title': row['title_clean'],
            'year': int(row['year']) if not pd.isna(row['year']) else None,
            'genres': row['genres']
        })
    return {'query': query, 'total': len(results), 'results': results}


@router.get("/{movie_id}", summary="Get movie detail by ID")
def get_movie(movie_id: int):
    movie = ml_engine.movies[ml_engine.movies['movieId'] == movie_id]
    if movie.empty:
        raise HTTPException(status_code=404, detail=f"Movie {movie_id} not found")
    row = movie.iloc[0]
    movie_ratings = ml_engine.ratings[ml_engine.ratings['movieId'] == movie_id]
    avg_rating = float(movie_ratings['rating'].mean()) if not movie_ratings.empty else None
    return {
        'movie_id': int(row['movieId']),
        'title': row['title_clean'],
        'year': int(row['year']) if not pd.isna(row['year']) else None,
        'genres': row['genres'],
        'average_rating': round(avg_rating, 2) if avg_rating else None,
        'rating_count': int(len(movie_ratings))
    }
