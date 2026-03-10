import Link from 'next/link';

export default function FooterComponent() {
  return (
    <footer className="bg-gray-100 text-black py-12 px-6 mt-12 border-t border-gray-200">
      <div className="max-w-[1440px] mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <h3 className="text-2xl font-display font-medium mb-4">STORE</h3>
          <p className="text-sm text-gray-600 mb-6">
            Equipment and apparel engineered for elite performance. Designed to push boundaries.
          </p>
        </div>
        
        <div className="flex flex-col gap-2">
          <h4 className="font-bold mb-2 uppercase text-sm font-display tracking-widest">Shop</h4>
          <Link href="/shoes" className="text-sm text-gray-600 hover:text-black">Shoes</Link>
          <Link href="/clothing" className="text-sm text-gray-600 hover:text-black">Clothing</Link>
          <Link href="/accessories" className="text-sm text-gray-600 hover:text-black">Accessories</Link>
          <Link href="/new" className="text-sm text-gray-600 hover:text-black">New Arrivals</Link>
        </div>

        <div className="flex flex-col gap-2">
          <h4 className="font-bold mb-2 uppercase text-sm font-display tracking-widest">Support</h4>
          <Link href="/help" className="text-sm text-gray-600 hover:text-black">Get Help</Link>
          <Link href="/returns" className="text-sm text-gray-600 hover:text-black">Returns &amp; Exchanges</Link>
          <Link href="/shipping" className="text-sm text-gray-600 hover:text-black">Shipping</Link>
          <Link href="/contact" className="text-sm text-gray-600 hover:text-black">Contact Us</Link>
        </div>

        <div className="flex flex-col gap-2">
          <h4 className="font-bold mb-2 uppercase text-sm font-display tracking-widest">Company</h4>
          <Link href="/about" className="text-sm text-gray-600 hover:text-black">About Us</Link>
          <Link href="/careers" className="text-sm text-gray-600 hover:text-black">Careers</Link>
          <Link href="/sustainability" className="text-sm text-gray-600 hover:text-black">Sustainability</Link>
        </div>
      </div>
      
      <div className="max-w-[1440px] mx-auto border-t border-gray-300 mt-12 pt-6 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-gray-500">
        <p>&copy; {new Date().getFullYear()} E-Commerce Store. All Rights Reserved.</p>
        <div className="flex gap-4">
          <Link href="/privacy" className="hover:text-black">Privacy Policy</Link>
          <Link href="/terms" className="hover:text-black">Terms of Service</Link>
        </div>
      </div>
    </footer>
  );
}
