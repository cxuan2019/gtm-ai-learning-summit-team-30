'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';

interface CarouselProps {
  images: string[];
}

export default function PersonalizedCarousel({ images }: CarouselProps) {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    // Auto-advance the carousel every 4 seconds
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 4000);
    return () => clearInterval(interval);
  }, [images.length]);

  if (!images || images.length === 0) return null;

  return (
    <section className="relative w-full h-[70vh] min-h-[500px] overflow-hidden bg-black flex items-center justify-center">
      {images.map((imgSrc, index) => (
        <div
          key={imgSrc}
          className={`absolute inset-0 transition-opacity duration-1000 ease-in-out ${index === currentIndex ? 'opacity-100 z-10' : 'opacity-0 z-0'
            }`}
        >
          <div className="relative w-full h-full max-w-5xl mx-auto flex items-center justify-center">
            <Image
              src={imgSrc}
              alt={`Personalized style ${index + 1}`}
              fill
              priority={index === 0}
              className="object-contain opacity-90"
              sizes="100vw"
            />
          </div>
        </div>
      ))}

      {/* Overlay Content */}
      <div className="relative z-20 text-center text-white px-4 max-w-4xl mx-auto flex flex-col items-center">
        <span className="bg-white/10 backdrop-blur-md px-4 py-1 rounded-full text-xs font-bold tracking-[0.2em] uppercase mb-6 border border-white/20">
          Curated For Jamal
        </span>
        <h2 className="text-5xl md:text-7xl font-display font-bold tracking-tighter drop-shadow-lg mb-4">
          YOUR SIGNATURE STYLE
        </h2>
        <p className="text-lg md:text-xl font-medium drop-shadow-md max-w-2xl text-gray-200">
          From the skatepark to the streets, we've hand-picked the freshest retro and performance gear to match your vibe.
        </p>
      </div>

      {/* Navigation Indicators */}
      <div className="absolute bottom-8 left-0 right-0 z-20 flex justify-center gap-3">
        {images.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentIndex(index)}
            className={`transition-all duration-300 rounded-full ${index === currentIndex
                ? 'w-8 h-2 bg-white'
                : 'w-2 h-2 bg-white/50 hover:bg-white/80'
              }`}
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>
    </section>
  );
}
