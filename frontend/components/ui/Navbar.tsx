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
    <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-md border-b"
      style={{ backgroundColor: 'rgba(20,20,20,0.95)', borderColor: 'var(--border)' }}>
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 font-bold text-lg">
          <div className="p-1.5 rounded-lg bg-red-600">
            <Film className="w-4 h-4 text-white" />
          </div>
          <span className="text-white">FilmLens</span>
          <span className="text-red-500">AI</span>
        </Link>

        {/* Desktop links */}
        <div className="hidden md:flex items-center gap-6">
          {links.map(link => (
            <Link
              key={link.href}
              href={link.href}
              className={`text-sm font-medium transition-colors ${
                pathname === link.href
                  ? 'text-red-500'
                  : 'text-zinc-400 hover:text-white'
              }`}
            >
              {link.label}
            </Link>
          ))}
        </div>

        {/* AI Badge */}
        <div className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium bg-red-950 text-red-400 border border-red-900">
          <Sparkles className="w-3 h-3" />
          <span>SVD + TF-IDF</span>
        </div>

        {/* Mobile menu button */}
        <button
          className="md:hidden text-zinc-400 hover:text-white"
          onClick={() => setMobileOpen(!mobileOpen)}
        >
          {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden border-t px-4 py-4 flex flex-col gap-3"
          style={{ borderColor: 'var(--border)', backgroundColor: 'var(--background)' }}>
          {links.map(link => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMobileOpen(false)}
              className={`text-sm font-medium py-2 transition-colors ${
                pathname === link.href ? 'text-red-500' : 'text-zinc-400'
              }`}
            >
              {link.label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  )
}
