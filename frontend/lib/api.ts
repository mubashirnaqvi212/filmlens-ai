import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const TMDB_KEY = process.env.NEXT_PUBLIC_TMDB_API_KEY
const TMDB_IMAGE_BASE = process.env.NEXT_PUBLIC_TMDB_IMAGE_BASE || 'https://image.tmdb.org/t/p/w500'

export const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
})

// ── Movies ────────────────────────────────────────────────────────────────

export async function searchMovies(query: string, limit = 10) {
  const res = await api.get('/movies/search', { params: { query, limit } })
  return res.data
}

export async function getMovie(movieId: number) {
  const res = await api.get(`/movies/${movieId}`)
  return res.data
}

export async function getMovies(page = 1, limit = 20, genre?: string) {
  const res = await api.get('/movies/', { params: { page, limit, genre } })
  return res.data
}

// ── Recommendations ───────────────────────────────────────────────────────

export async function getContentRecommendations(title: string, n = 10) {
  const res = await api.get('/recommend/content', { params: { title, n } })
  return res.data
}

export async function getCollaborativeRecommendations(userId: number, n = 10) {
  const res = await api.get(`/recommend/user/${userId}`, { params: { n } })
  return res.data
}

export async function getHybridRecommendations(
  userId: number, title: string, n = 10, alpha = 0.5
) {
  const res = await api.get(`/recommend/hybrid/${userId}`, {
    params: { title, n, alpha }
  })
  return res.data
}

export async function getMetrics() {
  const res = await api.get('/recommend/metrics')
  return res.data
}

// ── Ratings & Feedback ────────────────────────────────────────────────────

export async function submitRating(userId: number, movieId: number, rating: number) {
  const res = await api.post('/rate', { user_id: userId, movie_id: movieId, rating })
  return res.data
}

export async function submitFeedback(
  userId: number, movieId: number,
  recommendationType: string, signal: string
) {
  const res = await api.post('/feedback', {
    user_id: userId,
    movie_id: movieId,
    recommendation_type: recommendationType,
    signal
  })
  return res.data
}

// ── TMDB ──────────────────────────────────────────────────────────────────

export async function getTMDBPoster(tmdbId: number): Promise<string | null> {
  if (!TMDB_KEY || !tmdbId) return null
  try {
    const res = await axios.get(
      `https://api.themoviedb.org/3/movie/${tmdbId}`,
      { params: { api_key: TMDB_KEY } }
    )
    const path = res.data.poster_path
    return path ? `${TMDB_IMAGE_BASE}${path}` : null
  } catch {
    return null
  }
}

export async function searchTMDB(title: string, year?: number): Promise<string | null> {
  if (!TMDB_KEY) return null
  try {
    const res = await axios.get(
      'https://api.themoviedb.org/3/search/movie',
      { params: { api_key: TMDB_KEY, query: title, year } }
    )
    const results = res.data.results
    if (results && results.length > 0 && results[0].poster_path) {
      return `${TMDB_IMAGE_BASE}${results[0].poster_path}`
    }
    return null
  } catch {
    return null
  }
}
