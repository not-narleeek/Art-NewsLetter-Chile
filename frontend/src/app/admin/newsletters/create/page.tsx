"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Event } from '@/types/event';

export default function CreateNewsletterPage() {
    const router = useRouter();
    const [events, setEvents] = useState<Event[]>([]);
    const [selectedEvents, setSelectedEvents] = useState<string[]>([]);
    const [subject, setSubject] = useState('');
    const [previewHtml, setPreviewHtml] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        // Fetch published events for selection
        // Filters ideally: status=published
        fetch('http://localhost:8000/api/v1/events/?status=published')
            .then(res => res.json())
            .then(data => setEvents(data))
            .catch(err => console.error(err));
    }, []);

    const toggleEvent = (id: string) => {
        setSelectedEvents(prev =>
            prev.includes(id) ? prev.filter(e => e !== id) : [...prev, id]
        );
    };

    const handlePreview = async () => {
        if (selectedEvents.length === 0) return alert("Selecciona eventos");

        try {
            const res = await fetch('http://localhost:8000/api/v1/newsletters/preview', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    subject,
                    event_ids: selectedEvents
                })
            });
            const html = await res.json();
            setPreviewHtml(html);
        } catch (err) {
            console.error(err);
        }
    };

    const handleSave = async () => {
        if (!subject) return alert("Ingresa un asunto");
        setLoading(true);
        try {
            const res = await fetch('http://localhost:8000/api/v1/newsletters/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    subject,
                    event_ids: selectedEvents,
                    preview_text: "Lo mejor de la cultura esta semana"
                })
            });
            if (res.ok) {
                router.push('/admin/newsletters');
            } else {
                alert("Error al guardar");
            }
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="grid grid-cols-2 gap-8" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
            <div>
                <div className="page-header">
                    <h1>Crear Newsletter</h1>
                </div>

                <div className="form-group">
                    <label className="form-label">Asunto del Correo</label>
                    <input
                        className="form-input"
                        value={subject}
                        onChange={e => setSubject(e.target.value)}
                        placeholder="Ej: Agenda Cultural - Enero 2024"
                    />
                </div>

                <h3>Seleccionar Eventos</h3>
                <div style={{ maxHeight: '400px', overflowY: 'auto', border: '1px solid #eee', padding: '10px', borderRadius: '4px' }}>
                    {events.map(event => (
                        <div key={event.id} style={{ marginBottom: '10px', padding: '10px', background: 'white', border: '1px solid #ddd', borderRadius: '4px', display: 'flex', gap: '10px' }}>
                            <input
                                type="checkbox"
                                checked={selectedEvents.includes(event.id)}
                                onChange={() => toggleEvent(event.id)}
                            />
                            <div>
                                <div style={{ fontWeight: 'bold' }}>{event.title}</div>
                                <div style={{ fontSize: '0.85rem', color: '#666' }}>{new Date(event.start_date).toLocaleDateString()}</div>
                            </div>
                        </div>
                    ))}
                </div>

                <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
                    <button onClick={handlePreview} className="btn" style={{ background: '#333', color: 'white' }}>Generar Vista Previa</button>
                    <button onClick={handleSave} className="btn btn-primary" disabled={loading}>{loading ? 'Guardando...' : 'Guardar Borrador'}</button>
                </div>
            </div>

            <div style={{ background: '#fff', border: '1px solid #ddd', padding: '20px', minHeight: '600px' }}>
                <h3>Vista Previa</h3>
                {previewHtml ? (
                    <iframe
                        srcDoc={previewHtml}
                        style={{ width: '100%', height: '100%', border: 'none', minHeight: '500px' }}
                        title="Preview"
                    />
                ) : (
                    <div style={{ color: '#999', textAlign: 'center', marginTop: '100px' }}>
                        Selecciona eventos y genera una vista previa
                    </div>
                )}
            </div>
        </div>
    );
}
