# 🎨 Magazine Generator

Aplicación inteligente que genera revistas automáticas sobre cualquier tema utilizando LangGraph, Gemini AI y herramientas de búsqueda web. Ahora con soporte para gestión de convocatorias y configuración de notificaciones por correo electrónico.

## 📋 Características

- **Búsqueda Inteligente**: Tavily + Brave (vía herramientas del agente) para hallar información relevante
- **Procesamiento con IA**: Gemini (Google AI) con LangGraph para planificar, extraer y curar contenido
- **Generación de Magazine en PDF**: Creación de PDF con portadas temáticas y tarjetas por convocatoria/evento
- **Extracción de requisitos**: `GET /requirements/{id}` descarga la página original y resume requisitos con IA
- **API REST**: Backend FastAPI con CORS habilitado y estáticos en `/outputs` y `/frontend`
- **Frontend Moderno**: UI con botones flotantes, carrito enumerado y visor tipo flipbook en `/viewer`
- **PDF por selección**: `POST /generate_pdf_from_ids` a partir de IDs guardados en `outputs/convocatorias.json`
- **Fuentes administrables**: CRUD de `outputs/sources.json` y búsquedas asistidas por IA (`/sources/search`, `/sources/ai_search`)
- **Email de magazines**: Configuración y envío de PDFs por correo (`/email_settings`, `/send_email`) y subida de PDF (`/upload_pdf`)

## 🏗️ Estructura del Proyecto

```
magazine_app/
├── backend/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── state.py         # Estado del grafo LangGraph
│   │   ├── tools.py         # Herramientas (Tavily, Brave)
│   │   ├── nodes.py         # Nodos del grafo (funciones)
│   │   └── graph.py         # Definición del grafo
│   ├── Roboto-*.ttf         # Fuentes usadas en el PDF
│   ├── __init__.py
│   ├── main_api.py          # Servidor API FastAPI + endpoints de PDF/flipbook/email/sources
│   └── run_agent_local.py   # Script para pruebas locales del agente
├── assets/                  # Portadas del PDF (inicio, secciones, cierre)
├── img/                     # Íconos usados en el PDF (logo, secciones)
├── frontend/
│   ├── index.html           # Interfaz principal
│   ├── viewer.html          # Visor básico de PDF servido en /viewer
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── main.js
│       ├── email.js
│       ├── savedMagazines.js
│       └── organizer.js
├── outputs/
│   ├── uploads/             # PDFs subidos vía /upload_pdf
│   ├── convocatorias.json   # Almacenamiento de convocatorias
│   ├── email_settings.json  # Configuración de correo
│   ├── sources.json         # Fuentes de Investigación
│   └── magazine_*.pdf       # Magazines generados
├── .env                     # Claves de API (no incluido en git)
├── requirements.txt         # Dependencias Python
└── README.md                # Este archivo
```

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd magazine_app
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar variables de entorno (.env)

Crea un archivo `.env` en la raíz del proyecto con al menos:

```env
# Claves de IA
GEMINI_API_KEY="tu_clave_de_api_de_google_aqui"
TAVILY_API_KEY="tu_clave_de_api_de_tavily_aqui"
BRAVE_API_KEY="tu_clave_de_api_de_brave_aqui"

# Tema por defecto (opcional)
DEFAULT_TOPIC="convocatorias de financiación nacionales e internacionales y eventos en ciencia, tecnología e IA para startups"

# Redis (cola de tareas)
REDIS_URL=redis://localhost:6379/0

# SMTP para notificaciones (email de finalización de flujos)
SMTP_HOST="smtp.tudominio.com"
SMTP_PORT=587
SMTP_TLS=true
SMTP_USER="tu_email@dominio.com"
SMTP_PASS="tu_contraseña"
TEST_EMAIL="destinatario_pruebas@dominio.com"

# Modo demo de email (si true, guarda .eml en outputs/sent_emails/)
DEMO_MODE=false

# Auth/DB
JWT_SECRET="un_secreto_largo_y_aleatorio"
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL la inyecta Compose a los contenedores ("postgresql+psycopg2://mag_user:mag_pass@postgres:5432/mag_db")
```


1) Requisitos

- Docker Desktop (Windows/macOS) o Docker Engine (Linux)

2) Variables de entorno (.env)

3) Levantar todo

```
docker compose up --build
```

Esto iniciará:
- `postgres` (datos en volumen `pg-data`)
- `redis`
- `api` en `http://localhost:8000`
- `worker` (Celery) escuchando `flows`

4) Migraciones de BD (opcional, recomendado)

La API crea tablas automáticamente en el primer arranque. Para usar Alembic:

```
docker compose exec api alembic upgrade head
```

5) Frontend y autenticación

- Abre `http://localhost:8000/frontend/index.html`.
- Regístrate e inicia sesión desde el botón "Iniciar sesión" (modal). El token se guarda en `localStorage` y se envía automáticamente.
- Genera un magazine (protegido): el PDF se registrará en tu usuario.

6) Probar endpoints protegidos

```
# Obtener perfil
curl -H "Authorization: Bearer <token>" http://localhost:8000/auth/me

# Crear tarea magazine
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"type":"magazine","payload":{}}'

# Listar mis PDFs
curl -H "Authorization: Bearer <token>" http://localhost:8000/magazines
```

## 🔧 Cómo Funciona

### Flujo del Agente LangGraph

```
1. Planificador → Genera consultas de búsqueda
2. Búsqueda → Busca información en la web (Tavily)
3. Extracción → Extrae datos estructurados
4. Curación → Crea resúmenes atractivos
5. Generador → Crea PDF del magazine
```

### Endpoints de la API

- `GET /`
  - Estado básico de la API.

- V2 Flujos en background (recomendado para UI)
  - `POST /tasks` → crea una tarea de flujo: `{ "type": "magazine" | "requisitos" | "fuentes", "payload": {...} }`
  - `GET /tasks?status=active` → lista tareas activas para rehidratación de UI
  - `GET /tasks/{id}` → estado de una tarea `{ id, type, status, progress?, message?, result? }`
  - `GET /tasks/stream` → SSE global con eventos: `task_started`, `task_progress`, `task_succeeded`, `task_failed`

- (Compat) `POST /generate`
  - Aún disponible, pero en la UI ya se usa `/tasks` para ejecución en background.

- `GET /viewer`
  - Sirve el visor tipo flipbook (`frontend/viewer.html`) que renderiza el PDF como páginas pasables. Usar con query `?file=/outputs/xxx.pdf`.

- `POST /generate_pdf_from_ids`
  - Genera un PDF con tarjetas a partir de IDs existentes en `outputs/convocatorias.json`.
  - Request body:
    ```json
    { "ids": [1, 2, 3] }
    ```
  - Respuesta:
    ```json
    { "status": "success", "pdf_url": "/outputs/selected_1731352367.pdf", "viewer_url": "/viewer?file=/outputs/selected_1731352367.pdf" }
    ```

- `GET /requirements/{item_id}`
  - Extrae requisitos a partir de la URL original (y PDFs enlazados) del item ID en `outputs/convocatorias.json`.
  - Respuesta: `{ "id": <n>, "requirements": ["..."], "sources": ["url", ...], "saved": true }`

- `GET /sources`
  - Lista todas las fuentes.

- `POST /sources`
  - Crea una fuente.
  - Body:
    ```json
    { "name": "Colciencias", "type": "Nacional", "url": "https://..." }
    ```

- `PUT /sources/{source_id}`
  - Actualiza nombre/tipo/url/hidden de una fuente.
  - Body (parcial):
    ```json
    { "name": "Nuevo nombre", "hidden": true }
    ```

- `PATCH /sources/{source_id}/toggle`
  - Alterna `hidden` de una fuente.

- `DELETE /sources/{source_id}`
  - Elimina una fuente.

- `POST /sources/search`
  - Busca posibles fuentes en la web y marca si ya existen en `outputs/sources.json`.

- `POST /sources/ai_search`
  - Genera consultas con LLM, busca fuentes y marca las existentes vs nuevas.

- `GET /email_settings`
  - Devuelve configuración de correo: `{ sender_email, favorite_emails }`.

- `POST /email_settings`
  - Guarda `{ sender_email?, favorite_emails? }`.

- `POST /send_email`
  - Envía correo con asunto, cuerpo y/o PDF adjunto (ruta en `outputs/` o URL). Requiere SMTP en `.env`.

- `POST /upload_pdf`
  - Sube un PDF y lo almacena en `outputs/uploads/`. Responde con ruta relativa para usar en `/send_email`.

Notas:
- Archivos estáticos expuestos en `/outputs`.
- CORS abierto por defecto en desarrollo (`allow_origins=["*"]`).

#### Ejemplos rápidos (curl)

```bash
# Crear tarea de magazine (background)
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"type":"magazine","payload":{"tema":"convocatorias sobre IA para startups"}}'

# Generar PDF desde IDs
curl -X POST http://localhost:8000/generate_pdf_from_ids \
  -H "Content-Type: application/json" \
  -d '{"ids":[1,2,3]}'

# CRUD de fuentes
curl http://localhost:8000/sources
```

## 🛠️ Personalización

### Modificar el Modelo de IA

En `backend/agent/nodes.py`:

```python
_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=_api_key)
```

### Cambiar el Diseño del Magazine

En `backend/agent/nodes.py`, función `nodo_generador_magazine()`:

```python
# Personaliza colores, fuentes, tamaños, etc.
img = Image.new('RGB', (800, 1100), color=(255, 255, 255))
```

### Ajustar Número de Resultados

En `backend/agent/tools.py`:

```python
tavily_tool = TavilySearchResults(max_results=1)  # Cambia el número
```


### Email y Adjuntos

- Configura credenciales SMTP en `.env` (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USERNAME`, `EMAIL_PASSWORD`, `DEFAULT_SENDER_EMAIL`).
- Sube un PDF con `/upload_pdf` o usa uno generado en `outputs/` y llama `/send_email`.


## 🐛 Solución de Problemas

### Error: "No module named 'langchain'"

```bash
pip install -r requirements.txt
```

### Error: "GEMINI_API_KEY not found"

Asegúrate de que el archivo `.env` existe y contiene tus claves de API.

Además, cuando ejecutes desde la carpeta `backend/`, este proyecto ya carga `.env` desde la raíz automáticamente tanto en `main_api.py` como en `run_agent_local.py`.

### Error: "Did not find tavily_api_key"

Asegúrate de que `TAVILY_API_KEY` esté en tu `.env` y que hayas instalado las dependencias. Si ves una advertencia de deprecación, instala y usa `langchain-tavily`:

```bash
pip install langchain-tavily
```

### Error: "Port 8000 already in use"

Cambia el puerto en `main_api.py`:

```python
uvicorn.run(api, host="0.0.0.0", port=8001)  # Usa otro puerto
```


### Problemas al enviar correo

- Verifica credenciales SMTP y puertos.
- Asegura que el adjunto exista en `outputs/` o que la URL sea accesible.

## 🔷 Diagrama de flujo (alto nivel)

```mermaid
flowchart TD
  U[Usuario (UI)] -->|1. Gestiona fuentes| S1[Ver fuentes]
  U -->|1a. Buscar con IA| SAI[POST /sources/ai_search]
  U -->|1b. Buscar textos| SS[POST /sources/search]
  U -->|1c. CRUD manual| SCRUD[GET/POST/PUT/PATCH/DELETE /sources]
  S1 --> SD[sources.json]

  U -->|2. Generar magazine| G[POST /generate]
  G -->|LLM + Web| A[Agente LangGraph]
  A -->|Curado + extracción| CJ[(convocatorias.json)]
  G -->|Respuesta| GRES{pdf_url<br/>contenido_curado}
  GRES -->|contenido_curado| V1[3. Ver convocatorias extraídas]
  V1 --> F[3a. Filtros UI (fecha, tipo, keywords)]
  CJ --> V2[3b. Ver "todas" desde dataset]

  U -->|4. Ver requisitos| RQ[GET /requirements/{id}]
  RQ -->|Descarga página y enlaza PDFs| RQ2[Parseo + LLM]
  RQ2 -->|Graba requisitos| CJ

  U -->|5. Añadir al carrito| CARR[UI Carrito]
  CARR -->|ids[]| PDFGEN[POST /generate_pdf_from_ids]
  PDFGEN -->|Genera PDF| PDF[(outputs/magazine_*.pdf)]
  PDFGEN -->|viewer_url| VIEWER[/viewer?file=/outputs/*.pdf/]
  PDFGEN -->|pdf_url| PDFURL([/outputs/*.pdf])

  U -->|6. Abrir PDFs| PDFURL
  U -->|6. Ver flipbook| VIEWER

  U -->|7. Enviar correo| MAIL[POST /send_email]
  MAIL -->|Adjunto PDF + destinatarios| SMTP[(SMTP)]
  U -->|7a. Configurar correo| MCONF[GET/POST /email_settings]
  MCONF -->|Guardar| ESET[(email_settings.json)]

  SCRUD --> SD
  SAI --> SD
  SS --> SD
```

## 🔶 Diagrama de secuencia (resumen)

```mermaid
sequenceDiagram
  participant UI as Usuario (UI)
  participant API as Backend FastAPI
  participant DS as JSONs (sources, convocatorias, email)
  participant LLM as Agente/LLM + Web

  UI->>API: GET/POST/PUT/PATCH/DELETE /sources
  API->>DS: Actualiza sources.json

  UI->>API: POST /generate (tema?)
  API->>LLM: Flujo búsqueda+curado
  LLM-->>API: contenido_curado + (pdf_path?)
  API->>DS: Actualiza convocatorias.json
  API-->>UI: { pdf_url?, contenido_curado }

  UI->>API: GET /requirements/{id}
  API->>LLM: Parseo página + LLM
  LLM-->>API: { requirements: [...] }
  API->>DS: Guarda requisitos en convocatorias.json
  API-->>UI: { requirements }

  UI->>API: POST /generate_pdf_from_ids { ids }
  API->>DS: Lee convocatorias.json
  API-->>UI: { pdf_url, viewer_url }

  UI->>API: POST /send_email { from?, to[], adjunto }
  API->>SMTP: Envío
  API-->>UI: { status }
