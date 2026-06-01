import pathlib

files = {}

files['frontend/app/page.tsx'] = """'use client'
import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, TrendingUp, Brain, Zap } from 'lucide-react'
import { getMovies } from '@/lib/api'
import { Movie } from '@/types'
import Navbar from '@/components/ui/Navbar'
import MovieCarousel from '@/components/movies/MovieCarousel'
import SearchBar from '@/components/movies/SearchBar'
import { useRouter } from 'next/navigation'

export default function HomePage() {
  const [movies, setMovies] = useState<Movie[]>([])
  const [actionMovies, setActionMovies] = useState<Movie[]>([])
  const [dramaMovies, setDramaMovies] = useState<Movie[]>([])
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    Promise.all([
      getMovies(1, 20),
      getMovies(1, 20, 'Action'),
      getMovies(1, 20, 'Drama'),
    ]).then(([all, action, drama]) => {
      setMovies(all.results)
      setActionMovies(action.results)
      setDramaMovies(drama.results)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  const handleMovieClick = (movie: Movie) => {
    router.push(`/movies/${movie.movie_id}`)
  }

  const handleSearch = (movie: Movie) => {
    router.push(`/movies/${movie.movie_id}`)
  }

  const stats = [
    { icon: Brain, label: 'ML Model', value: 'SVD + TF-IDF' },
    { icon: TrendingUp, label: 'RMSE Improvement', value: '38.7%' },
    { icon: Sparkles, label: 'Precision@10', value: '74.5%' },
    { icon: Zap, label: 'Movies Indexed', value: '9,742' },
  ]

  return (
    <div className="min-h-screen" style={{ backgroundColor: 'var(--background)' }}>
      <Navbar />

      {/* Hero */}
      <div className="pt-24 pb-16 px-4 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium mb-6 bg-red-950 text-red-400 border border-red-900">
            <Sparkles className="w-4 h-4" />
            <span>AI-Powered Recommendations</span>
          </div>

          <h1 className="text-5xl md:text-6xl font-bold text-white mb-4">
            Film<span className="text-red-500">Lens</span> AI
          </h1>
          <p className="text-zinc-400 text-lg max-w-2xl mx-auto mb-8">
            Smart movie recommendations using SVD collaborative filtering
            and TF-IDF content analysis. Explains every recommendation.
          </p>

          {/* Search */}
          <div className="mb-12">
            <SearchBar onSelectMovie={handleSearch} />
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto">
            {stats.map((stat, i) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 + i * 0.1 }}
                className="rounded-xl p-4 text-center"
                style={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }}
              >
                <stat.icon className="w-5 h-5 text-red-500 mx-auto mb-2" />
                <p className="text-white font-bold text-lg">{stat.value}</p>
                <p className="text-zinc-400 text-xs">{stat.label}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Carousels */}
      {!loading && (
        <div className="pb-16">
          <MovieCarousel
            title="🎬 All Movies"
            movies={movies}
            onMovieClick={handleMovieClick}
          />
          <MovieCarousel
            title="💥 Action"
            movies={actionMovies}
            onMovieClick={handleMovieClick}
          />
          <MovieCarousel
            title="🎭 Drama"
            movies={dramaMovies}
            onMovieClick={handleMovieClick}
          />
        </div>
      )}
    </div>
  )
}
"""

files['frontend/app/movies/[id]/page.tsx'] = """'use client'
import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { Star, Calendar, ArrowLeft, Sparkles } from 'lucide-react'
import { getMovie, getContentRecommendations, getHybridRecommendations, searchTMDB } from '@/lib/api'
import { Movie, RecommendationItem } from '@/types'
import Navbar from '@/components/ui/Navbar'
import GenreBadge from '@/components/ui/GenreBadge'
import RecommendationCard from '@/components/recommendations/RecommendationCard'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import { getGenreList } from '@/lib/utils'

export default function MovieDetailPage() {
  const params = useParams()
  const router = useRouter()
  const movieId = Number(params.id)

  const [movie, setMovie] = useState<Movie | null>(null)
  const [poster, setPoster] = useState<string | null>(null)
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([])
  const [loading, setLoading] = useState(true)
  const [recsLoading, setRecsLoading] = useState(true)

  useEffect(() => {
    getMovie(movieId).then(data => {
      setMovie(data)
      setLoading(false)
      searchTMDB(data.title, data.year).then(setPoster)
      getContentRecommendations(data.title, 8).then(recs => {
        setRecommendations(recs.recommendations)
        setRecsLoading(false)
      }).catch(() => setRecsLoading(false))
    }).catch(() => setLoading(false))
  }, [movieId])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--background)' }}>
        <Navbar />
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!movie) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--background)' }}>
        <Navbar />
        <p className="text-zinc-400">Movie not found</p>
      </div>
    )
  }

  const genres = getGenreList(movie.genres)

  return (
    <div className="min-h-screen" style={{ backgroundColor: 'var(--background)' }}>
      <Navbar />

      <div className="max-w-6xl mx-auto px-4 pt-24 pb-16">
        {/* Back button */}
        <button
          onClick={() => router.back()}
          className="flex items-center gap-2 text-zinc-400 hover:text-white transition-colors mb-8"
        >
          <ArrowLeft className="w-4 h-4" />
          <span className="text-sm">Back</span>
        </button>

        {/* Movie detail */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col md:flex-row gap-8 mb-12"
        >
          {/* Poster */}
          <div className="flex-shrink-0 w-full md:w-64">
            <div className="aspect-[2/3] rounded-2xl overflow-hidden bg-zinc-900">
              {poster ? (
                <img src={poster} alt={movie.title} className="w-full h-full object-cover" />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-zinc-600">
                  <Star className="w-16 h-16" />
                </div>
              )}
            </div>
          </div>

          {/* Info */}
          <div className="flex-1">
            <h1 className="text-4xl font-bold text-white mb-2">{movie.title}</h1>

            <div className="flex items-center gap-4 text-zinc-400 text-sm mb-4">
              <div className="flex items-center gap-1">
                <Calendar className="w-4 h-4" />
                <span>{movie.year ?? 'N/A'}</span>
              </div>
              {movie.average_rating && (
                <div className="flex items-center gap-1">
                  <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                  <span className="text-white font-medium">{movie.average_rating.toFixed(1)}</span>
                  <span>({movie.rating_count?.toLocaleString()} ratings)</span>
                </div>
              )}
            </div>

            <div className="flex flex-wrap gap-2 mb-6">
              {genres.map(g => <GenreBadge key={g} genre={g} />)}
            </div>

            {/* AI badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm bg-red-950 text-red-400 border border-red-900">
              <Sparkles className="w-4 h-4" />
              <span>AI recommendations based on this movie below</span>
            </div>
          </div>
        </motion.div>

        {/* Recommendations */}
        <div>
          <h2 className="text-2xl font-bold text-white mb-6">Similar Movies</h2>
          {recsLoading ? (
            <LoadingSpinner />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {recommendations.map((rec, i) => (
                <RecommendationCard
                  key={rec.movie_id}
                  item={rec}
                  index={i}
                  userId={1}
                  recommendationType="content"
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
"""

files['frontend/app/recommendations/page.tsx'] = """'use client'
import { useState } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, User, Film, Sliders } from 'lucide-react'
import { getHybridRecommendations, getCollaborativeRecommendations } from '@/lib/api'
import { RecommendationItem } from '@/types'
import Navbar from '@/components/ui/Navbar'
import SearchBar from '@/components/movies/SearchBar'
import RecommendationCard from '@/components/recommendations/RecommendationCard'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import { Movie } from '@/types'

export default function RecommendationsPage() {
  const [userId, setUserId] = useState(1)
  const [seedMovie, setSeedMovie] = useState<Movie | null>(null)
  const [alpha, setAlpha] = useState(0.5)
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([])
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState<'hybrid' | 'collaborative'>('hybrid')
  const [seedTitle, setSeedTitle] = useState('')

  const handleGetRecommendations = async () => {
    setLoading(true)
    try {
      if (mode === 'hybrid' && seedMovie) {
        const data = await getHybridRecommendations(userId, seedMovie.title, 12, alpha)
        setRecommendations(data.recommendations)
        setSeedTitle(data.seed_movie)
      } else {
        const data = await getCollaborativeRecommendations(userId, 12)
        setRecommendations(data.recommendations)
        setSeedTitle('')
      }
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: 'var(--background)' }}>
      <Navbar />

      <div className="max-w-5xl mx-auto px-4 pt-24 pb-16">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-10"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm mb-4 bg-red-950 text-red-400 border border-red-900">
            <Sparkles className="w-4 h-4" />
            <span>AI Recommendation Engine</span>
          </div>
          <h1 className="text-4xl font-bold text-white mb-2">Get Recommendations</h1>
          <p className="text-zinc-400">Powered by SVD collaborative filtering + TF-IDF content analysis</p>
        </motion.div>

        {/* Controls */}
        <div className="rounded-2xl p-6 mb-8" style={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }}>
          {/* Mode toggle */}
          <div className="flex gap-3 mb-6">
            <button
              onClick={() => setMode('hybrid')}
              className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-xl text-sm font-medium transition-all ${
                mode === 'hybrid'
                  ? 'bg-red-600 text-white'
                  : 'bg-zinc-800 text-zinc-400 hover:text-white'
              }`}
            >
              <Sparkles className="w-4 h-4" />
              Hybrid (Recommended)
            </button>
            <button
              onClick={() => setMode('collaborative')}
              className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-xl text-sm font-medium transition-all ${
                mode === 'collaborative'
                  ? 'bg-red-600 text-white'
                  : 'bg-zinc-800 text-zinc-400 hover:text-white'
              }`}
            >
              <User className="w-4 h-4" />
              Collaborative Only
            </button>
          </div>

          {/* User ID */}
          <div className="mb-4">
            <label className="flex items-center gap-2 text-sm text-zinc-400 mb-2">
              <User className="w-4 h-4" />
              User ID (1–610)
            </label>
            <input
              type="number"
              min={1}
              max={610}
              value={userId}
              onChange={e => setUserId(Number(e.target.value))}
              className="w-full px-4 py-3 rounded-xl text-white outline-none focus:ring-2 focus:ring-red-600"
              style={{ backgroundColor: 'var(--background)', border: '1px solid var(--border)' }}
            />
          </div>

          {/* Seed movie (hybrid only) */}
          {mode === 'hybrid' && (
            <div className="mb-4">
              <label className="flex items-center gap-2 text-sm text-zinc-400 mb-2">
                <Film className="w-4 h-4" />
                Seed Movie
              </label>
              {seedMovie ? (
                <div className="flex items-center justify-between px-4 py-3 rounded-xl"
                  style={{ backgroundColor: 'var(--background)', border: '1px solid var(--border)' }}>
                  <div>
                    <p className="text-white text-sm font-medium">{seedMovie.title}</p>
                    <p className="text-zinc-400 text-xs">{seedMovie.year}</p>
                  </div>
                  <button onClick={() => setSeedMovie(null)} className="text-zinc-400 hover:text-white text-xs">
                    Change
                  </button>
                </div>
              ) : (
                <SearchBar onSelectMovie={setSeedMovie} />
              )}
            </div>
          )}

          {/* Alpha slider (hybrid only) */}
          {mode === 'hybrid' && (
            <div className="mb-6">
              <label className="flex items-center justify-between text-sm text-zinc-400 mb-2">
                <div className="flex items-center gap-2">
                  <Sliders className="w-4 h-4" />
                  Content vs Collaborative weight
                </div>
                <span className="text-white font-medium">α = {alpha.toFixed(1)}</span>
              </label>
              <input
                type="range"
                min={0}
                max={1}
                step={0.1}
                value={alpha}
                onChange={e => setAlpha(Number(e.target.value))}
                className="w-full accent-red-600"
              />
              <div className="flex justify-between text-xs text-zinc-500 mt-1">
                <span>Pure Collaborative</span>
                <span>Balanced</span>
                <span>Pure Content</span>
              </div>
            </div>
          )}

          {/* Submit */}
          <button
            onClick={handleGetRecommendations}
            disabled={loading || (mode === 'hybrid' && !seedMovie)}
            className="w-full py-3 rounded-xl font-semibold text-white transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            style={{ backgroundColor: 'var(--accent)' }}
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                Get Recommendations
              </>
            )}
          </button>
        </div>

        {/* Results */}
        {recommendations.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-white">
                {seedTitle ? `Because you liked: ${seedTitle}` : `Recommended for User ${userId}`}
              </h2>
              <span className="text-zinc-400 text-sm">{recommendations.length} results</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {recommendations.map((rec, i) => (
                <RecommendationCard
                  key={rec.movie_id}
                  item={rec}
                  index={i}
                  userId={userId}
                  recommendationType={mode === 'hybrid' ? 'hybrid' : 'collaborative'}
                />
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}
"""

files['frontend/app/movies/page.tsx'] = """'use client'
import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { Film } from 'lucide-react'
import { getMovies } from '@/lib/api'
import { Movie } from '@/types'
import Navbar from '@/components/ui/Navbar'
import MovieCard from '@/components/movies/MovieCard'
import SearchBar from '@/components/movies/SearchBar'
import LoadingSpinner from '@/components/ui/LoadingSpinner'

const GENRES = ['All', 'Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Thriller', 'Romance', 'Animation', 'Documentary']

export default function MoviesPage() {
  const [movies, setMovies] = useState<Movie[]>([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [genre, setGenre] = useState('All')
  const router = useRouter()

  useEffect(() => {
    setLoading(true)
    getMovies(page, 24, genre === 'All' ? undefined : genre)
      .then(data => {
        setMovies(data.results)
        setTotal(data.total)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [page, genre])

  const handleGenreChange = (g: string) => {
    setGenre(g)
    setPage(1)
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: 'var(--background)' }}>
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 pt-24 pb-16">
        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <Film className="w-6 h-6 text-red-500" />
          <h1 className="text-3xl font-bold text-white">Movies</h1>
          <span className="text-zinc-400 text-sm">({total.toLocaleString()} total)</span>
        </div>

        {/* Search */}
        <div className="mb-6">
          <SearchBar onSelectMovie={m => router.push(`/movies/${m.movie_id}`)} />
        </div>

        {/* Genre filter */}
        <div className="flex flex-wrap gap-2 mb-8">
          {GENRES.map(g => (
            <button
              key={g}
              onClick={() => handleGenreChange(g)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                genre === g
                  ? 'bg-red-600 text-white'
                  : 'bg-zinc-800 text-zinc-400 hover:text-white hover:bg-zinc-700'
              }`}
            >
              {g}
            </button>
          ))}
        </div>

        {/* Grid */}
        {loading ? (
          <div className="flex justify-center py-20">
            <LoadingSpinner size="lg" />
          </div>
        ) : (
          <>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
              {movies.map((movie, i) => (
                <motion.div
                  key={movie.movie_id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.02 }}
                >
                  <MovieCard
                    movie={movie}
                    onClick={() => router.push(`/movies/${movie.movie_id}`)}
                  />
                </motion.div>
              ))}
            </div>

            {/* Pagination */}
            <div className="flex items-center justify-center gap-4 mt-10">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-6 py-2 rounded-xl text-sm font-medium bg-zinc-800 text-zinc-400 hover:text-white disabled:opacity-40 transition-all"
              >
                Previous
              </button>
              <span className="text-zinc-400 text-sm">Page {page}</span>
              <button
                onClick={() => setPage(p => p + 1)}
                disabled={movies.length < 24}
                className="px-6 py-2 rounded-xl text-sm font-medium bg-zinc-800 text-zinc-400 hover:text-white disabled:opacity-40 transition-all"
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
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

print("\n🎉 All pages written successfully")