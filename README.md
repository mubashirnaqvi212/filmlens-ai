# FilmLens AI

A full-stack movie recommendation system built with FastAPI and Next.js, using SVD collaborative filtering and TF-IDF content-based filtering. Trained on the MovieLens dataset (100K ratings), served via a REST API, and deployed on Railway + Vercel.

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=flat-square&logo=typescript)](https://typescriptlang.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

**Live demo:** [filmlens-ai-blue.vercel.app](https://filmlens-ai-blue.vercel.app) — **API docs:** [filmlens-api-production.up.railway.app/docs](https://filmlens-api-production.up.railway.app/docs)

---
## Website 

<img width="1900" height="874" alt="Recording 2026-06-03 034426 (1)" src="https://github.com/user-attachments/assets/6eb199e0-d7dd-4900-89a2-b948166dfdb2" />
<img width="1920" height="872" alt="2" src="https://github.com/user-attachments/assets/4f29d05c-6b71-4bb4-9a9c-cbaa185ac8f1" />
<img width="1894" height="872" alt="3" src="https://github.com/user-attachments/assets/3107b9b7-400c-4ccf-a6f2-8d9050b25454" />



---
## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [ML Pipeline](#ml-pipeline)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Design Decisions](#design-decisions)

---

## Overview

FilmLens AI implements three recommendation strategies:

| Strategy | Method | Use Case |
|---|---|---|
| Content-Based | TF-IDF on genres + cosine similarity | Cold-start users |
| Collaborative | SVD matrix factorization | Users with rating history |
| Hybrid | Weighted blend with adjustable alpha | Best overall accuracy |

Every recommendation includes an explanation of why it was suggested. Users can submit thumbs-up/down feedback which is persisted to the backend.

---

## Architecture

```
Browser (Next.js)  -->  FastAPI (Railway)  -->  SQLite
                              |
                         ML Engine
                        /     |     \
                   TF-IDF    SVD   Hybrid
                              |
                         MovieLens CSV
```

The ML engine loads on startup, reads directly from the MovieLens CSV files, trains SVD in-memory, and serves recommendations via REST endpoints. No external ML infrastructure required.

---

## ML Pipeline

The notebooks in `notebooks/` document the full research process:

**01 — Exploratory Data Analysis**
- 9,742 movies, 100,836 ratings, 610 users
- Matrix sparsity: 98.3% (motivates SVD over KNN)
- Rating distribution: positive skew, mode at 4.0

**02 — Content-Based Filtering**
- TF-IDF vectorization on cleaned genre strings
- Cosine similarity computed on-demand (avoids storing 9742x9742 matrix)
- Handles Sci-Fi/Film-Noir normalization

**03 — Collaborative Filtering**
- SVD via scikit-surprise (n_factors=50, n_epochs=10)
- 5-fold cross-validation
- RMSE: 0.8727 vs baseline 1.4243 (38.7% improvement)
- Precision@10: 74.5%, Recall@10: 50.9%

**04 — Hybrid Model**
- Score: alpha * content_score + (1 - alpha) * collaborative_score
- Default alpha=0.5, adjustable per request
- Exposed as a live slider in the frontend

---

## API Reference

```
GET    /                              Health check
GET    /health                        ML engine status

GET    /movies/                       List movies (paginated, genre filter)
GET    /movies/search?query=          Search movies by title
GET    /movies/{movie_id}             Movie detail with average rating

GET    /recommend/content?title=      Content-based recommendations
GET    /recommend/user/{user_id}      Collaborative SVD recommendations
GET    /recommend/hybrid/{user_id}    Hybrid recommendations (alpha param)
GET    /recommend/metrics             Model evaluation metrics

POST   /rate                          Submit a rating (0.5-5.0)
GET    /user/{user_id}/ratings        User rating history
POST   /feedback                      Thumbs up/down on a recommendation
```

Full interactive documentation available at `/docs` (Swagger UI) and `/redoc`.

---

## Project Structure

```
filmlens-ai/
|
+-- backend/
|   +-- main.py                       FastAPI application, CORS, startup
|   +-- recommender/
|   |   +-- engine.py                 ML engine (TF-IDF, SVD, hybrid)
|   |   +-- hybrid_config.json        Default alpha configuration
|   +-- routers/
|   |   +-- movies.py                 Movie listing and search endpoints
|   |   +-- recommendations.py        Recommendation endpoints
|   |   +-- ratings.py                Rating and feedback endpoints
|   +-- models/
|   |   +-- schemas.py                Pydantic request/response schemas
|   +-- database/
|       +-- database.py               SQLAlchemy engine and session
|
+-- frontend/
|   +-- app/
|   |   +-- page.tsx                  Home page with hero and carousels
|   |   +-- movies/
|   |   |   +-- page.tsx              Movie browser with genre filters
|   |   |   +-- [id]/page.tsx         Movie detail with similar movies
|   |   +-- recommendations/
|   |       +-- page.tsx              Recommendation dashboard
|   +-- components/
|   |   +-- movies/
|   |   |   +-- MovieCard.tsx         Poster card with TMDB images
|   |   |   +-- MovieCarousel.tsx     Horizontal scrollable row
|   |   |   +-- SearchBar.tsx         Live search with dropdown
|   |   +-- recommendations/
|   |   |   +-- RecommendationCard.tsx  Match score, explanation, feedback
|   |   +-- ui/
|   |       +-- Navbar.tsx            Fixed navigation bar
|   |       +-- Footer.tsx            Tech stack and links
|   |       +-- GenreBadge.tsx        Color-coded genre tags
|   |       +-- LoadingSpinner.tsx    Loading state component
|   +-- lib/
|   |   +-- api.ts                    Typed Axios API client
|   |   +-- utils.ts                  Helper functions
|   +-- types/
|       +-- index.ts                  TypeScript interfaces
|
+-- notebooks/
|   +-- 01_eda.ipynb                  Exploratory data analysis
|   +-- 02_content_based.ipynb        TF-IDF and cosine similarity
|   +-- 03_collaborative_filtering.ipynb  SVD with cross-validation
|   +-- 04_hybrid_model.ipynb         Alpha-blended hybrid model
|
+-- data/
|   +-- movies.csv                    MovieLens movie metadata
|   +-- ratings.csv                   100K user ratings
|   +-- links.csv                     TMDB and IMDB ID mappings
|
+-- requirements.txt
+-- runtime.txt
+-- render.yaml
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- TMDB API key (free at [themoviedb.org](https://www.themoviedb.org/settings/api))

### Backend

```bash
# Clone the repository
git clone https://github.com/mubashirnaqvi212/filmlens-ai.git
cd filmlens-ai

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set your values

# Start the API server
python -m uvicorn backend.main:app --reload

# API available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
# Create frontend/.env.local with:
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_TMDB_API_KEY=your_tmdb_api_key
NEXT_PUBLIC_TMDB_IMAGE_BASE=https://image.tmdb.org/t/p/w500

# Start development server
npm run dev

# App available at http://localhost:3000
```

---

## Deployment

| Service | Platform | Configuration |
|---|---|---|
| Backend API | Railway | `render.yaml`, Python 3.11, auto-deploy from main |
| Frontend | Vercel | Root directory: `frontend`, auto-deploy from main |

Environment variables required on each platform are documented in `.env.example` (backend) and the frontend README.

---

## Design Decisions

**SVD over KNN for collaborative filtering**
With 98.3% matrix sparsity, KNN-based approaches struggle to find meaningful neighbors. SVD decomposes the sparse user-item matrix into latent factors, achieving 38.7% RMSE improvement over the global mean baseline.

**On-demand cosine similarity instead of precomputed matrix**
The full 9,742 x 9,742 cosine similarity matrix requires ~724MB of RAM. On Railway's free tier (512MB), this causes OOM crashes. Computing similarity on-demand per request uses negligible memory with acceptable latency.

**Hybrid alpha as a request parameter**
Rather than hardcoding the content/collaborative blend ratio, alpha is exposed as a query parameter and a live UI slider. This lets users and developers explore the tradeoff interactively.

**SQLite for persistence**
For a portfolio project with low write volume (ratings, feedback), SQLite is sufficient and eliminates infrastructure complexity. The schema is compatible with PostgreSQL via SQLAlchemy if scaling is needed.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Author

<p align="left">
  <img src="https://cdn-icons-png.flaticon.com/512/1077/1077012.png" width="18"/>
  <b> Mubashir Naqvi</b>
</p>

<p align="left">
  <a href="https://github.com/mubashirnaqvi212">
    <img src="https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white" />
  </a>
</p>
