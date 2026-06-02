'use client'
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

      <div className="max-w-5xl mx-auto px-4 pb-16" style={{paddingTop: '100px'}}>
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
