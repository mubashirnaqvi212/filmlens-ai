'use client'
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
  className="w-full rounded-xl text-white outline-none transition-all"
  style={{
    backgroundColor: '#2a2a2a',
    border: '1px solid #555',
    paddingLeft: '40px',
    paddingRight: '40px',
    paddingTop: '12px',
    paddingBottom: '12px',
    color: 'white',
  }}
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
            style={{ backgroundColor: '#2a2a2a', border: '1px solid #555' }}
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
