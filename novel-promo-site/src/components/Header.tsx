"use client";

import Link from "next/link";
import { useState, useEffect } from "react";

export default function Header() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 w-full z-50 transition-all duration-500 ${
        scrolled
          ? "glass-strong shadow-lg shadow-black/20"
          : "bg-transparent"
      }`}
    >
      <nav className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-rose-500 to-purple-600 flex items-center justify-center shadow-lg shadow-rose-500/20 group-hover:shadow-rose-500/40 transition-shadow">
            <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
            </svg>
          </div>
          <span className="font-bold text-lg tracking-wide">
            <span className="text-gradient-rose">NC</span>
            <span className="text-white/90"> Story</span>
          </span>
        </Link>

        {/* Desktop nav */}
        <div className="hidden md:flex items-center gap-1">
          <NavLink href="/">หน้าแรก</NavLink>
          <NavLink href="/blog">บทความ</NavLink>
          <Link
            href="/novels/pantanakan-rattikan"
            className="ml-3 px-5 py-2 rounded-full bg-gradient-to-r from-rose-600 to-purple-600 text-white text-sm font-medium hover:from-rose-500 hover:to-purple-500 transition-all shadow-lg shadow-rose-500/20 hover:shadow-rose-500/30"
          >
            อ่านนิยาย
          </Link>
        </div>

        {/* Mobile hamburger */}
        <button
          className="md:hidden text-white/80 p-2 hover:text-white transition-colors"
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle menu"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            {isOpen ? (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            ) : (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            )}
          </svg>
        </button>
      </nav>

      {/* Mobile menu */}
      <div
        className={`md:hidden overflow-hidden transition-all duration-300 ${
          isOpen ? "max-h-60 opacity-100" : "max-h-0 opacity-0"
        }`}
      >
        <div className="glass-strong px-4 py-4 space-y-1 border-t border-white/5">
          <MobileNavLink href="/" onClick={() => setIsOpen(false)}>หน้าแรก</MobileNavLink>
          <MobileNavLink href="/blog" onClick={() => setIsOpen(false)}>บทความ</MobileNavLink>
          <Link
            href="/novels/pantanakan-rattikan"
            className="block mt-3 text-center px-5 py-2.5 rounded-full bg-gradient-to-r from-rose-600 to-purple-600 text-white text-sm font-medium"
            onClick={() => setIsOpen(false)}
          >
            อ่านนิยาย
          </Link>
        </div>
      </div>
    </header>
  );
}

function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <Link
      href={href}
      className="relative px-4 py-2 text-white/60 hover:text-white text-sm font-medium transition-colors group"
    >
      {children}
      <span className="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-0.5 bg-gradient-to-r from-rose-500 to-purple-500 group-hover:w-2/3 transition-all duration-300 rounded-full" />
    </Link>
  );
}

function MobileNavLink({ href, onClick, children }: { href: string; onClick: () => void; children: React.ReactNode }) {
  return (
    <Link
      href={href}
      className="block px-4 py-2.5 text-white/70 hover:text-white hover:bg-white/5 rounded-lg transition-all text-sm"
      onClick={onClick}
    >
      {children}
    </Link>
  );
}
