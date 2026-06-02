'use client'
import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Star, Calendar, Film } from 'lucide-react'
import { Movie } from '@/types'
import { searchTMDB } from '@/lib/api'
import { getGenreList } from '@/lib/utils'
import GenreBadge from '@/components/ui/GenreBadge'

interface MovieCardProps {
  movie: Movie
  onClick?: () => void
  showRating?: boolean
}

export default function MovieCard({ movie, onClick, showRating = true }: MovieCardProps) {
  const [poster, setPoster] = useState<string | null>(null)
  const [imageLoaded, setImageLoaded] = useState(false)

  useEffect(() => {
    searchTMDB(movie.title, movie.year ?? undefined).then(url => {
      setPoster(url)
    })
  }, [movie.title, movie.year])

  const genres = getGenreList(movie.genres).slice(0, 2)

  return (
    <motion.div
      whileHover={{ scale: 1.03, y: -4 }}
      transition={{ duration: 0.2 }}
      onClick={onClick}
      className="cursor-pointer rounded-xl overflow-hidden group"
      style={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }}
    >
      {/* Poster */}
      <div className="relative aspect-[2/3] overflow-hidden bg-zinc-900">
        {poster ? (
          <img
            src={poster}
            alt={movie.title}
            className={`w-full h-full object-cover transition-opacity duration-300 ${
              imageLoaded ? 'opacity-100' : 'opacity-0'
            }`}
            onLoad={() => setImageLoaded(true)}
          />
        ) : (
          <div className="w-full h-full flex flex-col items-center justify-center gap-2 text-zinc-600">
            <Film className="w-12 h-12" />
            <span className="text-xs text-center px-2">{movie.title}</span>
          </div>
        )}

        {/* Overlay on hover */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

        {/* Rating badge */}
        {showRating && movie.average_rating && (
          <div className="absolute top-2 right-2 flex items-center gap-1 bg-black/70 rounded-full px-2 py-1">
            <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
            <span className="text-xs text-white font-medium">
              {movie.average_rating.toFixed(1)}
            </span>
          </div>
        )}
      </div>

      {/* Info */}
      <div className="p-3 pb-4">
        <h3 className="font-semibold text-white text-sm leading-tight line-clamp-2 mb-1">
          {movie.title}
        </h3>
        <div className="flex items-center gap-1 text-zinc-400 text-xs mb-2">
          <Calendar className="w-3 h-3" />
          <span>{movie.year ?? 'N/A'}</span>
        </div>
        <div className="flex flex-wrap gap-1">
          {genres.map(g => (
            <GenreBadge key={g} genre={g} small />
          ))}
        </div>
      </div>
    </motion.div>
  )
}
