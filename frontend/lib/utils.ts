import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function getGenreList(genres: string): string[] {
  return genres.split('|').filter(g => g !== '(no genres listed)')
}

export function formatRating(rating: number): string {
  return rating.toFixed(1)
}

export function getGenreColor(genre: string): string {
  const colors: Record<string, string> = {
    'Action': 'bg-red-900 text-red-200',
    'Adventure': 'bg-orange-900 text-orange-200',
    'Animation': 'bg-yellow-900 text-yellow-200',
    'Comedy': 'bg-green-900 text-green-200',
    'Crime': 'bg-gray-800 text-gray-200',
    'Documentary': 'bg-blue-900 text-blue-200',
    'Drama': 'bg-purple-900 text-purple-200',
    'Fantasy': 'bg-pink-900 text-pink-200',
    'Horror': 'bg-red-950 text-red-300',
    'Mystery': 'bg-indigo-900 text-indigo-200',
    'Romance': 'bg-rose-900 text-rose-200',
    'SciFi': 'bg-cyan-900 text-cyan-200',
    'Sci-Fi': 'bg-cyan-900 text-cyan-200',
    'Thriller': 'bg-slate-800 text-slate-200',
    'War': 'bg-stone-800 text-stone-200',
    'Western': 'bg-amber-900 text-amber-200',
  }
  return colors[genre] || 'bg-zinc-800 text-zinc-200'
}
