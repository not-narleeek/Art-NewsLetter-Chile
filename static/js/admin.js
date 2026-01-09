// Admin Panel JavaScript

// Load stats on page load
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadEvents();
});

// Load dashboard statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        document.getElementById('totalSubscribers').textContent = data.total_subscribers;
        document.getElementById('activeSubscribers').textContent = data.active_subscribers;
        document.getElementById('totalEvents').textContent = data.total_events;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load events list
async function loadEvents() {
    try {
        const response = await fetch('/api/events?limit=10');
        const data = await response.json();

        const eventsList = document.getElementById('eventsList');

        if (data.events.length === 0) {
            eventsList.innerHTML = '<p class="empty-state">No hay eventos aún. ¡Crea el primero!</p>';
            return;
        }

        eventsList.innerHTML = data.events.map(event => `
            <div class="event-card">
                <div class="event-header">
                    <h4>${event.title}</h4>
                    <span class="badge badge-${event.category}">${event.category}</span>
                </div>
                <p class="event-meta">
                    📅 ${new Date(event.start_date).toLocaleDateString('es-CL')}
                    ${event.region ? `| 📍 ${event.region}` : ''}
                </p>
                <p class="event-description">${event.description || 'Sin descripción'}</p>
                <div class="event-actions">
                    <button onclick="deleteEvent(${event.id})" class="btn-danger-sm">Eliminar</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading events:', error);
    }
}

// Handle event form submission
document.getElementById('eventForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const eventData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        category: document.getElementById('category').value,
        region: document.getElementById('region').value,
        start_date: document.getElementById('startDate').value,
        end_date: document.getElementById('endDate').value || null,
        venue: document.getElementById('venue').value,
        url: document.getElementById('url').value,
        image_url: document.getElementById('imageUrl').value
    };

    try {
        const response = await fetch('/api/events', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(eventData)
        });

        if (response.ok) {
            alert('✅ Evento creado exitosamente');
            document.getElementById('eventForm').reset();
            loadEvents();
            loadStats();
        } else {
            alert('❌ Error al crear evento');
        }
    } catch (error) {
        console.error('Error creating event:', error);
        alert('❌ Error al crear evento');
    }
});

// Delete event
async function deleteEvent(eventId) {
    if (!confirm('¿Estás seguro de eliminar este evento?')) {
        return;
    }

    try {
        const response = await fetch(`/api/events/${eventId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('✅ Evento eliminado');
            loadEvents();
            loadStats();
        } else {
            alert('❌ Error al eliminar evento');
        }
    } catch (error) {
        console.error('Error deleting event:', error);
        alert('❌ Error al eliminar evento');
    }
}

// Preview newsletter
async function previewNewsletter() {
    try {
        const response = await fetch('/api/newsletter/preview');
        const data = await response.json();

        const previewBox = document.getElementById('newsletterPreview');

        if (data.count === 0) {
            previewBox.innerHTML = '<p class="empty-state">No hay eventos para incluir en el newsletter</p>';
        } else {
            previewBox.innerHTML = `
                <h3>Vista Previa del Newsletter (${data.count} eventos)</h3>
                <div class="preview-events">
                    ${data.events.map(event => `
                        <div class="preview-event">
                            <strong>${event.title}</strong>
                            <span class="badge badge-${event.category}">${event.category}</span>
                            <p>${event.start_date}${event.region ? ` | ${event.region}` : ''}</p>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        previewBox.style.display = 'block';
    } catch (error) {
        console.error('Error previewing newsletter:', error);
        alert('❌ Error al generar vista previa');
    }
}

// Send newsletter
async function sendNewsletter() {
    if (!confirm('¿Estás seguro de enviar el newsletter a todos los suscriptores activos?')) {
        return;
    }

    try {
        const response = await fetch('/api/newsletter/send', {
            method: 'POST'
        });

        const data = await response.json();

        alert(`✅ Newsletter enviado!\n\nEnviados: ${data.sent}\nFallidos: ${data.failed}`);
    } catch (error) {
        console.error('Error sending newsletter:', error);
        alert('❌ Error al enviar newsletter');
    }
}
