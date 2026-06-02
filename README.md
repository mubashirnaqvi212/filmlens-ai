# FilmLens AI 🎬

> Full-stack AI movie recommendation system — SVD collaborative filtering + TF-IDF content analysis, served via FastAPI, visualized in a Netflix-style Next.js UI.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=flat-square&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=flat-square&logo=typescript)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-orange?style=flat-square&logo=scikitlearn)
![Deployed](https://img.shields.io/badge/Deployed-Railway%20%2B%20Vercel-brightgreen?style=flat-square)

## 🔗 Live Demo

| | Link |
|---|---|
| **Frontend** | [filmlens-ai-blue.vercel.app](https://filmlens-ai-blue.vercel.app) |
| **API Docs** | [filmlens-api-production.up.railway.app/docs](https://filmlens-api-production.up.railway.app/docs) |

---

## 🧠 What Makes This Interesting

Most recommendation tutorials stop at a Jupyter notebook. This project goes end-to-end:

- **Real ML pipeline** — EDA → feature engineering → model training → evaluation → serving
- **Three recommendation strategies** with a live alpha-blending slider
- **Every recommendation is explained** — users see *why* a movie was recommended
- **Thumbs up/down feedback loop** — ratings sent back to the FastAPI backend
- **Deployed and publicly accessible** — not just a local demo

---

## 📊 ML Performance

| Metric | Score | vs Baseline |
|---|---|---|
| SVD RMSE | **0.8727** | **38.7% better** |
| SVD MAE | 0.6713 | 40.9% better |
| Precision@10 | **74.5%** | — |
| Recall@10 | 50.9% | — |

Dataset: [MovieLens ml-latest-small](https://grouplens.org/datasets/movielens/) — 9,742 movies, 100,836 ratings, 610 users, 98.3% matrix sparsity.

---

## 🤖 Recommendation Approaches

| Method | Technique | Strength |
|---|---|---|
| **Content-Based** | TF-IDF on genres + cosine similarity | Works for new users |
| **Collaborative** | SVD matrix factorization | Captures user taste |
| **Hybrid** | Weighted blend (adjustable α) | Best of both worlds |

---

## 🏗️ Project Structure
filmlens-ai/
├── backend/
│   ├── main.py                      # FastAPI app entry point
│   ├── recommender/
│   │   └── engine.py                # ML inference engine
│   ├── routers/
│   │   ├── movies.py                # Movie endpoints
│   │   ├── recommendations.py       # Recommendation endpoints
│   │   └── ratings.py               # Rating & feedback endpoints
│   ├── models/schemas.py            # Pydantic schemas
│   └── database/database.py         # SQLAlchemy setup
├── frontend/
│   ├── app/
│   │   ├── page.tsx                 # Home — hero + carousels
│   │   ├── movies/                  # Browse + movie detail
│   │   └── recommendations/         # Recommendation dashboard
│   ├── components/
│   │   ├── movies/                  # MovieCard, Carousel, SearchBar
│   │   ├── recommendations/         # RecommendationCard with feedback
│   │   └── ui/                      # Navbar, Footer, badges
│   └── lib/api.ts                   # Typed API client
├── notebooks/
│   ├── 01_eda.ipynb                 # Exploratory data analysis
│   ├── 02_content_based.ipynb       # TF-IDF + cosine similarity
│   ├── 03_collaborative_filtering.ipynb  # SVD with cross-validation
│   └── 04_hybrid_model.ipynb        # Alpha-blended hybrid
└── data/                            # MovieLens dataset + charts

---

## 🔌 API Endpoints
GET  /movies/                     Paginated movie list with genre filter
GET  /movies/search?query=        Live title search
GET  /movies/{id}                 Movie detail with average rating
GET  /recommend/content?title=    Content-based recommendations
GET  /recommend/user/{id}         Collaborative SVD recommendations
GET  /recommend/hybrid/{id}       Hybrid recommendations with alpha param
GET  /recommend/metrics           Model evaluation metrics
POST /rate                        Submit a movie rating
POST /feedback                    Thumbs up/down on a recommendation

---

## ⚙️ Tech Stack

**ML & Backend**
- Python 3.11, FastAPI, Uvicorn
- scikit-surprise (SVD matrix factorization)
- scikit-learn (TF-IDF, cosine similarity)
- pandas, numpy
- SQLAlchemy + SQLite
- Deployed on Railway

**Frontend**
- Next.js 15, TypeScript
- Framer Motion (animations)
- Lucide React (icons)
- TMDB API (real movie posters)
- Deployed on Vercel

---

## 🏃 Running Locally

**Backend**
```bash
pip install fastapi uvicorn pandas scikit-learn scikit-surprise sqlalchemy python-dotenv

cp .env.example .env
# Edit .env with your values

python -m uvicorn backend.main:app --reload
# API docs at http://localhost:8000/docs
```

**Frontend**
```bash
cd frontend
npm install

# Create frontend/.env.local and add:
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_TMDB_API_KEY=your_key
# NEXT_PUBLIC_TMDB_IMAGE_BASE=https://image.tmdb.org/t/p/w500

npm run dev
# App at http://localhost:3000
```

---

## 💡 Key Design Decisions

**Why SVD over KNN?**
Matrix sparsity was 98.3% — KNN breaks down at this density. SVD factorizes the sparse matrix into latent factors, achieving 38.7% RMSE improvement over the global mean baseline.

**Why hybrid recommendations?**
Pure content-based filtering ignores user taste history. Pure collaborative filtering fails for new users (cold-start). The hybrid blends both with an adjustable α parameter — exposed as a live slider in the UI.

**Why FastAPI over Django/Flask?**
Automatic OpenAPI documentation, async support, and Pydantic validation out of the box. The `/docs` endpoint makes the API immediately explorable without any extra tooling.

---

## 👤 Author

Built by [Mubashir Naqvi](https://github.com/mubashirnaqvi212) as a portfolio project demonstrating end-to-end ML system design.
