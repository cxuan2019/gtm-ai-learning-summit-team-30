'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';

export default function HeaderComponent() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-black text-white px-6 py-4 flex items-center justify-between">
      <Link href="/" className="text-3xl font-display font-bold tracking-tighter">STORE</Link>
      
      {/* Desktop Menu */}
      <nav className="hidden md:flex gap-6 items-center text-sm font-medium">
        <Link href="/new" className="hover:text-gray-300 transition-colors">New Releases</Link>
        <Link href="/men" className="hover:text-gray-300 transition-colors">Men</Link>
        <Link href="/women" className="hover:text-gray-300 transition-colors">Women</Link>
        <Link href="/kids" className="hover:text-gray-300 transition-colors">Kids</Link>
        <Link href="/sale" className="text-red-500 hover:text-red-400 transition-colors focus:outline-none">Sale</Link>
      </nav>

      {/* Utilities */}
      <div className="flex items-center gap-4">
        {/* Jamal Personalized Greeting */}
        <div className="hidden sm:flex items-center gap-2 mr-2 border-r border-gray-800 pr-4">
          <span className="text-sm font-medium text-gray-300">Welcome, Jamal!</span>
          <div className="relative w-8 h-8 rounded-full overflow-hidden border border-gray-700">
            <Image
              src="/customer_3_1773176314089.png"
              alt="Jamal Reynolds"
              fill
              className="object-cover"
            />
          </div>
        </div>

        <button className="hidden md:block hover:opacity-70 transition-opacity uppercase text-sm font-medium">Search</button>
        <button className="hover:opacity-70 transition-opacity uppercase text-sm font-medium">Cart (0)</button>
        <button 
          className="md:hidden flex flex-col gap-1 p-1"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          aria-label="Toggle Menu"
        >
          <div className={`w-6 h-0.5 bg-white transition-transform ${isMenuOpen ? 'rotate-45 translate-y-1.5' : ''}`} />
          <div className={`w-6 h-0.5 bg-white transition-opacity ${isMenuOpen ? 'opacity-0' : ''}`} />
          <div className={`w-6 h-0.5 bg-white transition-transform ${isMenuOpen ? '-rotate-45 -translate-y-1.5' : ''}`} />
        </button>
      </div>

      {/* Mobile Menu Overlay */}
      {isMenuOpen && (
        <div className="absolute top-full left-0 w-full bg-black border-t border-gray-800 flex flex-col gap-4 p-6 md:hidden shadow-xl">
          <Link href="/new" className="text-lg">New Releases</Link>
          <Link href="/men" className="text-lg">Men</Link>
          <Link href="/women" className="text-lg">Women</Link>
          <Link href="/kids" className="text-lg">Kids</Link>
          <Link href="/sale" className="text-lg text-red-500">Sale</Link>
        </div>
      )}
    </header>
  );
}
