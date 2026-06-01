from fastapi import APIRouter, HTTPException, Query
from backend.recommender.engine import engine as ml_engine

router = APIRouter(prefix="/recommend", tags=["Recommendations"])


@router.get("/content/{movie_id}", summary="Content-based recommendations by movie ID")
def content_by_id(movie_id: int, n: int = Query(10, ge=1, le=50)):
    movie = ml_engine.movies[ml_engine.movies['movieId'] == movie_id]
    if movie.empty:
        raise HTTPException(status_code=404, detail=f"Movie {movie_id} not found")
    title = movie.iloc[0]['title_clean']
    result = ml_engine.content_recommendations(title=title, n=n)
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    return result


@router.get("/content", summary="Content-based recommendations by title")
def content_by_title(title: str = Query(..., min_length=1), n: int = Query(10, ge=1, le=50)):
    result = ml_engine.content_recommendations(title=title, n=n)
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    return result


@router.get("/user/{user_id}", summary="Collaborative recommendations for a user")
def collaborative(user_id: int, n: int = Query(10, ge=1, le=50)):
    valid_users = ml_engine.ratings['userId'].unique()
    if user_id not in valid_users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found. Valid range: 1-610")
    return ml_engine.collaborative_recommendations(user_id=user_id, n=n)


@router.get("/hybrid/{user_id}", summary="Hybrid recommendations for a user")
def hybrid(
    user_id: int,
    title: str = Query(..., min_length=1),
    n: int = Query(10, ge=1, le=50),
    alpha: float = Query(0.5, ge=0.0, le=1.0)
):
    valid_users = ml_engine.ratings['userId'].unique()
    if user_id not in valid_users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found. Valid range: 1-610")
    result = ml_engine.hybrid_recommendations(user_id=user_id, title=title, n=n, alpha=alpha)
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    return result


@router.get("/metrics", summary="Model evaluation metrics")
def get_metrics():
    return ml_engine.get_metrics()
