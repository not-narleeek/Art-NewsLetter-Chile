export default function Footer() {
    return (
        <footer style={{ background: '#111', color: '#888', padding: '60px 20px', textAlign: 'center' }}>
            <div style={{ marginBottom: '20px', color: 'white', fontWeight: 'bold' }}>Art Newsletter Chile</div>
            <p>&copy; {new Date().getFullYear()} Todos los derechos reservados.</p>
            <div style={{ marginTop: '20px', display: 'flex', gap: '20px', justifyContent: 'center' }}>
                <a href="/admin" style={{ color: '#555', textDecoration: 'none', fontSize: '0.9rem' }}>Admin Login</a>
            </div>
        </footer>
    );
}
