import Image from 'next/image';
import Link from 'next/link';
import { Product } from '@/types';

export default function ShoeGrid({ products }: { products: Product[] }) {
  if (!products || products.length === 0) {
    return (
      <div className="py-20 text-center text-gray-500 font-medium">
        No footwear available at the moment.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-x-6 gap-y-12">
      {products.map((product) => (
        <Link 
          key={product.id} 
          href={`/shop/shoes/${product.id}`}
          className="group block"
        >
          <div className="relative aspect-square bg-gray-100 mb-4 overflow-hidden rounded-md">
            <Image
              src={product.imageUrl}
              alt={product.name}
              fill
              className="object-cover transition-transform duration-700 group-hover:scale-105"
              sizes="(max-width: 640px) 100vw, (max-width: 768px) 50vw, (max-width: 1024px) 33vw, 25vw"
            />
          </div>
          <div className="flex justify-between items-start gap-4">
            <div>
              <h3 className="font-medium text-black group-hover:text-gray-600 transition-colors">{product.name}</h3>
              <p className="text-gray-500 text-sm mt-1">Men's Shoes</p>
            </div>
            <span className="font-medium whitespace-nowrap">${product.price.toFixed(2)}</span>
          </div>
        </Link>
      ))}
    </div>
  );
}
