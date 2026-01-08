"use client";
import { useState } from 'react';

export default function SubscriptionForm() {
    const [email, setEmail] = useState('');
    const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setStatus('loading');

        try {
            const res = await fetch('http://localhost:8000/api/v1/subscribers/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });

            if (res.ok) {
                setStatus('success');
                setMessage('¡Genial! Revisa tu correo para confirmar tu suscripción.');
                setEmail('');
            } else {
                setStatus('error');
                const data = await res.json();
                setMessage(data.detail || 'Hubo un error al suscribirte.');
            }
        } catch (err) {
            setStatus('error');
            setMessage('Error de conexión. Inténtalo más tarde.');
        }
    };

    return (
        <section id="subscribe" style={{ padding: '80px 20px', background: 'white', textAlign: 'center' }}>
            <div style={{ maxWidth: '500px', margin: '0 auto' }}>
                <h2 style={{ fontSize: '2rem', marginBottom: '20px' }}>Únete a la comunidad de arte</h2>
                <p style={{ marginBottom: '30px', color: '#666' }}>
                    Sé parte de los más de 5,000 suscriptores que ya reciben nuestra agenda exclusiva.
                </p>

                {status === 'success' ? (
                    <div style={{
                        padding: '20px',
                        background: '#e6fffa',
                        color: '#008f75',
                        borderRadius: '8px',
                        border: '1px solid #b7eb8f'
                    }}>
                        {message}
                    </div>
                ) : (
                    <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px' }}>
                        <input
                            type="email"
                            required
                            placeholder="tu@correo.com"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                            style={{
                                flex: 1,
                                padding: '14px',
                                borderRadius: '8px',
                                border: '1px solid #ddd',
                                fontSize: '1rem'
                            }}
                        />
                        <button
                            type="submit"
                            disabled={status === 'loading'}
                            style={{
                                background: '#333',
                                color: 'white',
                                border: 'none',
                                padding: '14px 24px',
                                borderRadius: '8px',
                                fontSize: '1rem',
                                cursor: 'pointer',
                                fontWeight: '600'
                            }}
                        >
                            {status === 'loading' ? 'Enviando...' : 'Suscribirme'}
                        </button>
                    </form>
                )}

                {status === 'error' && (
                    <div style={{ marginTop: '15px', color: '#ff4d4f' }}>{message}</div>
                )}

                <p style={{ marginTop: '20px', fontSize: '0.8rem', color: '#999' }}>
                    Respetamos tu privacidad. Sin spam. Cancela cuando quieras.
                </p>
            </div>
        </section>
    );
}
