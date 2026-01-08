# Art Newsletter Chile 🎨🇨🇱

Plataforma integral para la gestión, curaduría y difusión automatizada de eventos culturales en Chile. Este proyecto permite agregar eventos de diversas fuentes (manuales y scrapers), curarlos mediante un panel de administración y difundirlos a través de newsletters mensuales personalizados.

## 🚀 Características

### 1. Gestión de Eventos (CMS)
- **CRUD Completo**: Creación, edición y archivado de eventos.
- **Categorización**: Clasificación por tipo (Arte, Música, Teatro) y Región.
- **Imágenes**: Soporte para subida de imágenes locales.

### 2. Motor de Newsletter
- **Constructor Visual**: Selección de eventos mediante interfaz "Wizard".
- **Plantillas Dinámicas**: Renderizado HTML con Jinja2.
- **Envío Asíncrono**: Procesamiento en background usando Celery y Redis.
- **Gestión de Suscriptores**: Sistema de Double Opt-in para registro seguro.

### 3. Automatización (Collector)
- **Extracción Automática**: Scrapers integrados (Chile Cultura simulado, Instagram Mock).
- **Pipeline de Normalización**: Detección de duplicados y creación de borradores para revisión.

### 4. Analítica
- **Dashboard**: Visualización de KPIs clave (Suscriptores Activos, Eventos Publicados, Newsletters Enviados).

### 5. Frontend Público (Landing Page)
- **Landing Page Optimizada**: Diseño moderno pensado en conversión.
- **SEO Técnico**: Metadatos Open Graph y optimización de rendimiento.

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Base de Datos**: PostgreSQL
- **ORM**: SQLAlchemy (Async)
- **Colas**: Celery + Redis
- **Scraping**: BeautifulSoup4 + httpx

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Lenguaje**: TypeScript
- **Estilos**: CSS Modules / Vanilla CSS

### Infraestructura
- **Contenedores**: Docker & Docker Compose
- **Email Testing**: Mailpit (SMTP Mock)

## 📦 Instalación y Ejecución

El proyecto está contenerizado para facilitar el despliegue local.

### Prerrequisitos
- Docker Engine & Docker Compose (v2)

### Pasos
1. **Clonar el repositorio**:
   ```bash
   git clone <repo-url>
   cd Art-NewsLetter-Chile
   ```

2. **Iniciar servicios**:
   ```bash
   docker compose up --build
   ```

3. **Aplicar migraciones de base de datos**:
   ```bash
   docker compose exec backend poetry run alembic upgrade head
   ```

## 🌐 Accesos

Una vez iniciados los contenedores, puedes acceder a los siguientes servicios:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Landing Page** | http://localhost:3000 | Sitio público para suscripción |
| **Admin Panel** | http://localhost:3000/admin | Gestión de eventos y newsletters |
| **API Docs** | http://localhost:8000/docs | Swagger UI del Backend |
| **Mailpit** | http://localhost:8025 | Bandeja de entrada simulada (Emails) |

## 🧪 Pruebas Comunes

### Crear un Newsletter
1. Accede al Admin Panel (`/admin`).
2. Ve a la sección **Eventos** y crea o asegúrate de tener eventos publicados.
3. Ve a **Newsletters** > **Crear**.
4. Selecciona los eventos y guarda el borrador.
5. Envía el newsletter y revisa **Mailpit** para ver el correo recibido.

### Ejecutar Scraping
1. Realiza una petición POST al endpoint de triggering:
   ```bash
   curl -X POST http://localhost:8000/api/v1/collector/run
   ```
2. Verifica en el Admin Panel (`/admin/events`) la aparición de nuevos eventos en estado borrador.

## 📁 Estructura del Proyecto

```
Art-NewsLetter-Chile/
├── backend/            # API FastAPI, Workers, Scraping
│   ├── app/
│   │   ├── api/        # Endpoints
│   │   ├── collector/  # Scrapers & Pipeline
│   │   ├── models/     # Modelos SQL
│   │   ├── services/   # Lógica de Negocio
│   │   └── templates/  # Email Templates (Jinja2)
├── frontend/           # Next.js App
│   ├── src/
│   │   ├── app/
│   │   │   ├── admin/  # Panel de Administración
│   │   │   └── components/
└── docker-compose.yml  # Orquestación de servicios
```
