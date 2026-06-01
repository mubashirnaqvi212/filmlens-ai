from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database.database import get_db, Rating, Feedback
from backend.models.schemas import RatingCreate, RatingResponse, FeedbackCreate, FeedbackResponse
from backend.recommender.engine import engine as ml_engine
from datetime import datetime

router = APIRouter(tags=["Ratings & Feedback"])


@router.post("/rate", response_model=RatingResponse, summary="Submit a movie rating")
def rate_movie(payload: RatingCreate, db: Session = Depends(get_db)):
    movie = ml_engine.movies[ml_engine.movies['movieId'] == payload.movie_id]
    if movie.empty:
        raise HTTPException(status_code=404, detail=f"Movie {payload.movie_id} not found")
    existing = db.query(Rating).filter(
        Rating.user_id == payload.user_id,
        Rating.movie_id == payload.movie_id
    ).first()
    if existing:
        existing.rating = payload.rating
        existing.timestamp = datetime.utcnow()
        db.commit()
        message = "Rating updated"
    else:
        db.add(Rating(user_id=payload.user_id, movie_id=payload.movie_id, rating=payload.rating))
        db.commit()
        message = "Rating saved"
    return RatingResponse(user_id=payload.user_id, movie_id=payload.movie_id, rating=payload.rating, message=message)


@router.get("/user/{user_id}/ratings", summary="Get all ratings by a user")
def get_user_ratings(user_id: int, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
    results = []
    for r in ratings:
        movie = ml_engine.movies[ml_engine.movies['movieId'] == r.movie_id]
        title = movie.iloc[0]['title_clean'] if not movie.empty else "Unknown"
        results.append({'movie_id': r.movie_id, 'title': title, 'rating': r.rating, 'timestamp': r.timestamp})
    return {'user_id': user_id, 'total_ratings': len(results), 'ratings': results}


@router.post("/feedback", response_model=FeedbackResponse, summary="Submit recommendation feedback")
def submit_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    if payload.signal not in ['thumbs_up', 'thumbs_down']:
        raise HTTPException(status_code=400, detail="Signal must be 'thumbs_up' or 'thumbs_down'")
    if payload.recommendation_type not in ['content', 'collaborative', 'hybrid']:
        raise HTTPException(status_code=400, detail="recommendation_type must be content, collaborative, or hybrid")
    db.add(Feedback(
        user_id=payload.user_id, movie_id=payload.movie_id,
        recommendation_type=payload.recommendation_type, signal=payload.signal
    ))
    db.commit()
    return FeedbackResponse(message="Feedback recorded", user_id=payload.user_id, movie_id=payload.movie_id, signal=payload.signal)
