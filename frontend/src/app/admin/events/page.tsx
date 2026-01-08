"use client";

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Event } from '@/types/event';

export default function EventsPage() {
    const [events, setEvents] = useState<Event[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // In a real app, use an env var for API URL
        fetch('http://localhost:8000/api/v1/events/')
            .then(res => res.json())
            .then(data => {
                setEvents(data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }, []);

    return (
        <div>
            <div className="page-header">
                <h1>Gestión de Eventos</h1>
                <Link href="/admin/events/create" className="btn btn-primary">
                    + Nuevo Evento
                </Link>
            </div>

            {loading ? (
                <p>Cargando eventos...</p>
            ) : (
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>Título</th>
                            <th>Fecha</th>
                            <th>Categoría</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {events.map(event => (
                            <tr key={event.id}>
                                <td>{event.title}</td>
                                <td>{new Date(event.start_date).toLocaleDateString()}</td>
                                <td>{event.category}</td>
                                <td>
                                    <span className={`badge badge-${event.status}`}>
                                        {event.status}
                                    </span>
                                </td>
                                <td>
                                    <button className="btn-sm">Editar</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
