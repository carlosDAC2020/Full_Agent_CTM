# Magazine App

Plataforma inteligente para la generación automatizada de revistas y boletines informativos sobre convocatorias de financiación, tecnología y ciencia. El sistema utiliza **Agentes de IA** (LangGraph, Gemini) para curar contenido, extraer requisitos y generar documentos PDF de alta calidad, con un backend robusto en FastAPI.

## 📋 Características

-   **Búsqueda Inteligente**: Tavily + Brave para hallar información relevante.
-   **Procesamiento con IA**: Gemini (Google AI) con LangGraph para planificar, extraer y curar contenido.
-   **Generación de Magazine**: Creación de PDFs con portadas temáticas y diseño profesional.
-   **Extracción de Requisitos**: Análisis automático de URLs de convocatorias para extraer elegibilidad, montos y fechas.
-   **Backend Modular**: Arquitectura limpia basada en dominios con FastAPI, SQLAlchemy y Pydantic.
-   **Sistema de Tareas**: Procesamiento asíncrono con Celery y Redis para tareas de larga duración.
-   **Frontend Moderno**: UI con visor de PDF tipo flipbook, gestión de fuentes y carrito de convocatorias.
-   **Gestión de Fuentes**: CRUD de fuentes y descubrimiento asistido por IA (OSINT).
-   **Notificaciones**: Envío de magazines por correo electrónico.

---

## 🛠️ Tecnologías Principales

El backend está construido con un stack moderno y eficiente en Python:

-   **Framework Web**: [FastAPI](https://fastapi.tiangolo.com/)
-   **Base de Datos**: SQLite (Desarrollo) / SQLAlchemy (ORM)
-   **Asincronía & Background Tasks**:
    -   **Celery**: Procesamiento de tareas pesadas.
    -   **Redis**: Broker de mensajes y caché.
-   **Inteligencia Artificial**:
    -   **LangGraph / LangChain**: Orquestación.
    -   **Google Gemini**: Modelo de lenguaje (LLM).
    -   **Herramientas de Búsqueda**: Tavily, Brave Search.
-   **Seguridad**: OAuth2 con JWT.

---

## 🚀 Instalación y Ejecución

### 1. Prerrequisitos
-   Python 3.10+
-   Redis (para tareas asíncronas)
-   Claves de API: Google Gemini, Tavily, Brave.

### 2. Configuración
Crea un archivo `.env` en la raíz del proyecto (ver ejemplo en documentación anterior o `config.py`):
```env
GEMINI_API_KEY="..."
TAVILY_API_KEY="..."
REDIS_URL="redis://localhost:6379/0"
JWT_SECRET="..."
```

### 3. Instalación de Dependencias
```bash
python -m venv venv
# Activar entorno (Windows: venv\Scripts\activate, Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación

#### Opción A: Docker (Recomendado)
Docker Compose levantará la API, el Worker de Celery, Redis y PostgreSQL automáticamente.

1. Asegúrate de tener Docker instalado.
2. Crea el archivo `.env` (ver arriba).
3. Ejecuta:
   ```bash
   docker compose up --build
   ```
4. La API estará disponible en `http://localhost:8000`.

#### Opción B: Ejecución Local (Manual)

#### Servidor API
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Worker de Celery (para agentes)
```bash
celery -A backend.celery_app worker --loglevel=info --pool=solo
```

---
### 5. Migración de JSON a DB (Opcional)
```bash
docker compose exec magazine_api python -m backend.scripts.migrate_convocatorias
```


## 📂 Estructura del Proyecto

```text
magazine_app/
├── backend/
│   ├── app/                # Nueva estructura modular (Core, DB, Schemas, Services, API)
│   ├── fonts/              # Fuentes tipográficas
│   ├── agent/              # Definición del Grafo del Agente (LangGraph)
│   ├── celery_app.py       # Configuración de Celery
│   └── tasks.py            # Tareas asíncronas
├── assets/                 # Portadas e imágenes del PDF
├── img/                    # Iconos
├── frontend/               # Interfaz de usuario (HTML/JS/CSS)
├── outputs/                # Archivos generados (PDFs, JSONs)
└── README.md               # Este archivo
```

## 🔐 Endpoints Clave

La API está organizada en routers bajo `/api`:

-   **`/auth`**: Registro y login (JWT).
-   **`/magazines`**: Generación y listado de magazines.
-   **`/tasks`**: Gestión y monitoreo de tareas en segundo plano (SSE).
-   **`/sources`**: Gestión y búsqueda de fuentes de información.
-   **`/utils`**: Subida de archivos, visor y utilidades de correo.

---

*Para más detalles sobre el desarrollo del backend, consulta el código en `backend/app/`.*
