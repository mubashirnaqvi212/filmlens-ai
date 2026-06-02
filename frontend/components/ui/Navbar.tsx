'use client'
import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Film, Sparkles, Menu, X } from 'lucide-react'

export default function Navbar() {
  const pathname = usePathname()
  const [mobileOpen, setMobileOpen] = useState(false)

  const links = [
    { href: '/', label: 'Home' },
    { href: '/movies', label: 'Movies' },
    { href: '/recommendations', label: 'Recommendations' },
  ]

  return (
    <nav style={{
      position: 'fixed', top: 0, left: 0, right: 0, zIndex: 50,
      backgroundColor: 'rgba(20,20,20,0.95)',
      backdropFilter: 'blur(12px)',
      borderBottom: '1px solid #2a2a2a'
    }}>
      <div style={{
        maxWidth: '1280px', margin: '0 auto',
        padding: '0 48px', height: '64px',
        display: 'flex', alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        {/* Logo */}
        <Link href="/" style={{
          display: 'flex', alignItems: 'center',
          gap: '8px', textDecoration: 'none',
          fontWeight: 'bold', fontSize: '18px'
        }}>
          <div style={{
            padding: '6px', borderRadius: '8px',
            backgroundColor: '#e50914'
          }}>
            <Film style={{ width: '16px', height: '16px', color: 'white' }} />
          </div>
          <span style={{ color: 'white' }}>FilmLens</span>
          <span style={{ color: '#e50914' }}>AI</span>
        </Link>

        {/* Desktop links */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '32px' }}>
          {links.map(link => (
            <Link
              key={link.href}
              href={link.href}
              style={{
                fontSize: '14px', fontWeight: '500',
                textDecoration: 'none',
                color: pathname === link.href ? '#e50914' : '#a1a1aa',
                transition: 'color 0.2s'
              }}
            >
              {link.label}
            </Link>
          ))}
        </div>

        {/* AI Badge */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: '6px',
          padding: '6px 14px', borderRadius: '9999px',
          fontSize: '12px', fontWeight: '500',
          backgroundColor: '#450a0a', color: '#f87171',
          border: '1px solid #7f1d1d'
        }}>
          <Sparkles style={{ width: '12px', height: '12px' }} />
          SVD + TF-IDF
        </div>
      </div>
    </nav>
  )
}
