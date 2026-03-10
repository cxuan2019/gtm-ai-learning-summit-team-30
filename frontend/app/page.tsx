import HeroCarousel from '@/components/HeroCarousel';
import ShopBySport from '@/components/ShopBySport';
import { fetchHeroCampaigns, fetchSportsCategories } from '@/lib/api';

export default async function Home() {
  const [campaigns, sports] = await Promise.all([
    fetchHeroCampaigns(),
    fetchSportsCategories(),
  ]);

  return (
    <div className="flex flex-col gap-0 pb-0 w-full overflow-hidden">
      <HeroCarousel campaigns={campaigns} />
      <ShopBySport sports={sports} />
    </div>
  );
}
