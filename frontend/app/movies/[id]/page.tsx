'use client'
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
