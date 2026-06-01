import pathlib

files = {}

files['frontend/types/index.ts'] = """export interface Movie {
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
"""

files['frontend/lib/api.ts'] = """import axios from 'axios'

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
"""

files['frontend/lib/utils.ts'] = """import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function getGenreList(genres: string): string[] {
  return genres.split('|').filter(g => g !== '(no genres listed)')
}

export function formatRating(rating: number): string {
  return rating.toFixed(1)
}

export function getGenreColor(genre: string): string {
  const colors: Record<string, string> = {
    'Action': 'bg-red-900 text-red-200',
    'Adventure': 'bg-orange-900 text-orange-200',
    'Animation': 'bg-yellow-900 text-yellow-200',
    'Comedy': 'bg-green-900 text-green-200',
    'Crime': 'bg-gray-800 text-gray-200',
    'Documentary': 'bg-blue-900 text-blue-200',
    'Drama': 'bg-purple-900 text-purple-200',
    'Fantasy': 'bg-pink-900 text-pink-200',
    'Horror': 'bg-red-950 text-red-300',
    'Mystery': 'bg-indigo-900 text-indigo-200',
    'Romance': 'bg-rose-900 text-rose-200',
    'SciFi': 'bg-cyan-900 text-cyan-200',
    'Sci-Fi': 'bg-cyan-900 text-cyan-200',
    'Thriller': 'bg-slate-800 text-slate-200',
    'War': 'bg-stone-800 text-stone-200',
    'Western': 'bg-amber-900 text-amber-200',
  }
  return colors[genre] || 'bg-zinc-800 text-zinc-200'
}
"""

files['frontend/app/globals.css'] = """@import "tailwindcss";

:root {
  --background: #141414;
  --foreground: #ffffff;
  --card: #1f1f1f;
  --card-hover: #2a2a2a;
  --accent: #e50914;
  --accent-hover: #f40612;
  --muted: #6b7280;
  --border: #2a2a2a;
}

* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

html,
body {
  max-width: 100vw;
  overflow-x: hidden;
  background-color: var(--background);
  color: var(--foreground);
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: var(--background);
}
::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}
"""

files['frontend/app/layout.tsx'] = """import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'FilmLens AI — Smart Movie Recommendations',
  description: 'AI-powered movie recommendations using SVD collaborative filtering and content-based filtering',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen" style={{ backgroundColor: 'var(--background)', color: 'var(--foreground)' }}>
        {children}
      </body>
    </html>
  )
}
"""

files['frontend/components/ui/GenreBadge.tsx'] = """import { getGenreColor } from '@/lib/utils'

interface GenreBadgeProps {
  genre: string
  small?: boolean
}

export default function GenreBadge({ genre, small = false }: GenreBadgeProps) {
  return (
    <span className={`
      inline-block rounded-full font-medium
      ${small ? 'px-2 py-0.5 text-xs' : 'px-3 py-1 text-sm'}
      ${getGenreColor(genre)}
    `}>
      {genre}
    </span>
  )
}
"""

files['frontend/components/ui/LoadingSpinner.tsx'] = """export default function LoadingSpinner({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) {
  const sizes = { sm: 'w-4 h-4', md: 'w-8 h-8', lg: 'w-12 h-12' }
  return (
    <div className="flex items-center justify-center">
      <div className={`${sizes[size]} border-2 border-zinc-700 border-t-red-600 rounded-full animate-spin`} />
    </div>
  )
}
"""

files['frontend/components/ui/StarRating.tsx'] = """'use client'
import { useState } from 'react'
import { Star } from 'lucide-react'

interface StarRatingProps {
  onRate: (rating: number) => void
  initialRating?: number
}

export default function StarRating({ onRate, initialRating = 0 }: StarRatingProps) {
  const [hovered, setHovered] = useState(0)
  const [selected, setSelected] = useState(initialRating)

  const ratings = [1, 2, 3, 4, 5]

  return (
    <div className="flex gap-1">
      {ratings.map((r) => (
        <button
          key={r}
          onMouseEnter={() => setHovered(r)}
          onMouseLeave={() => setHovered(0)}
          onClick={() => { setSelected(r); onRate(r) }}
          className="transition-transform hover:scale-110"
        >
          <Star
            className={`w-6 h-6 ${
              r <= (hovered || selected)
                ? 'fill-yellow-400 text-yellow-400'
                : 'text-zinc-600'
            }`}
          />
        </button>
      ))}
    </div>
  )
}
"""

# Write all files
for path, content in files.items():
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')
    print(f"✅ Written: {path}")

print("\\n🎉 Frontend foundation files written successfully")