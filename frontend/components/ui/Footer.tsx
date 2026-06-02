import Link from 'next/link'
import { Film, GitBranch, Sparkles } from 'lucide-react'

export default function Footer() {
  return (
    <footer
      style={{
        backgroundColor: '#0a0a0a',
        borderTop: '1px solid #1f1f1f',
        paddingTop: '48px',
        paddingBottom: '32px',
      }}
    >
      <div
        style={{
          maxWidth: '1280px',
          margin: '0 auto',
          padding: '0 48px',
        }}
      >
        {/* Top section */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '2fr 1fr 1fr 1fr',
            gap: '48px',
            marginBottom: '48px',
          }}
        >
          {/* Brand */}
          <div>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                marginBottom: '16px',
              }}
            >
              <div
                style={{
                  padding: '6px',
                  borderRadius: '8px',
                  backgroundColor: '#e50914',
                }}
              >
                <Film style={{ width: '16px', height: '16px', color: 'white' }} />
              </div>

              <span style={{ color: 'white', fontWeight: 'bold', fontSize: '18px' }}>
                FilmLens <span style={{ color: '#e50914' }}>AI</span>
              </span>
            </div>

            <p
              style={{
                color: '#52525b',
                fontSize: '14px',
                lineHeight: '1.6',
                maxWidth: '280px',
              }}
            >
              AI-powered movie recommendations using SVD collaborative filtering and TF-IDF
              content analysis. Built as a full-stack portfolio project.
            </p>

            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                marginTop: '16px',
                padding: '6px 12px',
                backgroundColor: '#1c1c1c',
                borderRadius: '8px',
                border: '1px solid #2a2a2a',
                width: 'fit-content',
              }}
            >
              <Sparkles style={{ width: '12px', height: '12px', color: '#e50914' }} />
              <span style={{ fontSize: '12px', color: '#a1a1aa' }}>
                RMSE: 0.8727 · Precision@10: 74.5%
              </span>
            </div>
          </div>

          {/* Navigate */}
          <div>
            <h4 style={{ color: 'white', fontSize: '14px', fontWeight: '600', marginBottom: '16px' }}>
              Navigate
            </h4>

            {[
              { href: '/', label: 'Home' },
              { href: '/movies', label: 'Browse Movies' },
              { href: '/recommendations', label: 'Get Recommendations' },
            ].map((link) => (
              <div key={link.href} style={{ marginBottom: '10px' }}>
                <Link
                  href={link.href}
                  style={{
                    color: '#71717a',
                    fontSize: '14px',
                    textDecoration: 'none',
                  }}
                >
                  {link.label}
                </Link>
              </div>
            ))}
          </div>

          {/* ML Stack */}
          <div>
            <h4 style={{ color: 'white', fontSize: '14px', fontWeight: '600', marginBottom: '16px' }}>
              ML Stack
            </h4>

            {[
              'SVD Matrix Factorization',
              'TF-IDF Vectorization',
              'Cosine Similarity',
              'Hybrid Blending',
              'Precision@K Evaluation',
            ].map((item) => (
              <div key={item} style={{ marginBottom: '10px' }}>
                <span style={{ color: '#71717a', fontSize: '13px' }}>{item}</span>
              </div>
            ))}
          </div>

          {/* Tech Stack */}
          <div>
            <h4 style={{ color: 'white', fontSize: '14px', fontWeight: '600', marginBottom: '16px' }}>
              Tech Stack
            </h4>

            {[
              'Python + FastAPI',
              'scikit-surprise',
              'Next.js 15',
              'TypeScript',
              'SQLite + SQLAlchemy',
            ].map((item) => (
              <div key={item} style={{ marginBottom: '10px' }}>
                <span style={{ color: '#71717a', fontSize: '13px' }}>{item}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Bottom bar */}
        <div
          style={{
            borderTop: '1px solid #1f1f1f',
            paddingTop: '24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <p style={{ color: '#3f3f46', fontSize: '13px' }}>
            © 2026 FilmLens AI — Built with Python, FastAPI, and Next.js
          </p>

          <a
            href="https://github.com/mubashirnaqvi212/filmlens-ai"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              color: '#71717a',
              textDecoration: 'none',
              fontSize: '13px',
            }}
          >
            <GitBranch style={{ width: '14px', height: '14px' }} />
            View on GitHub
          </a>
        </div>
      </div>
    </footer>
  )
}