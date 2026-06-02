import type { Metadata } from 'next'
import './globals.css'
import Footer from '@/components/ui/Footer'

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
      <body style={{ backgroundColor: '#141414', color: 'white', margin: 0 }}>
        {children}
        <Footer />
      </body>
    </html>
  )
}