export default function Features() {
    return (
        <section style={{ padding: '80px 20px', background: '#fafafa' }}>
            <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
                <h2 style={{ textAlign: 'center', fontSize: '2rem', marginBottom: '60px' }}>¿Por qué suscribirte?</h2>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '40px' }}>
                    <FeatureCard
                        title="Curaduría Experta"
                        description="Nuestro equipo selecciona solo los eventos que valen la pena, filtrando el ruido."
                        emoji="🎨"
                    />
                    <FeatureCard
                        title="Agenda Mensual"
                        description="Recibe todo el primer día del mes. Planifica tus salidas culturales con tiempo."
                        emoji="📅"
                    />
                    <FeatureCard
                        title="Cobertura Nacional"
                        description="Eventos en Santiago, Valparaíso, Biobío y opciones online."
                        emoji="🇨🇱"
                    />
                </div>
            </div>
        </section>
    );
}

function FeatureCard({ title, description, emoji }: { title: string, description: string, emoji: string }) {
    return (
        <div style={{ background: 'white', padding: '30px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
            <div style={{ fontSize: '3rem', marginBottom: '20px' }}>{emoji}</div>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '10px' }}>{title}</h3>
            <p style={{ color: '#666', lineHeight: '1.6' }}>{description}</p>
        </div>
    );
}
