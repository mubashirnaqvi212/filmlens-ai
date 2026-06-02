from fastapi import FastAPI
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
    description="""
## FilmLens AI — Movie Recommendation API

- **Content-Based Filtering** — TF-IDF genre similarity
- **Collaborative Filtering** — SVD matrix factorization
- **Hybrid Model** — weighted blend of both

### Metrics
- SVD RMSE: **0.8727** (38.7% better than baseline)
- Precision@10: **74.5%**
- Recall@10: **50.9%**
    """,
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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
