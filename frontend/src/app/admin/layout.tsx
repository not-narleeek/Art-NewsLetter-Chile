import Link from 'next/link';
import './admin.css';

export default function AdminLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <div className="admin-container">
            <aside className="admin-sidebar">
                <div className="admin-logo">Art Newsletter Admin</div>
                <nav className="admin-nav">
                    <Link href="/admin/dashboard" className="nav-item">Dashboard</Link>
                    <Link href="/admin/events" className="nav-item">Eventos</Link>
                    <Link href="/admin/newsletters" className="nav-item">Newsletters</Link>
                    <Link href="/admin/subscribers" className="nav-item">Suscriptores</Link>
                    <Link href="/" className="nav-item">Ver Sitio</Link>
                </nav>
            </aside>
            <main className="admin-content">
                {children}
            </main>
        </div>
    )
}
