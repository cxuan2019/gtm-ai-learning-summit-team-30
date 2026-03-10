'use client';

import { useRef, useEffect, useState } from 'react';
import Image from 'next/image';
import { Category } from '@/types';

export default function ShopBySport({ sports }: { sports: Category[] }) {
  const sliderRef = useRef<HTMLDivElement>(null);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(true);

  const checkScroll = () => {
    if (!sliderRef.current) return;
    const { scrollLeft, scrollWidth, clientWidth } = sliderRef.current;
    setCanScrollLeft(scrollLeft > 0);
    // Allow a small 2px margin of error for scroll comparison
    setCanScrollRight(scrollLeft < scrollWidth - clientWidth - 2);
  };

  useEffect(() => {
    // Check initial scroll state
    checkScroll();
    window.addEventListener('resize', checkScroll);
    return () => window.removeEventListener('resize', checkScroll);
  }, [sports]);

  const scroll = (direction: 'left' | 'right') => {
    if (!sliderRef.current) return;
    const card = sliderRef.current.firstElementChild as HTMLElement;
    const gap = 16; // 1rem gap as used in our layout
    const scrollAmount = card ? card.offsetWidth + gap : 300;
    
    sliderRef.current.scrollBy({
      left: direction === 'left' ? -scrollAmount : scrollAmount,
      behavior: 'smooth'
    });
  };

  return (
    <section className="py-16 px-4 md:px-8 max-w-[1440px] mx-auto w-full flex flex-col gap-8 overflow-hidden">
      <div className="flex justify-between items-end">
        <h2 className="text-4xl md:text-5xl font-display font-bold tracking-tighter">SHOP BY SPORT</h2>
        <div className="hidden md:flex gap-2">
          <button 
            onClick={() => scroll('left')} 
            disabled={!canScrollLeft}
            className={`w-12 h-12 rounded-full flex items-center justify-center transition-all ${!canScrollLeft ? 'opacity-30 bg-gray-100 cursor-not-allowed text-gray-400' : 'bg-black text-white hover:scale-105 shadow-md'}`}
            aria-label="Scroll left"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m15 18-6-6 6-6"/></svg>
          </button>
          <button 
            onClick={() => scroll('right')} 
            disabled={!canScrollRight}
            className={`w-12 h-12 rounded-full flex items-center justify-center transition-all ${!canScrollRight ? 'opacity-30 bg-gray-100 cursor-not-allowed text-gray-400' : 'bg-black text-white hover:scale-105 shadow-md'}`}
            aria-label="Scroll right"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m9 18 6-6-6-6"/></svg>
          </button>
        </div>
      </div>

      <div 
        ref={sliderRef}
        onScroll={checkScroll}
        className="flex gap-4 overflow-x-auto snap-x snap-mandatory pb-8 -mx-4 px-4 md:mx-0 md:px-0"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        <style jsx>{`
          div::-webkit-scrollbar {
            display: none;
          }
        `}</style>
        {sports.map((sport) => (
          <a key={sport.id} href={`/sports/${sport.id}`} className="flex-none w-[85%] md:w-[calc(40%-1rem)] lg:w-[calc(30%-1rem)] snap-start relative block rounded-xl overflow-hidden group">
            <div className="w-full aspect-[4/5] relative bg-gray-100 overflow-hidden">
              <Image 
                src={sport.imageUrl} 
                alt={sport.name} 
                fill 
                className="object-cover transition-transform duration-700 group-hover:scale-110"
                sizes="(max-width: 768px) 85vw, (max-width: 1024px) 40vw, 30vw"
              />
              <div className="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition-colors duration-500" />
            </div>
            <div className="absolute bottom-0 left-0 w-full p-8 flex flex-col items-start gap-3 bg-gradient-to-t from-black/80 via-black/40 to-transparent">
              {sport.athlete && (
                <span className="text-white/80 font-medium text-sm tracking-widest uppercase mb-1">{sport.athlete}</span>
              )}
              <h3 className="text-white font-display text-4xl font-bold tracking-tighter drop-shadow-md">{sport.name}</h3>
              <span className="bg-white text-black px-6 py-3 rounded-full font-bold text-sm tracking-widest uppercase transition-transform group-hover:-translate-y-1 shadow-lg mt-2 font-display">
                Shop {sport.name}
              </span>
            </div>
          </a>
        ))}
      </div>
    </section>
  );
}
