'use client'
import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { ThumbsUp, ThumbsDown, Star, Info } from 'lucide-react'
import { RecommendationItem } from '@/types'
import { searchTMDB, submitFeedback } from '@/lib/api'
import { getGenreList } from '@/lib/utils'
import GenreBadge from '@/components/ui/GenreBadge'

interface RecommendationCardProps {
  item: RecommendationItem
  index: number
  userId: number
  recommendationType: 'content' | 'collaborative' | 'hybrid'
}

export default function RecommendationCard({
  item, index, userId, recommendationType
}: RecommendationCardProps) {
  const [poster, setPoster] = useState<string | null>(null)
  const [feedback, setFeedback] = useState<'thumbs_up' | 'thumbs_down' | null>(null)
  const [showExplanation, setShowExplanation] = useState(false)

  useEffect(() => {
    searchTMDB(item.title, item.year ?? undefined).then(setPoster)
  }, [item.title, item.year])

  const handleFeedback = async (signal: 'thumbs_up' | 'thumbs_down') => {
    setFeedback(signal)
    try {
      await submitFeedback(userId, item.movie_id, recommendationType, signal)
    } catch {
      // silent fail — feedback is non-critical
    }
  }

  const genres = getGenreList(item.genres).slice(0, 3)

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      className="rounded-xl overflow-hidden flex gap-4 p-4 group"
      style={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }}
    >
      {/* Poster */}
      <div className="flex-shrink-0 w-16 h-24 rounded-lg overflow-hidden bg-zinc-900">
        {poster ? (
          <img src={poster} alt={item.title} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-zinc-700">
            <Star className="w-6 h-6" />
          </div>
        )}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between gap-2">
          <div>
            <h3 className="font-semibold text-white text-sm leading-tight">{item.title}</h3>
            <p className="text-zinc-400 text-xs mt-0.5">{item.year}</p>
          </div>
          {/* Match percentage */}
          <span className="flex-shrink-0 text-sm font-bold text-red-500">{item.match_pct}</span>
        </div>

        {/* Genres */}
        <div className="flex flex-wrap gap-1 mt-2">
          {genres.map(g => <GenreBadge key={g} genre={g} small />)}
        </div>

        {/* Explanation */}
        <button
          onClick={() => setShowExplanation(!showExplanation)}
          className="flex items-center gap-1 mt-2 text-xs text-zinc-400 hover:text-white transition-colors"
        >
          <Info className="w-3 h-3" />
          <span>Why recommended?</span>
        </button>

        {showExplanation && (
          <motion.p
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="text-xs text-zinc-300 mt-1 p-2 rounded-lg bg-zinc-800"
          >
            {item.explanation}
          </motion.p>
        )}

        {/* Feedback */}
        <div className="flex items-center gap-2 mt-3">
          <button
            onClick={() => handleFeedback('thumbs_up')}
            className={`p-1.5 rounded-lg transition-colors ${
              feedback === 'thumbs_up'
                ? 'bg-green-700 text-white'
                : 'bg-zinc-800 text-zinc-400 hover:text-green-400'
            }`}
          >
            <ThumbsUp className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => handleFeedback('thumbs_down')}
            className={`p-1.5 rounded-lg transition-colors ${
              feedback === 'thumbs_down'
                ? 'bg-red-800 text-white'
                : 'bg-zinc-800 text-zinc-400 hover:text-red-400'
            }`}
          >
            <ThumbsDown className="w-3.5 h-3.5" />
          </button>
          {feedback && (
            <span className="text-xs text-zinc-400">
              {feedback === 'thumbs_up' ? 'Thanks for the feedback!' : 'Got it, noted.'}
            </span>
          )}
        </div>
      </div>
    </motion.div>
  )
}
