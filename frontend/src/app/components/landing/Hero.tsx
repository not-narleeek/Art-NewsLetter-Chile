import Link from 'next/link';
import Image from 'next/image';

export default function Hero() {
    return (
        <section style={{
            padding: '100px 20px',
            textAlign: 'center',
            background: 'linear-gradient(180deg, #fff 0%, #f4f6f8 100%)'
        }}>
            <h1 style={{
                fontSize: '3.5rem',
                fontWeight: '800',
                marginBottom: '20px',
                background: '-webkit-linear-gradient(45deg, #0070f3, #a033ff)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                lineHeight: '1.2'
            }}>
                La Cultura de Chile<br />en tu bandeja de entrada
            </h1>
            <p style={{ fontSize: '1.25rem', color: '#666', marginBottom: '40px', maxWidth: '600px', margin: '0 auto 40px' }}>
                Recibe mensualmente una curaduría experta con los mejores eventos de arte, música, teatro y literatura.
                <br /><strong>Sin spam, solo cultura.</strong>
            </p>

            <a href="#subscribe" style={{
                display: 'inline-block',
                background: '#0070f3',
                color: 'white',
                padding: '16px 32px',
                borderRadius: '50px',
                fontSize: '1.1rem',
                fontWeight: '600',
                textDecoration: 'none',
                boxShadow: '0 4px 14px 0 rgba(0,118,255,0.39)'
            }}>
                Suscribirme Gratis
            </a>
        </section>
    );
}
