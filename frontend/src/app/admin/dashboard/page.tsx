"use client";

import { useEffect, useState } from 'react';

interface Stats {
    subscribers: { total: number; active: number };
    events: { total: number; published: number; draft: number };
    newsletters: { total: number; sent: number };
}

export default function DashboardPage() {
    const [stats, setStats] = useState<Stats | null>(null);

    useEffect(() => {
        fetch('http://localhost:8000/api/v1/analytics/dashboard')
            .then(res => res.json())
            .then(data => setStats(data))
            .catch(err => console.error(err));
    }, []);

    if (!stats) return <div className="p-8">Cargando Dashboard...</div>;

    return (
        <div>
            <div className="page-header">
                <h1>Dashboard</h1>
            </div>

            <div className="grid grid-cols-3 gap-6" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
                <div className="card" style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
                    <h3 style={{ margin: '0 0 10px 0', color: '#666', fontSize: '0.9rem', textTransform: 'uppercase' }}>Suscriptores</h3>
                    <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#333' }}>{stats.subscribers.total}</div>
                    <div style={{ color: '#0070f3' }}>{stats.subscribers.active} Activos</div>
                </div>

                <div className="card" style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
                    <h3 style={{ margin: '0 0 10px 0', color: '#666', fontSize: '0.9rem', textTransform: 'uppercase' }}>Eventos</h3>
                    <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#333' }}>{stats.events.total}</div>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <span style={{ color: 'green' }}>{stats.events.published} Publicados</span>
                        <span style={{ color: 'orange' }}>{stats.events.draft} Borradores</span>
                    </div>
                </div>

                <div className="card" style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
                    <h3 style={{ margin: '0 0 10px 0', color: '#666', fontSize: '0.9rem', textTransform: 'uppercase' }}>Newsletters</h3>
                    <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#333' }}>{stats.newsletters.total}</div>
                    <div style={{ color: '#666' }}>{stats.newsletters.sent} Enviados</div>
                </div>
            </div>

            <div style={{ marginTop: '40px' }}>
                <h2>Accesos Rápidos</h2>
                <div style={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
                    <a href="/admin/events/create" className="btn btn-primary" style={{ textDecoration: 'none', background: '#0070f3', color: 'white', padding: '15px 30px', borderRadius: '6px' }}>
                        + Nuevo Evento
                    </a>
                    <a href="/admin/newsletters/create" className="btn" style={{ textDecoration: 'none', background: '#333', color: 'white', padding: '15px 30px', borderRadius: '6px' }}>
                        Crear Newsletter
                    </a>
                </div>
            </div>
        </div>
    );
}
