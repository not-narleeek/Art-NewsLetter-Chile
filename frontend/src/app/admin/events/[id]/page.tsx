"use client";

import { useEffect, useState, use } from 'react';
import { useRouter } from 'next/navigation';
import { Event } from '@/types/event';

export default function EditEventPage({ params }: { params: Promise<{ id: string }> }) {
    const router = useRouter();
    const { id: eventId } = use(params);

    const [event, setEvent] = useState<Partial<Event>>({});
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        if (!eventId || eventId === 'undefined') {
            alert("Error: ID del evento no válido. Volviendo...");
            router.push('/admin/events');
            return;
        }

        // Add console log for debug
        console.log("Fetching event:", eventId);

        fetch(`http://localhost:8000/api/v1/events/${eventId}`)
            .then(res => {
                if (!res.ok) throw new Error("Event not found");
                return res.json();
            })
            .then(data => {
                setEvent(data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                alert("Error cargando evento");
                router.push('/admin/events');
            });
    }, [eventId, router]);

    const handleChange = (field: string, value: any) => {
        setEvent(prev => ({ ...prev, [field]: value }));
    };

    const handleSave = async () => {
        setSaving(true);
        try {
            const res = await fetch(`http://localhost:8000/api/v1/events/${eventId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: event.title,
                    description: event.description,
                    start_date: event.start_date,
                    end_date: event.end_date,
                    category: event.category,
                    region: event.region,
                    external_url: event.external_url,
                    status: event.status,
                    slug: event.slug,
                    image_url: event.image_url
                })
            });

            if (res.ok) {
                alert("Evento actualizado correctamente");
                router.push('/admin/events');
            } else {
                alert("Error al guardar cambios");
            }
        } catch (err) {
            console.error(err);
            alert("Error de conexión");
        } finally {
            setSaving(false);
        }
    };

    if (loading) return <div>Cargando...</div>;

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            <div className="page-header">
                <h1>Editar Evento</h1>
                <button onClick={() => router.back()} className="btn" style={{ background: '#eee' }}>Volver</button>
            </div>

            <div className="form-group">
                <label className="form-label">Título</label>
                <input
                    className="form-input"
                    value={event.title || ''}
                    onChange={e => handleChange('title', e.target.value)}
                />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                <div className="form-group">
                    <label className="form-label">Fecha Inicio</label>
                    <input
                        type="datetime-local"
                        className="form-input"
                        value={event.start_date ? new Date(event.start_date).toISOString().slice(0, 16) : ''}
                        onChange={e => handleChange('start_date', e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">Estado</label>
                    <select
                        className="form-input"
                        value={event.status || 'draft'}
                        onChange={e => handleChange('status', e.target.value)}
                        style={{ borderColor: event.status === 'published' ? 'green' : '#ddd' }}
                    >
                        <option value="draft">Borrador (Draft)</option>
                        <option value="published">Publicado (Published)</option>
                        <option value="archived">Archivado</option>
                    </select>
                </div>
            </div>

            <div className="form-group">
                <label className="form-label">Descripción</label>
                <textarea
                    className="form-input"
                    rows={5}
                    value={event.description || ''}
                    onChange={e => handleChange('description', e.target.value)}
                />
            </div>

            <div className="form-group">
                <label className="form-label">URL Externa</label>
                <input
                    className="form-input"
                    value={event.external_url || ''}
                    onChange={e => handleChange('external_url', e.target.value)}
                />
            </div>

            <div className="form-group">
                <label className="form-label">Imagen URL</label>
                <input
                    className="form-input"
                    value={event.image_url || ''}
                    onChange={e => handleChange('image_url', e.target.value)}
                />
                {event.image_url && (
                    <img src={event.image_url} alt="Preview" style={{ marginTop: '10px', maxHeight: '200px', borderRadius: '4px' }} />
                )}
            </div>

            <div style={{ marginTop: '30px' }}>
                <button
                    onClick={handleSave}
                    className="btn btn-primary"
                    disabled={saving}
                    style={{ width: '100%', padding: '15px', fontSize: '1.1rem' }}
                >
                    {saving ? 'Guardando...' : 'Guardar Cambios y Publicar'}
                </button>
            </div>
        </div>
    );
}
