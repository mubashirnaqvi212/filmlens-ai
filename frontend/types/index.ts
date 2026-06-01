export interface Movie {
  movie_id: number
  title: string
  year: number | null
  genres: string
  average_rating?: number
  rating_count?: number
  poster_url?: string
  tmdb_id?: number
}

export interface RecommendationItem {
  movie_id: number
  title: string
  year: number | null
  genres: string
  match_pct: string
  explanation: string
  predicted_rating?: number
  hybrid_score?: number
  similarity_score?: number
}

export interface ContentRecommendationResponse {
  seed_movie: string
  method: string
  recommendations: RecommendationItem[]
}

export interface CollaborativeRecommendationResponse {
  user_id: number
  rated_count: number
  method: string
  recommendations: RecommendationItem[]
}

export interface HybridRecommendationResponse {
  user_id: number
  seed_movie: string
  alpha: number
  method: string
  recommendations: RecommendationItem[]
}

export interface ModelMetrics {
  svd_rmse: number
  svd_mae: number
  precision_at_10: number
  recall_at_10: number
  baseline_rmse: number
  improvement_pct: number
}

export interface SearchResponse {
  query: string
  total: number
  results: Movie[]
}
