'use client'
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
      <div className="flex items-center justify-between" style={{marginBottom: '16px', paddingLeft: '48px', paddingRight: '48px'}}>
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
        className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide" style={{paddingLeft: '48px', paddingRight: '48px', scrollbarWidth: 'none', msOverflowStyle: 'none'}}
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
