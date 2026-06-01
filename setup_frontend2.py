import pathlib

files = {}

files['frontend/components/movies/MovieCard.tsx'] = """'use client'
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
      <div className="p-3">
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
"""

files['frontend/components/movies/MovieCarousel.tsx'] = """'use client'
import { useRef } from 'react'
import { motion } from 'framer-motion'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { Movie } from '@/types'
import MovieCard from './MovieCard'

interface MovieCarouselProps {
  title: string
  movies: Movie[]
  onMovieClick?: (movie: Movie) => void
}

export default function MovieCarousel({ title, movies, onMovieClick }: MovieCarouselProps) {
  const scrollRef = useRef<HTMLDivElement>(null)

  const scroll = (direction: 'left' | 'right') => {
    if (scrollRef.current) {
      const amount = 300
      scrollRef.current.scrollBy({
        left: direction === 'left' ? -amount : amount,
        behavior: 'smooth'
      })
    }
  }

  if (movies.length === 0) return null

  return (
    <div className="mb-10">
      <div className="flex items-center justify-between mb-4 px-4">
        <h2 className="text-xl font-bold text-white">{title}</h2>
        <div className="flex gap-2">
          <button
            onClick={() => scroll('left')}
            className="p-1.5 rounded-full bg-zinc-800 hover:bg-zinc-700 text-white transition-colors"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <button
            onClick={() => scroll('right')}
            className="p-1.5 rounded-full bg-zinc-800 hover:bg-zinc-700 text-white transition-colors"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div
        ref={scrollRef}
        className="flex gap-4 overflow-x-auto pb-4 px-4 scrollbar-hide"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        {movies.map((movie) => (
          <div key={movie.movie_id} className="flex-shrink-0 w-40">
            <MovieCard
              movie={movie}
              onClick={() => onMovieClick?.(movie)}
            />
          </div>
        ))}
      </div>
    </div>
  )
}
"""

files['frontend/components/movies/SearchBar.tsx'] = """'use client'
import { useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, X, Loader2 } from 'lucide-react'
import { searchMovies } from '@/lib/api'
import { Movie } from '@/types'

interface SearchBarProps {
  onSelectMovie: (movie: Movie) => void
}

export default function SearchBar({ onSelectMovie }: SearchBarProps) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<Movie[]>([])
  const [loading, setLoading] = useState(false)
  const [open, setOpen] = useState(false)

  const handleSearch = useCallback(async (q: string) => {
    setQuery(q)
    if (q.length < 2) { setResults([]); setOpen(false); return }
    setLoading(true)
    try {
      const data = await searchMovies(q, 8)
      setResults(data.results)
      setOpen(true)
    } catch {
      setResults([])
    } finally {
      setLoading(false)
    }
  }, [])

  const handleSelect = (movie: Movie) => {
    onSelectMovie(movie)
    setQuery('')
    setResults([])
    setOpen(false)
  }

  return (
    <div className="relative w-full max-w-xl mx-auto">
      <div className="relative flex items-center">
        <Search className="absolute left-3 w-4 h-4 text-zinc-400" />
        <input
          type="text"
          value={query}
          onChange={e => handleSearch(e.target.value)}
          placeholder="Search movies..."
          className="w-full pl-10 pr-10 py-3 rounded-xl text-white placeholder-zinc-500 outline-none focus:ring-2 focus:ring-red-600 transition-all"
          style={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }}
        />
        {loading && <Loader2 className="absolute right-3 w-4 h-4 text-zinc-400 animate-spin" />}
        {query && !loading && (
          <button onClick={() => { setQuery(''); setResults([]); setOpen(false) }}
            className="absolute right-3 text-zinc-400 hover:text-white">
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      <AnimatePresence>
        {open && results.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="absolute top-full mt-2 w-full rounded-xl overflow-hidden shadow-2xl z-50"
            style={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }}
          >
            {results.map(movie => (
              <button
                key={movie.movie_id}
                onClick={() => handleSelect(movie)}
                className="w-full px-4 py-3 text-left hover:bg-zinc-700 transition-colors flex items-center justify-between"
              >
                <div>
                  <p className="text-white text-sm font-medium">{movie.title}</p>
                  <p className="text-zinc-400 text-xs">{movie.year} · {movie.genres.split('|').slice(0,2).join(', ')}</p>
                </div>
              </button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
"""

files['frontend/components/recommendations/RecommendationCard.tsx'] = """'use client'
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
"""

files['frontend/components/ui/Navbar.tsx'] = """'use client'
import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Film, Sparkles, Menu, X } from 'lucide-react'

export default function Navbar() {
  const pathname = usePathname()
  const [mobileOpen, setMobileOpen] = useState(false)

  const links = [
    { href: '/', label: 'Home' },
    { href: '/movies', label: 'Movies' },
    { href: '/recommendations', label: 'Recommendations' },
  ]

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-md border-b"
      style={{ backgroundColor: 'rgba(20,20,20,0.95)', borderColor: 'var(--border)' }}>
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 font-bold text-lg">
          <div className="p-1.5 rounded-lg bg-red-600">
            <Film className="w-4 h-4 text-white" />
          </div>
          <span className="text-white">FilmLens</span>
          <span className="text-red-500">AI</span>
        </Link>

        {/* Desktop links */}
        <div className="hidden md:flex items-center gap-6">
          {links.map(link => (
            <Link
              key={link.href}
              href={link.href}
              className={`text-sm font-medium transition-colors ${
                pathname === link.href
                  ? 'text-red-500'
                  : 'text-zinc-400 hover:text-white'
              }`}
            >
              {link.label}
            </Link>
          ))}
        </div>

        {/* AI Badge */}
        <div className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium bg-red-950 text-red-400 border border-red-900">
          <Sparkles className="w-3 h-3" />
          <span>SVD + TF-IDF</span>
        </div>

        {/* Mobile menu button */}
        <button
          className="md:hidden text-zinc-400 hover:text-white"
          onClick={() => setMobileOpen(!mobileOpen)}
        >
          {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden border-t px-4 py-4 flex flex-col gap-3"
          style={{ borderColor: 'var(--border)', backgroundColor: 'var(--background)' }}>
          {links.map(link => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMobileOpen(false)}
              className={`text-sm font-medium py-2 transition-colors ${
                pathname === link.href ? 'text-red-500' : 'text-zinc-400'
              }`}
            >
              {link.label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  )
}
"""

# Write all files
for path, content in files.items():
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')
    print(f"✅ Written: {path}")

print("\n🎉 Core components written successfully")