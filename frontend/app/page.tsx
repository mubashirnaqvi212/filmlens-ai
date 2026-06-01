'use client'
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

  const stats = [
    { icon: Brain, label: 'ML Model', value: 'SVD + TF-IDF' },
    { icon: TrendingUp, label: 'RMSE Improvement', value: '38.7%' },
    { icon: Sparkles, label: 'Precision@10', value: '74.5%' },
    { icon: Zap, label: 'Movies Indexed', value: '9,742' },
  ]

  return (
    <div className="min-h-screen bg-[#141414]">
      <Navbar />
      <div className="flex flex-col items-center w-full pb-16 px-4" style={{paddingTop: '120px'}}>
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="flex flex-col items-center text-center w-full max-w-3xl"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium mb-6 bg-red-950 text-red-400 border border-red-900">
            <Sparkles className="w-4 h-4" />
            <span>AI-Powered Recommendations</span>
          </div>
          <h1 className="text-6xl md:text-7xl font-bold text-white mb-4 leading-tight tracking-tight">
            Film<span className="text-red-500">Lens</span> AI
          </h1><p className="text-zinc-400 text-lg max-w-xl leading-relaxed" style={{marginBottom: '32px'}}>
          
            Smart movie recommendations using SVD collaborative filtering
            and TF-IDF content analysis. Explains every recommendation.
          </p>
          <div className="w-full max-w-xl mx-auto" style={{marginBottom: '32px'}}>
            <SearchBar onSelectMovie={(m) => router.push(`/movies/${m.movie_id}`)} />
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full">
            {stats.map((stat, i) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 + i * 0.1 }}
                className="rounded-xl p-4 flex flex-col items-center text-center bg-[#1f1f1f] border border-[#2a2a2a]"
              >
                <stat.icon className="w-5 h-5 text-red-500 mb-2" />
                <p className="text-white font-bold text-lg">{stat.value}</p>
                <p className="text-zinc-400 text-xs">{stat.label}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
      {!loading && (
        <div className="pb-16">
          <MovieCarousel title="🎬 All Movies" movies={movies} onMovieClick={(m) => router.push(`/movies/${m.movie_id}`)} />
          <MovieCarousel title="💥 Action" movies={actionMovies} onMovieClick={(m) => router.push(`/movies/${m.movie_id}`)} />
          <MovieCarousel title="🎭 Drama" movies={dramaMovies} onMovieClick={(m) => router.push(`/movies/${m.movie_id}`)} />
        </div>
      )}
    </div>
  )
}
