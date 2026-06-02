# FilmLens AI 🎬

> AI-powered movie recommendation system using SVD collaborative filtering and TF-IDF content analysis.

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=flat-square&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=flat-square&logo=typescript)

## Live Demo

- **Frontend:** [filmlens-ai.vercel.app](https://filmlens-ai.vercel.app) *(coming soon)*
- **API Docs:** [filmlens-api.onrender.com/docs](https://filmlens-api.onrender.com/docs) *(coming soon)*

---

## What It Does

FilmLens AI recommends movies using three approaches:

| Method | How It Works |
|---|---|
| **Content-Based** | TF-IDF vectorization on genres + cosine similarity |
| **Collaborative** | SVD matrix factorization on 100K user ratings |
| **Hybrid** | Weighted blend of both (adjustable α parameter) |

Every recommendation comes with an explanation — *why* this movie was recommended.

---

## ML Performance

| Metric | Score |
|---|---|
| SVD RMSE | **0.8727** (38.7% better than baseline) |
| SVD MAE | 0.6713 |
| Precision@10 | **74.5%** |
| Recall@10 | 50.9% |

Dataset: [MovieLens ml-latest-small](https://grouplens.org/datasets/movielens/) — 9,742 movies, 100,836 ratings, 610 users.

---

## Tech Stack

**Backend**
- Python 3.14 + FastAPI
- scikit-surprise (SVD)
- scikit-learn (TF-IDF, cosine similarity)
- SQLAlchemy + SQLite
- Uvicorn

**Frontend**
- Next.js 15 + TypeScript
- Framer Motion (animations)
- Lucide React (icons)
- TMDB API (movie posters)

**ML Notebooks**
- Jupyter + pandas + matplotlib
- 4 notebooks: EDA → Content → Collaborative → Hybrid

---

## Project Structure
filmlens-ai/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── recommender/
│   │   └── engine.py        # ML inference engine
│   ├── routers/
│   │   ├── movies.py        # Movie endpoints
│   │   ├── recommendations.py
│   │   └── ratings.py
│   ├── models/schemas.py
│   └── database/database.py
├── frontend/
│   ├── app/
│   │   ├── page.tsx         # Home with carousels
│   │   ├── movies/          # Browse + detail pages
│   │   └── recommendations/ # Recommendation dashboard
│   ├── components/
│   │   ├── movies/          # MovieCard, Carousel, SearchBar
│   │   ├── recommendations/ # RecommendationCard
│   │   └── ui/              # Navbar, Footer, badges
│   └── lib/api.ts           # API client
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_content_based.ipynb
│   ├── 03_collaborative_filtering.ipynb
│   └── 04_hybrid_model.ipynb
└── data/                    # MovieLens dataset

---

## API Endpoints
GET  /movies/                    # Paginated movie list
GET  /movies/search?query=       # Search by title
GET  /movies/{id}                # Movie detail
GET  /recommend/content?title=   # Content-based recommendations
GET  /recommend/user/{id}        # Collaborative recommendations
GET  /recommend/hybrid/{id}      # Hybrid recommendations
GET  /recommend/metrics          # Model evaluation metrics
POST /rate                       # Submit rating
POST /feedback                   # Thumbs up/down feedback

---

## Running Locally

**Backend**
```bash
# Install dependencies
pip install fastapi uvicorn pandas scikit-learn scikit-surprise sqlalchemy python-dotenv

# Set environment variables
cp .env.example .env

# Start API
python -m uvicorn backend.main:app --reload
# API available at http://localhost:8000/docs
```

**Frontend**
```bash
cd frontend
npm install
cp .env.local.example .env.local  # Add your TMDB API key
npm run dev
# App available at http://localhost:3000
```

---

## Key Design Decisions

- **Why SVD?** Matrix sparsity was 98.3% — SVD handles sparse data better than KNN
- **Why hybrid?** Pure content-based ignores user taste; pure collaborative has cold-start problem
- **Why α=0.5 default?** Empirically balanced — adjustable per user preference
- **Why FastAPI?** Automatic OpenAPI docs, async support, Pydantic validation

---

## Author

Built by [Mubashir Naqvi](https://github.com/mubashirnaqvi212) as a portfolio project.
