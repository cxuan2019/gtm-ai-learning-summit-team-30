export interface Product {
  id: string;
  name: string;
  price: number;
  imageUrl: string;
}

export interface Campaign {
  id: string;
  title: string;
  subtitle: string;
  ctaText: string;
  ctaLink: string;
  imageUrl: string;
}

export interface Category {
  id: string;
  name: string;
  athlete?: string;
  imageUrl: string;
}
