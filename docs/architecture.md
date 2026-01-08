# Arquitectura del Sistema - Art Newsletter Chile

## Diagrama de Contexto (Nivel 1)
Describe las interacciones del sistema con usuarios y sistemas externos.

```mermaid
C4Context
    title Diagrama de Contexto del Sistema

    Person(subscriber, "Suscriptor", "Usuario que recibe el newsletter")
    Person(curator, "Curador/Admin", "Gestiona eventos y newsletters")

    System(art_system, "Art Newsletter System", "Plataforma de gestión de eventos y envío de newsletters")

    System_Ext(email_provider, "Email Service Provider", "SendGrid/SES para envío de correos")
    System_Ext(chile_cultura, "Chile Cultura / Fuentes", "Sitios web de eventos culturales")
    System_Ext(social_media, "Instagram API", "Fuente de eventos de redes sociales")

    Rel(subscriber, art_system, "Se suscribe, gestiona preferencias", "HTTPS")
    Rel(curator, art_system, "Administra eventos, crea newsletters", "HTTPS")
    Rel(art_system, email_provider, "Envía correos transaccionales y masivos", "API")
    Rel(art_system, chile_cultura, "Extrae eventos (Scraping)", "HTTPS")
    Rel(art_system, social_media, "Extrae eventos (API)", "HTTPS")
    Rel(email_provider, subscriber, "Envía newsletter", "SMTP")
```

## Diagrama de Contenedores (Nivel 2)
Muestra las aplicaciones y bases de datos principales.

```mermaid
C4Container
    title Diagrama de Contenedores

    Person(admin, "Admin", "Gestiona contenido")
    Person(user, "User", "Se suscribe")

    Container(spa, "Web App (Frontend)", "Next.js / React", "Interfaz de administración y Landing Page")
    Container(api, "API Gateway / Backend", "FastAPI / Python", "Lógica de negocio, gestión de usuarios y eventos")
    Container(worker, "Worker", "Celery / Python", "Procesamiento de tareas asíncronas (envío emails, scraping)")
    
    ContainerDb(db, "Database", "PostgreSQL", "Almacena usuarios, eventos, configuración")
    ContainerDb(redis, "Cache & Queue", "Redis", "Broker de mensajes y caché de sesiones")

    Rel(user, spa, "Visita", "HTTPS")
    Rel(admin, spa, "Administra", "HTTPS")
    Rel(spa, api, "Llama API", "JSON/HTTPS")
    
    Rel(api, db, "Lee/Escribe", "SQL")
    Rel(api, redis, "Encola tareas", "Redis Protocol")
    Rel(worker, redis, "Consume tareas", "Redis Protocol")
    Rel(worker, db, "Lee/Escribe", "SQL")
```

## Diagrama de Componentes (Backend) (Nivel 3)
Detalle de componentes internos de la API.

```mermaid
C4Component
    title Diagrama de Componentes - API Backend

    Container(api, "API Application", "FastAPI")

    Component(auth_controller, "Auth Controller", "FastAPI Router", "Maneja login y tokens")
    Component(event_controller, "Event Controller", "FastAPI Router", "CRUD de eventos")
    Component(sub_controller, "Subscriber Controller", "FastAPI Router", "Gestión de suscripciones")

    Component(auth_service, "Auth Service", "Service", "Lógica de autenticación")
    Component(event_service, "Event Service", "Service", "Lógica de negocio de eventos")
    Component(sub_service, "Subscriber Service", "Service", "Lógica de suscripción y validación")

    Component(repo_event, "Event Repository", "SQLAlchemy", "Acceso a datos de eventos")
    Component(repo_user, "User Repository", "SQLAlchemy", "Acceso a datos de usuarios")

    Rel(api, auth_controller, "Route")
    Rel(api, event_controller, "Route")
    Rel(api, sub_controller, "Route")

    Rel(auth_controller, auth_service, "Uses")
    Rel(event_controller, event_service, "Uses")
    Rel(sub_controller, sub_service, "Uses")

    Rel(event_service, repo_event, "Uses")
    Rel(sub_service, repo_user, "Uses")
```
