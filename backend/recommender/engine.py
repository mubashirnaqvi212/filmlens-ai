import pickle
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
