import { Metadata } from 'next';
import Hero from './components/landing/Hero';
import SubscriptionForm from './components/landing/SubscriptionForm';
import Features from './components/landing/Features';
import Footer from './components/landing/Footer';

export const metadata: Metadata = {
  title: 'Art Newsletter Chile | La mejor agenda cultural en tu correo',
  description: 'Recibe mensualmente una curaduría experta con los mejores eventos de arte, música, teatro y literatura en Chile. Suscríbete gratis.',
  openGraph: {
    title: 'Art Newsletter Chile',
    description: 'La cultura de Chile en tu bandeja de entrada. Curaduría mensual experta.',
    url: 'https://artnewsletter.cl',
    siteName: 'Art Newsletter Chile',
    locale: 'es_CL',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Art Newsletter Chile',
    description: 'La cultura de Chile en tu bandeja de entrada.',
  },
};

export default function Home() {
  return (
    <main style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Hero />
      <SubscriptionForm />
      <Features />
      <Footer />
    </main>
  );
}
