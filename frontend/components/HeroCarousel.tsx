import Image from 'next/image';
import Link from 'next/link';
import { Campaign } from '@/types';

export default function HeroCarousel({ campaigns }: { campaigns: Campaign[] }) {
  if (!campaigns || campaigns.length === 0) return null;
  
  const hero = campaigns[0]; // Assuming we display the first one for now

  return (
    <section className="relative w-full h-[80vh] min-h-[600px] flex items-center bg-black">
      <div className="absolute inset-0 z-0">
        <Image
          src={hero.imageUrl}
          alt={hero.title}
          fill
          priority
          className="object-cover opacity-60"
          sizes="100vw"
        />
      </div>
      
      <div className="relative z-10 p-8 md:p-16 max-w-[1440px] mx-auto w-full">
        <div className="max-w-3xl text-white">
          <h1 className="text-6xl md:text-8xl lg:text-9xl font-display font-bold mb-4 tracking-tighter leading-[0.85] text-shadow-lg drop-shadow-lg">
            {hero.title}
          </h1>
          <p className="text-xl md:text-3xl font-medium mb-10 max-w-2xl text-shadow drop-shadow-md">
            {hero.subtitle}
          </p>
          <Link 
            href={hero.ctaLink}
            className="inline-block bg-white text-black px-10 py-5 text-sm font-display font-bold tracking-[0.2em] uppercase hover:bg-gray-200 transition-colors"
          >
            {hero.ctaText}
          </Link>
        </div>
      </div>
    </section>
  );
}
