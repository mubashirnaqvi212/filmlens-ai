import { getGenreColor } from '@/lib/utils'

interface GenreBadgeProps {
  genre: string
  small?: boolean
}

export default function GenreBadge({ genre, small = false }: GenreBadgeProps) {
  return (
    <span className={`
      inline-block rounded-full font-medium
      ${small ? 'px-2 py-0.5 text-xs' : 'px-3 py-1 text-sm'}
      ${getGenreColor(genre)}
    `}>
      {genre}
    </span>
  )
}
