"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { EventStatus, EventCategory, EventRegion } from '@/types/event';

export default function CreateEventPage() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        setLoading(true);

        const formData = new FormData(e.currentTarget);

        // Add defaults if missing or handle file specifically
        try {
            const res = await fetch('http://localhost:8000/api/v1/events/', {
                method: 'POST',
                body: formData, // Auto-sets Content-Type to multipart/form-data
            });

            if (res.ok) {
                router.push('/admin/events');
            } else {
                alert('Error al crear evento');
            }
        } catch (err) {
            console.error(err);
            alert('Error de conexión');
        } finally {
            setLoading(false);
        }
    }

    return (
        <div>
            <div className="page-header">
                <h1>Nuevo Evento</h1>
            </div>

            <form onSubmit={handleSubmit} className="max-w-2xl bg-white p-6 rounded-lg shadow">
                <div className="form-group">
                    <label className="form-label">Título</label>
                    <input name="title" required className="form-input" />
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div className="form-group">
                        <label className="form-label">Fecha Inicio</label>
                        <input type="datetime-local" name="start_date" required className="form-input" />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Fecha Fin (Opcional)</label>
                        <input type="datetime-local" name="end_date" className="form-input" />
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div className="form-group">
                        <label className="form-label">Categoría</label>
                        <select name="category" className="form-select">
                            {Object.values(EventCategory).map(c => (
                                <option key={c} value={c}>{c}</option>
                            ))}
                        </select>
                    </div>
                    <div className="form-group">
                        <label className="form-label">Región</label>
                        <select name="region" className="form-select">
                            {Object.values(EventRegion).map(r => (
                                <option key={r} value={r}>{r}</option>
                            ))}
                        </select>
                    </div>
                </div>

                <div className="form-group">
                    <label className="form-label">Descripción</label>
                    <textarea name="description" className="form-textarea"></textarea>
                </div>

                <div className="form-group">
                    <label className="form-label">Imagen</label>
                    <input type="file" name="image" accept="image/*" className="form-input" />
                </div>

                <div className="form-group">
                    <label className="form-label">URL Externa</label>
                    <input name="external_url" type="url" className="form-input" />
                </div>

                <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? 'Guardando...' : 'Crear Evento'}
                </button>
            </form>
        </div>
    );
}
