"use client";

import { useEffect, useState } from 'react';
import { Subscriber } from '@/types/subscriber';

export default function SubscribersPage() {
    const [subscribers, setSubscribers] = useState<Subscriber[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://localhost:8000/api/v1/subscribers/')
            .then(res => res.json())
            .then(data => {
                setSubscribers(data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }, []);

    const handleDelete = async (id: string) => {
        if (!confirm('¿Estás seguro de eliminar este suscriptor?')) return;

        try {
            const res = await fetch(`http://localhost:8000/api/v1/subscribers/${id}`, {
                method: 'DELETE'
            });

            if (res.ok) {
                setSubscribers(prev => prev.filter(s => s.id !== id));
            } else {
                alert('Error al eliminar suscriptor');
            }
        } catch (err) {
            console.error(err);
            alert('Error de conexión');
        }
    };

    return (
        <div>
            <div className="page-header">
                <h1>Gestión de Suscriptores</h1>
            </div>

            {loading ? (
                <p>Cargando suscriptores...</p>
            ) : (
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>Email</th>
                            <th>Estado</th>
                            <th>Confirmado</th>
                            <th>ID</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {subscribers.map(sub => (
                            <tr key={sub.id}>
                                <td>{sub.email}</td>
                                <td>
                                    <span className={`badge ${sub.is_active ? 'badge-published' : 'badge-draft'}`}>
                                        {sub.is_active ? 'Activo' : 'Pendiente'}
                                    </span>
                                </td>
                                <td>{sub.is_active ? 'Sí' : 'No'}</td>
                                <td>
                                    <small style={{ fontSize: '10px', color: '#999' }}>{sub.id}</small>
                                </td>
                                <td>
                                    <button
                                        onClick={() => handleDelete(sub.id)}
                                        className="btn-sm"
                                        style={{ background: '#ff4444', color: 'white', border: 'none', cursor: 'pointer' }}
                                    >
                                        Eliminar
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {subscribers.length === 0 && (
                            <tr>
                                <td colSpan={4} style={{ textAlign: 'center', padding: '20px' }}>
                                    No hay suscriptores registrados.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            )}
        </div>
    );
}
