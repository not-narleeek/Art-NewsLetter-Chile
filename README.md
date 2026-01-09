# Newsletter Cultural Chile 🎨

Sistema de newsletter cultural para Chile - Versión personal con costo $0/mes.

## 🚀 Características

- ✅ Gestión de suscriptores con confirmación por email (double opt-in)
- ✅ CRUD completo de eventos culturales
- ✅ Generación y envío de newsletters
- ✅ Tracking de apertura de emails
- ✅ Panel de administración web
- ✅ Landing page responsive
- ✅ Base de datos SQLite (sin costo)
- ✅ Despliegue gratuito en Railway.app

## 📋 Requisitos

- Python 3.9+
- Cuenta de Gmail (para envío de emails)
- Cuenta de Railway.app (gratuita)

## 🛠️ Instalación Local

### 1. Clonar el repositorio

```bash
git clone <tu-repo>
cd Art-NewsLetter-Chile
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia `.env.example` a `.env` y configura:

```bash
cp ../.env.example .env
```

Edita `.env` con tus credenciales:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password  # Ver instrucciones abajo
FROM_EMAIL=tu-email@gmail.com
FROM_NAME=Newsletter Cultural Chile
BASE_URL=http://localhost:8000
```

**Cómo obtener App Password de Gmail:**
1. Ve a https://myaccount.google.com/security
2. Activa "Verificación en 2 pasos"
3. Ve a "Contraseñas de aplicaciones"
4. Genera una nueva para "Correo"
5. Copia la contraseña de 16 caracteres

### 5. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en:
- **Landing page:** http://localhost:8000
- **Admin panel:** http://localhost:8000/static/admin.html
- **API docs:** http://localhost:8000/docs

## 🧪 Testing

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=. --cov-report=html

# Solo tests rápidos
pytest -m "not slow" -v
```

## 🚢 Despliegue en Railway.app

### 1. Crear cuenta en Railway

Ve a https://railway.app y crea una cuenta gratuita.

### 2. Conectar repositorio

1. Click en "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Autoriza Railway y selecciona este repositorio

### 3. Configurar variables de entorno

En el dashboard de Railway, ve a "Variables" y agrega:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password
FROM_EMAIL=tu-email@gmail.com
FROM_NAME=Newsletter Cultural Chile
BASE_URL=https://tu-app.railway.app
```

### 4. Deploy automático

Railway detectará automáticamente el `railway.json` y desplegará la aplicación.

Tu app estará disponible en: `https://tu-app.railway.app`

## 📖 Uso

### Como administrador

1. Abre el panel admin: `https://tu-app.railway.app/static/admin.html`
2. Crea eventos culturales manualmente
3. Previsualiza el newsletter
4. Envía el newsletter a todos los suscriptores

### Como suscriptor

1. Visita la landing page
2. Ingresa tu email
3. Confirma la suscripción desde tu correo
4. Recibe newsletters mensuales

## 📁 Estructura del Proyecto

```
Art-NewsLetter-Chile/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── models.py           # Database models
│   ├── database.py         # Database connection
│   ├── email_service.py    # Email sending
│   ├── templates/          # Email templates
│   │   ├── confirmation.html
│   │   └── newsletter.html
│   ├── tests/              # Test suite
│   │   ├── conftest.py
│   │   ├── test_models.py
│   │   └── test_api.py
│   ├── requirements.txt
│   └── requirements-dev.txt
├── static/
│   ├── index.html          # Landing page
│   ├── admin.html          # Admin panel
│   ├── css/
│   │   ├── style.css
│   │   └── admin.css
│   └── js/
│       └── admin.js
├── railway.json            # Railway config
└── README.md
```

## 🎯 Roadmap (Opcional)

- [ ] Scraper automático de eventos (Chile Cultura)
- [ ] Filtros por región para suscriptores
- [ ] Estadísticas de engagement
- [ ] Programación de envíos
- [ ] Carga de imágenes

## 💰 Costos

- **Infraestructura:** $0 (Railway free tier)
- **Email:** $0 (Gmail SMTP, 500 emails/día)
- **Base de datos:** $0 (SQLite local)
- **Total:** **$0/mes**

## 📝 Licencia

Proyecto personal de código abierto.

## 🤝 Contribuciones

Este es un proyecto personal, pero sugerencias son bienvenidas vía issues.

---

Hecho con ❤️ en Chile
