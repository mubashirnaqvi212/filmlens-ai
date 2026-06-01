'use client'
import { useState } from 'react'
import { Star } from 'lucide-react'

interface StarRatingProps {
  onRate: (rating: number) => void
  initialRating?: number
}

export default function StarRating({ onRate, initialRating = 0 }: StarRatingProps) {
  const [hovered, setHovered] = useState(0)
  const [selected, setSelected] = useState(initialRating)

  const ratings = [1, 2, 3, 4, 5]

  return (
    <div className="flex gap-1">
      {ratings.map((r) => (
        <button
          key={r}
          onMouseEnter={() => setHovered(r)}
          onMouseLeave={() => setHovered(0)}
          onClick={() => { setSelected(r); onRate(r) }}
          className="transition-transform hover:scale-110"
        >
          <Star
            className={`w-6 h-6 ${
              r <= (hovered || selected)
                ? 'fill-yellow-400 text-yellow-400'
                : 'text-zinc-600'
            }`}
          />
        </button>
      ))}
    </div>
  )
}
