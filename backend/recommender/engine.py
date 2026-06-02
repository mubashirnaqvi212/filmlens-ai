import json
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import SVD, Dataset, Reader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', '..', 'data')

class RecommendationEngine:
    def __init__(self):
        self.movies = None
        self.ratings = None
        self.tfidf_matrix = None
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
            r'\s*\(\d{4}\)', '', regex=True).str.strip()
        self.movies['year'] = self.movies['title'].str.extract(
            r'\((\d{4})\)').astype(float)
        self.movies['genres_clean'] = self.movies['genres'].str.replace(
            'Sci-Fi', 'SciFi', regex=False)
        self.movies['genres_clean'] = self.movies['genres_clean'].str.replace(
            'Film-Noir', 'FilmNoir', regex=False)
        self.movies['genres_clean'] = self.movies['genres_clean'].str.replace(
            '|', ' ', regex=False)

        print("🔄 Building TF-IDF matrix...")
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies['genres_clean'])
        self.movie_index = pd.Series(
            self.movies.index, index=self.movies['title_clean'])

        print("🔄 Training SVD model...")
        reader = Reader(rating_scale=(0.5, 5.0))
        data = Dataset.load_from_df(
            self.ratings[['userId', 'movieId', 'rating']], reader)
        trainset = data.build_full_trainset()
        self.svd_model = SVD(n_factors=50, n_epochs=10, verbose=False)
        self.svd_model.fit(trainset)

        config_path = os.path.join(BASE_DIR, 'hybrid_config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {'alpha': 0.5}

        self._loaded = True
        print("✅ ML engine ready")

    def _get_content_scores(self, idx, n=20):
        movie_vec = self.tfidf_matrix[idx]
        scores = cosine_similarity(movie_vec, self.tfidf_matrix).flatten()
        scores[idx] = 0
        top_indices = np.argsort(scores)[::-1][:n]
        return [(i, scores[i]) for i in top_indices]

    def content_recommendations(self, title: str, n: int = 10) -> dict:
        matches = [t for t in self.movie_index.index if title.lower() in t.lower()]
        if not matches:
            return {'error': f"Movie '{title}' not found"}
        matched_title = matches[0]
        idx = self.movie_index[matched_title]
        if isinstance(idx, pd.Series):
            idx = idx.iloc[0]

        sim_scores = self._get_content_scores(idx, n)
        source_genres = set(self.movies.iloc[idx]['genres'].split('|'))
        results = []
        for i, score in sim_scores:
            row = self.movies.iloc[i]
            rec_genres = set(row['genres'].split('|'))
            shared = source_genres & rec_genres
            match_pct = f"{score * 100:.1f}%"
            results.append({
                'movie_id': int(row['movieId']),
                'title': row['title_clean'],
                'year': int(row['year']) if not pd.isna(row['year']) else None,
                'genres': row['genres'],
                'similarity_score': round(float(score), 4),
                'match_pct': match_pct,
                'explanation': f"Shares {len(shared)} genre(s) with {matched_title}: {', '.join(shared)}"
            })
        return {
            'seed_movie': matched_title,
            'method': 'content_based',
            'recommendations': results
        }

    def collaborative_recommendations(self, user_id: int, n: int = 10) -> dict:
        rated = set(self.ratings[self.ratings['userId'] == user_id]['movieId'].tolist())
        rated_count = len(rated)
        all_movie_ids = self.movies['movieId'].tolist()
        unrated = [m for m in all_movie_ids if m not in rated]

        predictions = []
        for movie_id in unrated:
            pred = self.svd_model.predict(user_id, movie_id)
            predictions.append((movie_id, pred.est))

        predictions.sort(key=lambda x: x[1], reverse=True)
        top = predictions[:n]

        results = []
        for movie_id, est in top:
            row = self.movies[self.movies['movieId'] == movie_id].iloc[0]
            results.append({
                'movie_id': int(movie_id),
                'title': row['title_clean'],
                'year': int(row['year']) if not pd.isna(row['year']) else None,
                'genres': row['genres'],
                'predicted_rating': round(est, 2),
                'match_pct': f"{min(est/5*100, 100):.1f}%",
                'explanation': f"Predicted {est:.1f}★ based on your rating history"
            })

        return {
            'user_id': user_id,
            'rated_count': rated_count,
            'method': 'collaborative_svd',
            'recommendations': results
        }

    def hybrid_recommendations(self, user_id: int, title: str, n: int = 10, alpha: float = 0.5) -> dict:
        content = self.content_recommendations(title, n=50)
        if 'error' in content:
            return content

        collab_movie_ids = [r['movie_id'] for r in content['recommendations']]
        results = []
        for rec in content['recommendations']:
            movie_id = rec['movie_id']
            pred = self.svd_model.predict(user_id, movie_id)
            content_score = rec['similarity_score']
            collab_score = pred.est / 5.0
            hybrid = alpha * content_score + (1 - alpha) * collab_score
            results.append({
                'movie_id': movie_id,
                'title': rec['title'],
                'year': rec['year'],
                'genres': rec['genres'],
                'hybrid_score': round(hybrid, 4),
                'match_pct': f"{hybrid * 100:.1f}%",
                'explanation': rec['explanation']
            })

        results.sort(key=lambda x: x['hybrid_score'], reverse=True)
        return {
            'user_id': user_id,
            'seed_movie': content['seed_movie'],
            'alpha': alpha,
            'method': 'hybrid',
            'recommendations': results[:n]
        }

    def get_metrics(self) -> dict:
        return {
            'svd_rmse': 0.8727,
            'svd_mae': 0.6713,
            'precision_at_10': 0.745,
            'recall_at_10': 0.509,
            'baseline_rmse': 1.4243,
            'improvement_pct': 38.7
        }
engine = RecommendationEngine()