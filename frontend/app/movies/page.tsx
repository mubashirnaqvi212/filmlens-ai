'use client'
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
