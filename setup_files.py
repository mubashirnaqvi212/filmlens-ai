import pathlib

files = {}

files['backend/database/database.py'] = """from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./filmlens.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Rating(Base):
    __tablename__ = "ratings"
    id        = Column(Integer, primary_key=True, index=True)
    user_id   = Column(Integer, index=True, nullable=False)
    movie_id  = Column(Integer, index=True, nullable=False)
    rating    = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedback"
    id                  = Column(Integer, primary_key=True, index=True)
    user_id             = Column(Integer, index=True, nullable=False)
    movie_id            = Column(Integer, index=True, nullable=False)
    recommendation_type = Column(String, nullable=False)
    signal              = Column(String, nullable=False)
    timestamp           = Column(DateTime, default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables ready")
"""

files['backend/models/schemas.py'] = """from pydantic import BaseModel, Field
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
"""

files['backend/routers/movies.py'] = """from fastapi import APIRouter, HTTPException, Query
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
"""

files['backend/routers/recommendations.py'] = """from fastapi import APIRouter, HTTPException, Query
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
"""

files['backend/routers/ratings.py'] = """from fastapi import APIRouter, HTTPException, Depends
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
"""

files['backend/main.py'] = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from backend.database.database import init_db
from backend.recommender.engine import engine as ml_engine
from backend.routers import movies, recommendations, ratings

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 FilmLens AI starting up...")
    init_db()
    ml_engine.load()
    print("✅ FilmLens AI ready")
    yield
    print("👋 FilmLens AI shutting down")


app = FastAPI(
    title="FilmLens AI",
    description=\"\"\"
## FilmLens AI — Movie Recommendation API

- **Content-Based Filtering** — TF-IDF genre similarity
- **Collaborative Filtering** — SVD matrix factorization
- **Hybrid Model** — weighted blend of both

### Metrics
- SVD RMSE: **0.8727** (38.7% better than baseline)
- Precision@10: **74.5%**
- Recall@10: **50.9%**
    \"\"\",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://filmlens-ai.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies.router)
app.include_router(recommendations.router)
app.include_router(ratings.router)


@app.get("/", tags=["Health"])
def root():
    return {"name": "FilmLens AI", "version": "1.0.0", "status": "running", "docs": "/docs"}


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "ml_engine_loaded": ml_engine._loaded,
        "movies_indexed": int(ml_engine.movies.shape[0]) if ml_engine._loaded else 0
    }
"""
files['backend/recommender/engine.py'] = """import pickle
import json
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', '..', 'data')
ARTIFACTS_DIR = BASE_DIR


class RecommendationEngine:
    def __init__(self):
        self.movies = None
        self.ratings = None
        self.cosine_sim = None
        self.movie_index = None
        self.tfidf = None
        self.svd_model = None
        self.config = None
        self._loaded = False

    def load(self):
        if self._loaded:
            return
        print("🔄 Loading ML artifacts...")
        self.movies = pd.read_csv(os.path.join(DATA_DIR, 'movies.csv'))
        self.ratings = pd.read_csv(os.path.join(DATA_DIR, 'ratings.csv'))
        self.movies['title_clean'] = self.movies['title'].str.replace(
            r'\\s*\\(\\d{4}\\)', '', regex=True).str.strip()
        self.movies['year'] = self.movies['title'].str.extract(
            r'\\((\\d{4})\\)').astype(float)
        self.movies['genres_clean'] = self.movies['genres'].str.replace(
            'Sci-Fi', 'SciFi', regex=False)
        self.movies['genres_clean'] = self.movies['genres_clean'].str.replace(
            'Film-Noir', 'FilmNoir', regex=False)
        self.movies['genres_clean'] = self.movies['genres_clean'].str.replace(
            '|', ' ', regex=False)
        print("🔄 Building TF-IDF matrix...")
        self.tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = self.tfidf.fit_transform(self.movies['genres_clean'])
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        self.movie_index = pd.Series(
            self.movies.index, index=self.movies['title_clean'])
        print("🔄 Loading SVD model...")
        collab_path = os.path.join(ARTIFACTS_DIR, 'collaborative_artifacts.pkl')
        with open(collab_path, 'rb') as f:
            collab = pickle.load(f)
        self.svd_model = collab['model']
        config_path = os.path.join(ARTIFACTS_DIR, 'hybrid_config.json')
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self._loaded = True
        print("✅ ML engine ready")

    def content_recommendations(self, title: str, n: int = 10) -> dict:
        matches = [t for t in self.movie_index.index if title.lower() in t.lower()]
        if not matches:
            return {'error': f"Movie '{title}' not found"}
        matched_title = matches[0]
        idx = self.movie_index[matched_title]
        if isinstance(idx, pd.Series):
            idx = idx.iloc[0]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n + 1]
        source_genres = set(self.movies.iloc[idx]['genres'].split('|'))
        results = []
        for i, score in sim_scores:
            row = self.movies.iloc[i]
            rec_genres = set(row['genres'].split('|'))
            shared = source_genres & rec_genres
            results.append({
                'movie_id': int(row['movieId']),
                'title': row['title_clean'],
                'year': int(row['year']) if not pd.isna(row['year']) else None,
                'genres': row['genres'],
                'similarity_score': round(float(score), 4),
                'match_pct': f"{score * 100:.1f}%",
                'explanation': f"Shares {len(shared)} genre(s) with {matched_title}: {', '.join(shared)}"
            })
        return {'seed_movie': matched_title, 'method': 'content_based', 'recommendations': results}

    def collaborative_recommendations(self, user_id: int, n: int = 10) -> dict:
        rated_ids = set(self.ratings[self.ratings['userId'] == user_id]['movieId'].tolist())
        all_ids = set(self.movies['movieId'].tolist())
        unrated = all_ids - rated_ids
        preds = [(mid, self.svd_model.predict(user_id, mid).est) for mid in unrated]
        preds.sort(key=lambda x: x[1], reverse=True)
        results = []
        for movie_id, predicted_rating in preds[:n]:
            row = self.movies[self.movies['movieId'] == movie_id].iloc[0]
            results.append({
                'movie_id': int(movie_id),
                'title': row['title_clean'],
                'year': int(row['year']) if not pd.isna(row['year']) else None,
                'genres': row['genres'],
                'predicted_rating': round(float(predicted_rating), 2),
                'match_pct': f"{(predicted_rating / 5.0) * 100:.1f}%",
                'explanation': f"Predicted {predicted_rating:.1f}★ based on your rating history"
            })
        return {'user_id': user_id, 'rated_count': len(rated_ids), 'method': 'collaborative_svd', 'recommendations': results}

    def hybrid_recommendations(self, user_id: int, title: str, n: int = 10, alpha: float = 0.5) -> dict:
        matches = [t for t in self.movie_index.index if title.lower() in t.lower()]
        if not matches:
            return {'error': f"Movie '{title}' not found"}
        matched_title = matches[0]
        idx = self.movie_index[matched_title]
        if isinstance(idx, pd.Series):
            idx = idx.iloc[0]
        sim_scores_dict = {i: score for i, score in enumerate(self.cosine_sim[idx])}
        rated_ids = set(self.ratings[self.ratings['userId'] == user_id]['movieId'].tolist())
        source_genres = set(self.movies.iloc[idx]['genres'].split('|'))
        results = []
        for i, row in self.movies.iterrows():
            movie_id = row['movieId']
            if movie_id in rated_ids:
                continue
            content_score = sim_scores_dict.get(i, 0)
            collab_pred = self.svd_model.predict(user_id, movie_id).est
            collab_score = (min(max(collab_pred, 0.5), 5.0) - 0.5) / 4.5
            hybrid_score = (alpha * content_score) + ((1 - alpha) * collab_score)
            rec_genres = set(row['genres'].split('|'))
            shared = source_genres & rec_genres
            explanation = (f"Shares genre(s) with {matched_title}: {', '.join(shared)}"
                          if shared else f"Predicted {collab_pred:.1f}★ based on your rating history")
            results.append({
                'movie_id': int(movie_id),
                'title': row['title_clean'],
                'year': int(row['year']) if not pd.isna(row['year']) else None,
                'genres': row['genres'],
                'content_score': round(float(content_score), 4),
                'collab_score': round(float(collab_score), 4),
                'hybrid_score': round(float(hybrid_score), 4),
                'predicted_rating': round(float(collab_pred), 2),
                'match_pct': f"{hybrid_score * 100:.1f}%",
                'explanation': explanation
            })
        results.sort(key=lambda x: x['hybrid_score'], reverse=True)
        return {'user_id': user_id, 'seed_movie': matched_title, 'alpha': alpha, 'method': 'hybrid', 'recommendations': results[:n]}

    def get_metrics(self) -> dict:
        return self.config['metrics']


engine = RecommendationEngine()
"""
# Write all files
for path, content in files.items():
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')
    print(f"✅ Written: {path}")

print("\n🎉 All files written successfully")