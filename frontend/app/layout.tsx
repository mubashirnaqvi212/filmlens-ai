import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'FilmLens AI — Smart Movie Recommendations',
  description: 'AI-powered movie recommendations using SVD collaborative filtering and content-based filtering',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen" style={{ backgroundColor: 'var(--background)', color: 'var(--foreground)' }}>
        {children}
      </body>
    </html>
  )
}
