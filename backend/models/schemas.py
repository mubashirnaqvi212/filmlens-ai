from pydantic import BaseModel, Field
from typing import Optional


class MovieBase(BaseModel):
    movie_id: int
    title: str
    year: Optional[int]
    genres: str


class MovieDetail(MovieBase):
    tmdb_id: Optional[int] = None
    poster_url: Optional[str] = None
    average_rating: Optional[float] = None
    rating_count: Optional[int] = None


class RecommendationItem(BaseModel):
    movie_id: int
    title: str
    year: Optional[int]
    genres: str
    match_pct: str
    explanation: str
    predicted_rating: Optional[float] = None
    hybrid_score: Optional[float] = None


class ContentRecommendationResponse(BaseModel):
    seed_movie: str
    method: str = "content_based"
    recommendations: list[RecommendationItem]


class CollaborativeRecommendationResponse(BaseModel):
    user_id: int
    rated_count: int
    method: str = "collaborative_svd"
    recommendations: list[RecommendationItem]


class HybridRecommendationResponse(BaseModel):
    user_id: int
    seed_movie: str
    alpha: float
    method: str = "hybrid"
    recommendations: list[RecommendationItem]


class RatingCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: float = Field(..., ge=0.5, le=5.0)


class RatingResponse(BaseModel):
    user_id: int
    movie_id: int
    rating: float
    message: str


class FeedbackCreate(BaseModel):
    user_id: int
    movie_id: int
    recommendation_type: str
    signal: str


class FeedbackResponse(BaseModel):
    message: str
    user_id: int
    movie_id: int
    signal: str


class ModelMetrics(BaseModel):
    svd_rmse: float
    svd_mae: float
    precision_at_10: float
    recall_at_10: float
    baseline_rmse: float
    improvement_pct: float
