import type { Metadata } from 'next';
import { Roboto, Oswald } from 'next/font/google';
import './globals.css';
import HeaderComponent from '@/components/HeaderComponent';
import FooterComponent from '@/components/FooterComponent';

const roboto = Roboto({
  weight: ['400', '500', '700'],
  subsets: ['latin'],
  variable: '--font-roboto',
});

const oswald = Oswald({
  subsets: ['latin'],
  variable: '--font-oswald',
});

export const metadata: Metadata = {
  title: 'Campaign Store',
  description: 'E-Commerce Campaign Landing Page',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${roboto.variable} ${oswald.variable} font-sans antialiased flex flex-col min-h-screen bg-white text-black`}>
        <HeaderComponent />
        <main className="flex-grow">
          {children}
        </main>
        <FooterComponent />
      </body>
    </html>
  );
}
