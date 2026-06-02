'use client'
import { useState } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, User, Film, Sliders, ChevronRight } from 'lucide-react'
import { getHybridRecommendations, getCollaborativeRecommendations } from '@/lib/api'
import { RecommendationItem, Movie } from '@/types'
import Navbar from '@/components/ui/Navbar'
import SearchBar from '@/components/movies/SearchBar'
import RecommendationCard from '@/components/recommendations/RecommendationCard'
import LoadingSpinner from '@/components/ui/LoadingSpinner'

export default function RecommendationsPage() {
  const [userId, setUserId] = useState(1)
  const [seedMovie, setSeedMovie] = useState<Movie | null>(null)
  const [alpha, setAlpha] = useState(0.5)
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([])
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState<'hybrid' | 'collaborative'>('hybrid')
  const [seedTitle, setSeedTitle] = useState('')
  const [hasResults, setHasResults] = useState(false)

  const handleGetRecommendations = async () => {
    setLoading(true)
    try {
      if (mode === 'hybrid' && seedMovie) {
        const data = await getHybridRecommendations(userId, seedMovie.title, 12, alpha)
        setRecommendations(data.recommendations)
        setSeedTitle(data.seed_movie)
      } else {
        const data = await getCollaborativeRecommendations(userId, 12)
        setRecommendations(data.recommendations)
        setSeedTitle('')
      }
      setHasResults(true)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#141414' }}>
      <Navbar />

      <div style={{ paddingTop: '100px', paddingBottom: '64px' }}>

        {/* Hero Header */}
        <div style={{ textAlign: 'center', marginBottom: '48px', padding: '0 24px' }}>
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: '8px',
            padding: '8px 16px', borderRadius: '9999px',
            backgroundColor: '#450a0a', color: '#f87171',
            border: '1px solid #7f1d1d', fontSize: '13px',
            fontWeight: '500', marginBottom: '16px'
          }}>
            <Sparkles style={{ width: '14px', height: '14px' }} />
            AI Recommendation Engine
          </div>
          <h1 style={{ fontSize: '42px', fontWeight: 'bold', color: 'white', marginBottom: '8px' }}>
            Get Recommendations
          </h1>
          <p style={{ color: '#71717a', fontSize: '16px' }}>
            Powered by SVD collaborative filtering + TF-IDF content analysis
          </p>
        </div>

        {/* Main Layout */}
        <div style={{
          maxWidth: '1100px', margin: '0 auto',
          padding: '0 24px',
          display: 'grid',
          gridTemplateColumns: hasResults ? '380px 1fr' : '1fr',
          gap: '32px',
          alignItems: 'start'
        }}>

          {/* Controls Panel */}
          <div style={{
            backgroundColor: '#1c1c1c',
            border: '1px solid #2a2a2a',
            borderRadius: '20px',
            padding: '28px',
            ...(hasResults ? {} : { maxWidth: '480px', margin: '0 auto', width: '100%' })
          }}>

            {/* Mode Toggle */}
            <div style={{
              display: 'grid', gridTemplateColumns: '1fr 1fr',
              gap: '8px', marginBottom: '28px',
              backgroundColor: '#141414',
              padding: '4px', borderRadius: '14px'
            }}>
              {[
                { key: 'hybrid', label: 'Hybrid', icon: Sparkles },
                { key: 'collaborative', label: 'Collaborative', icon: User }
              ].map(({ key, label, icon: Icon }) => (
                <button
                  key={key}
                  onClick={() => setMode(key as 'hybrid' | 'collaborative')}
                  style={{
                    display: 'flex', alignItems: 'center',
                    justifyContent: 'center', gap: '6px',
                    padding: '10px', borderRadius: '10px',
                    fontSize: '13px', fontWeight: '600',
                    border: 'none', cursor: 'pointer',
                    transition: 'all 0.2s',
                    backgroundColor: mode === key ? '#e50914' : 'transparent',
                    color: mode === key ? 'white' : '#71717a',
                  }}
                >
                  <Icon style={{ width: '14px', height: '14px' }} />
                  {label}
                </button>
              ))}
            </div>

            {/* User ID */}
            <div style={{ marginBottom: '20px' }}>
              <label style={{
                display: 'flex', alignItems: 'center', gap: '6px',
                fontSize: '13px', color: '#a1a1aa',
                marginBottom: '8px', fontWeight: '500'
              }}>
                <User style={{ width: '14px', height: '14px' }} />
                User ID (1–610)
              </label>
              <input
                type="number"
                min={1} max={610}
                value={userId}
                onChange={e => setUserId(Number(e.target.value))}
                style={{
                  width: '100%', padding: '12px 16px',
                  borderRadius: '12px', color: 'white',
                  backgroundColor: '#141414',
                  border: '1px solid #2a2a2a',
                  fontSize: '14px', outline: 'none',
                  boxSizing: 'border-box'
                }}
              />
            </div>

            {/* Seed Movie */}
            {mode === 'hybrid' && (
              <div style={{ marginBottom: '20px' }}>
                <label style={{
                  display: 'flex', alignItems: 'center', gap: '6px',
                  fontSize: '13px', color: '#a1a1aa',
                  marginBottom: '8px', fontWeight: '500'
                }}>
                  <Film style={{ width: '14px', height: '14px' }} />
                  Seed Movie
                </label>
                {seedMovie ? (
                  <div style={{
                    display: 'flex', alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '12px 16px', borderRadius: '12px',
                    backgroundColor: '#141414',
                    border: '1px solid #2a2a2a'
                  }}>
                    <div>
                      <p style={{ color: 'white', fontSize: '14px', fontWeight: '500', margin: 0 }}>
                        {seedMovie.title}
                      </p>
                      <p style={{ color: '#71717a', fontSize: '12px', margin: '2px 0 0 0' }}>
                        {seedMovie.year}
                      </p>
                    </div>
                    <button
                      onClick={() => setSeedMovie(null)}
                      style={{
                        color: '#71717a', background: 'none',
                        border: 'none', cursor: 'pointer',
                        fontSize: '12px'
                      }}
                    >
                      Change
                    </button>
                  </div>
                ) : (
                  <SearchBar onSelectMovie={setSeedMovie} />
                )}
              </div>
            )}

            {/* Alpha Slider */}
            {mode === 'hybrid' && (
              <div style={{ marginBottom: '28px' }}>
                <div style={{
                  display: 'flex', justifyContent: 'space-between',
                  alignItems: 'center', marginBottom: '10px'
                }}>
                  <label style={{
                    display: 'flex', alignItems: 'center', gap: '6px',
                    fontSize: '13px', color: '#a1a1aa', fontWeight: '500'
                  }}>
                    <Sliders style={{ width: '14px', height: '14px' }} />
                    Blend Weight
                  </label>
                  <span style={{
                    fontSize: '13px', fontWeight: '600',
                    color: '#e50914',
                    backgroundColor: '#450a0a',
                    padding: '2px 10px', borderRadius: '9999px'
                  }}>
                    α = {alpha.toFixed(1)}
                  </span>
                </div>
                <input
                  type="range" min={0} max={1} step={0.1}
                  value={alpha}
                  onChange={e => setAlpha(Number(e.target.value))}
                  style={{ width: '100%', accentColor: '#e50914' }}
                />
                <div style={{
                  display: 'flex', justifyContent: 'space-between',
                  fontSize: '11px', color: '#52525b', marginTop: '6px'
                }}>
                  <span>← Collaborative</span>
                  <span>Balanced</span>
                  <span>Content →</span>
                </div>
              </div>
            )}

            {/* Submit Button */}
            <button
              onClick={handleGetRecommendations}
              disabled={loading || (mode === 'hybrid' && !seedMovie)}
              style={{
                width: '100%', padding: '14px',
                borderRadius: '14px', fontWeight: '600',
                fontSize: '15px', color: 'white',
                backgroundColor: (loading || (mode === 'hybrid' && !seedMovie))
                  ? '#7f1d1d' : '#e50914',
                border: 'none',
                cursor: (loading || (mode === 'hybrid' && !seedMovie))
                  ? 'not-allowed' : 'pointer',
                display: 'flex', alignItems: 'center',
                justifyContent: 'center', gap: '8px',
                transition: 'all 0.2s'
              }}
            >
              {loading ? (
                <>
                  <div style={{
                    width: '16px', height: '16px',
                    border: '2px solid rgba(255,255,255,0.3)',
                    borderTop: '2px solid white',
                    borderRadius: '50%',
                    animation: 'spin 0.8s linear infinite'
                  }} />
                  Generating...
                </>
              ) : (
                <>
                  <Sparkles style={{ width: '16px', height: '16px' }} />
                  Get Recommendations
                  <ChevronRight style={{ width: '16px', height: '16px' }} />
                </>
              )}
            </button>
          </div>

          {/* Results */}
          {hasResults && (
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4 }}
            >
              <div style={{
                display: 'flex', alignItems: 'center',
                justifyContent: 'space-between', marginBottom: '20px'
              }}>
                <div>
                  <h2 style={{ color: 'white', fontSize: '20px', fontWeight: 'bold', margin: 0 }}>
                    {seedTitle ? `Because you liked "${seedTitle}"` : `For User ${userId}`}
                  </h2>
                  <p style={{ color: '#71717a', fontSize: '13px', margin: '4px 0 0 0' }}>
                    {recommendations.length} recommendations
                  </p>
                </div>
                <div style={{
                  padding: '6px 14px', borderRadius: '9999px',
                  backgroundColor: '#1c1c1c', border: '1px solid #2a2a2a',
                  fontSize: '12px', color: '#a1a1aa'
                }}>
                  {mode === 'hybrid' ? `Hybrid · α=${alpha}` : 'Collaborative SVD'}
                </div>
              </div>

              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                gap: '16px'
              }}>
                {recommendations.map((rec, i) => (
                  <RecommendationCard
                    key={rec.movie_id}
                    item={rec}
                    index={i}
                    userId={userId}
                    recommendationType={mode === 'hybrid' ? 'hybrid' : 'collaborative'}
                  />
                ))}
              </div>
            </motion.div>
          )}
        </div>
      </div>

      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}
