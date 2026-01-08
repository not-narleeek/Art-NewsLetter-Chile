"use client";

import { useEffect, useState } from 'react';
import Link from 'next/link';

interface Newsletter {
    id: string;
    subject: string;
    status: string;
    created_at: string;
    sent_at?: string;
}

export default function NewslettersPage() {
    const [newsletters, setNewsletters] = useState<Newsletter[]>([]);
    const [loading, setLoading] = useState(true);

    async function fetchNewsletters() {
        try {
            const res = await fetch('http://localhost:8000/api/v1/newsletters/');
            if (res.ok) {
                const data = await res.json();
                setNewsletters(data);
            }
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    }

    async function sendNewsletter(id: string) {
        if (!confirm('¿Seguro que deseas enviar este newsletter a todos los suscriptores?')) return;

        try {
            const res = await fetch(`http://localhost:8000/api/v1/newsletters/${id}/send`, { method: 'POST' });
            if (res.ok) {
                alert('Envío iniciado');
                fetchNewsletters(); // Refresh
            } else {
                alert('Error al enviar');
            }
        } catch (err) {
            console.error(err);
        }
    }

    useEffect(() => {
        fetchNewsletters();
    }, []);

    return (
        <div>
            <div className="page-header">
                <h1>Newsletters</h1>
                <Link href="/admin/newsletters/create" className="btn btn-primary">
                    + Nuevo Newsletter
                </Link>
            </div>

            {loading ? (
                <p>Cargando...</p>
            ) : (
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>Asunto</th>
                            <th>Estado</th>
                            <th>Creado</th>
                            <th>Enviado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {newsletters.map(n => (
                            <tr key={n.id}>
                                <td>{n.subject}</td>
                                <td>
                                    <span className={`badge badge-${n.status.toLowerCase()}`}>
                                        {n.status}
                                    </span>
                                </td>
                                <td>{new Date(n.created_at).toLocaleDateString()}</td>
                                <td>{n.sent_at ? new Date(n.sent_at).toLocaleString() : '-'}</td>
                                <td>
                                    {n.status === 'draft' && (
                                        <button
                                            onClick={() => sendNewsletter(n.id)}
                                            className="btn-sm"
                                            style={{ marginRight: '10px', color: '#0070f3', cursor: 'pointer' }}
                                        >
                                            Enviar
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
