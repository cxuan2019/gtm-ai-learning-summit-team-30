# SPEC.md: E-Commerce Campaign Landing Page (Next.js)

## 1. Project Overview
**Objective:** Develop a responsive, media-rich campaign landing page using **Next.js**. The application will fetch dynamic product and campaign data from an external backend API and will be containerized for deployment on **Google Cloud Run (GCP)**.
**Key Characteristics:** Server-Side Rendering (SSR) or Incremental Static Regeneration (ISR) for SEO and performance, bold typography, modular React components, and native CSS scroll-snapping.

## 2. Design System & Theming
* **Framework:** React / Next.js (App Router).
* **Styling:** Tailwind CSS (recommended for rapid UI development) or CSS Modules.
* **Typography:** 
    * **Headers (H1/H2):** Heavy, condensed sans-serif (e.g., Impact, Futura Condensed).
    * **Body:** Clean, legible sans-serif (e.g., Helvetica Neue, Roboto).
* **Color Palette:** High contrast (Black `#000000`, White `#FFFFFF`, Light Grey `#F5F5F5`).

## 3. Architecture & React Components

### 3.1 Global Layout (`app/layout.tsx`)
* **HeaderComponent:** Client component for interactive elements (mobile menu, cart drawer).
* **FooterComponent:** Static server component containing directory links and legal text.

### 3.2 Hero Carousel (`HeroCarousel.tsx`)
* **Data Fetching:** Fetches active hero campaign data from `/api/campaigns/hero`.
* **Features:** Next.js `next/image` with `priority={true}` for LCP optimization.

### 3.3 "Shop by Sport" Slider (`ShopBySport.tsx`)
* **Data Fetching:** Fetches sport categories from `/api/categories/sports`.
* **Behavior:** Client component using `useRef` for scroll container targeting and native CSS `scroll-snap-type` for performance.

### 3.4 API Integration Layer (`lib/api.ts`)
* **Implementation:** Standardized `fetch` wrappers for calling the external backend service.
* **Typing:** Strict TypeScript interfaces for expected API responses (e.g., `Product`, `Campaign`, `Category`).

## 4. Technical & Deployment Requirements
* **Performance:** 
    * Use `next/image` for all graphics to automatically handle WebP conversion, lazy loading, and responsive `srcset` generation.
    * Utilize Next.js caching and ISR (e.g., `revalidate: 3600`) to minimize load on the backend service while keeping content fresh.
* **Deployment (GCP Cloud Run):**
    * **Dockerized:** Application must include a multi-stage `Dockerfile` optimized for Next.js standalone output to minimize image size.
    * **Stateless:** The Cloud Run instance must be completely stateless. All persistent data lives in the backend API.
    * **Environment Variables:** Backend API URLs (`NEXT_PUBLIC_API_URL`, `API_SECRET_KEY`) managed via GCP Secret Manager and injected at runtime.

---

## 5. Component Code Example: `ShopBySport.tsx` (Next.js)

```tsx
'use client';

import { useRef, useEffect, useState } from 'react';
import Image from 'next/image';

interface SportCardProps {
  id: string;
  name: string;
  athlete: string;
  imageUrl: string;
}

export default function ShopBySport({ sports }: { sports: SportCardProps[] }) {
  const sliderRef = useRef<HTMLDivElement>(null);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(true);

  const checkScroll = () => {
    if (!sliderRef.current) return;
    const { scrollLeft, scrollWidth, clientWidth } = sliderRef.current;
    setCanScrollLeft(scrollLeft > 0);
    setCanScrollRight(scrollLeft < scrollWidth - clientWidth - 2);
  };

  useEffect(() => {
    checkScroll();
    window.addEventListener('resize', checkScroll);
    return () => window.removeEventListener('resize', checkScroll);
  }, []);

  const scroll = (direction: 'left' | 'right') => {
    if (!sliderRef.current) return;
    const card = sliderRef.current.firstElementChild as HTMLElement;
    const gap = 16; // 1rem gap
    const scrollAmount = card ? card.offsetWidth + gap : 300;
    
    sliderRef.current.scrollBy({
      left: direction === 'left' ? -scrollAmount : scrollAmount,
      behavior: 'smooth'
    });
  };

  return (
    <section className="py-12 px-4 max-w-[1440px] mx-auto">
      <div className="flex justify-between items-end mb-6">
        <h2 className="text-2xl font-medium">Shop by Sport</h2>
        <div className="hidden md:flex gap-2">
          <button 
            onClick={() => scroll('left')} 
            disabled={!canScrollLeft}
            className={`w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center transition-opacity ${!canScrollLeft ? 'opacity-30 cursor-not-allowed' : 'hover:bg-gray-200'}`}
          >
            &lt;
          </button>
          <button 
            onClick={() => scroll('right')} 
            disabled={!canScrollRight}
            className={`w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center transition-opacity ${!canScrollRight ? 'opacity-30 cursor-not-allowed' : 'hover:bg-gray-200'}`}
          >
            &gt;
          </button>
        </div>
      </div>

      <div 
        ref={sliderRef}
        onScroll={checkScroll}
        className="flex gap-4 overflow-x-auto snap-x snap-mandatory scrollbar-hide pb-4"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        {sports.map((sport) => (
          <a key={sport.id} href={`/sports/${sport.id}`} className="flex-none w-[85%] md:w-[calc(40%-1rem)] lg:w-[calc(30%-1rem)] snap-start relative block rounded overflow-hidden group">
            <div className="w-full aspect-[4/5] relative bg-gray-100 overflow-hidden">
              <Image 
                src={sport.imageUrl} 
                alt={sport.name} 
                fill 
                className="object-cover transition-transform duration-400 group-hover:scale-105"
                sizes="(max-width: 768px) 85vw, (max-width: 1024px) 40vw, 30vw"
              />
            </div>
            <div className="absolute bottom-0 left-0 w-full p-6 flex flex-col items-start gap-2 bg-gradient-to-t from-black/60 to-transparent">
              <span className="text-white font-medium text-shadow">{sport.athlete}</span>
              <span className="bg-white text-black px-4 py-2 rounded-full font-semibold text-sm transition-colors group-hover:bg-gray-200">
                Shop {sport.name}
              </span>
            </div>
          </a>
        ))}
      </div>
    </section>
  );
}