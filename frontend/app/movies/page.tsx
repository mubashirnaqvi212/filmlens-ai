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
    <div className="min-h-screen bg-[#141414]">
      <Navbar />

      <div style={{paddingTop: '100px', paddingLeft: '48px', paddingRight: '48px', paddingBottom: '64px'}}>

        {/* Header */}
        <div style={{display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px'}}>
          <Film style={{width: '24px', height: '24px', color: '#e50914'}} />
          <h1 style={{fontSize: '30px', fontWeight: 'bold', color: 'white'}}>Movies</h1>
          <span style={{color: '#6b7280', fontSize: '14px'}}>({total.toLocaleString()} total)</span>
        </div>

        {/* Search */}
        <div style={{maxWidth: '480px', marginBottom: '20px'}}>
          <SearchBar onSelectMovie={m => router.push(`/movies/${m.movie_id}`)} />
        </div>

        {/* Genre filter */}
        <div style={{display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '32px'}}>
          {GENRES.map(g => (
            <button
              key={g}
              onClick={() => handleGenreChange(g)}
              style={{
                padding: '8px 16px',
                borderRadius: '9999px',
                fontSize: '14px',
                fontWeight: '500',
                border: 'none',
                cursor: 'pointer',
                backgroundColor: genre === g ? '#e50914' : '#27272a',
                color: genre === g ? 'white' : '#a1a1aa',
                transition: 'all 0.2s'
              }}
            >
              {g}
            </button>
          ))}
        </div>

        {/* Grid */}
        {loading ? (
          <div style={{display: 'flex', justifyContent: 'center', paddingTop: '80px', paddingBottom: '80px'}}>
            <LoadingSpinner size="lg" />
          </div>
        ) : (
          <>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))',
              gap: '16px'
            }}>
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
            <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px', marginTop: '40px'}}>
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                style={{
                  padding: '8px 24px',
                  borderRadius: '12px',
                  fontSize: '14px',
                  fontWeight: '500',
                  backgroundColor: '#27272a',
                  color: page === 1 ? '#52525b' : '#a1a1aa',
                  border: 'none',
                  cursor: page === 1 ? 'not-allowed' : 'pointer'
                }}
              >
                Previous
              </button>
              <span style={{color: '#6b7280', fontSize: '14px'}}>Page {page}</span>
              <button
                onClick={() => setPage(p => p + 1)}
                disabled={movies.length < 24}
                style={{
                  padding: '8px 24px',
                  borderRadius: '12px',
                  fontSize: '14px',
                  fontWeight: '500',
                  backgroundColor: '#27272a',
                  color: movies.length < 24 ? '#52525b' : '#a1a1aa',
                  border: 'none',
                  cursor: movies.length < 24 ? 'not-allowed' : 'pointer'
                }}
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
