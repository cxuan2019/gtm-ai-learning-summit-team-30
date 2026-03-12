import ShoeGrid from '@/components/ShoeGrid';
import PersonalizedCarousel from '@/components/PersonalizedCarousel';
import { fetchMensShoes, JAMAL_CAROUSEL_IMAGES } from '@/lib/api';

export default async function MensPage() {
  const shoes = await fetchMensShoes();

  return (
    <div className="flex flex-col w-full">
      {/* Personalized Experience for Jamal */}
      <PersonalizedCarousel images={JAMAL_CAROUSEL_IMAGES} />

      {/* Grid Section */}
      <section className="py-16 px-4 md:px-8 max-w-[1440px] mx-auto w-full">
        <div className="flex justify-between items-end mb-8">
          <h2 className="text-2xl md:text-3xl font-display font-bold tracking-tighter">ALL STYLES</h2>
          <span className="text-sm font-medium text-gray-500">{shoes.length} Results</span>
        </div>

        <ShoeGrid products={shoes} />
      </section>
    </div>
  );
}
