<div align="center">
  <table style="border: none; border-collapse: collapse; background: transparent; margin: 20px auto;">
    <tr style="border: none;">
      <td style="border: none; padding: 0 40px 0 0; vertical-align: middle;">
        <img src="Intecmar_api/static/images/CotecmarLogo_white.png" alt="Intecmar Logo" width="160">
      </td>
      <td style="border: none; border-left: 6px solid #333; padding: 10px 0 10px 40px; vertical-align: middle; text-align: left;">
        <h1 style="border: none; margin: 0; padding: 0; font-size: 48px; line-height: 1; color: #ffffff; font-family: sans-serif;">
          Intecmar AI<br>Platform
        </h1>
      </td>
    </tr>
  </table>
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.95+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Celery-Async-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery">
  <img src="https://img.shields.io/badge/LangChain-AI-1C1C1C?style=for-the-badge&logo=chainlink&logoColor=white" alt="LangChain">
</p>

## **📖 Descripción General**

**Intecmar AI Platform** es una solución integral diseñada para modernizar y automatizar los procesos de vigilancia tecnológica y gestión de publicaciones digitales. La plataforma combina una arquitectura robusta de microservicios con capacidades avanzadas de Inteligencia Artificial Generativa.

Su propuesta de valor reside en dos pilares fundamentales:
1.  **Vigilancia Tecnológica Autónoma**: Un agente inteligente capaz de ingerir convocatorias, generar ideas de proyectos, investigar en fuentes académicas (Arxiv, Wikipedia) y redactar informes técnicos completos con diagramas y esquemas.
2.  **Gestión de Revista Digital**: Un sistema fluido para la maquetación, generación y visualización de revistas digitales interactivas, facilitando la difusión del conocimiento.

---

## **📸 Demo & User Journey**

La plataforma ofrece una experiencia fluida dividida en dos módulos principales. A continuación se detalla el flujo de trabajo:

### **1. Agente de Vigilancia Tecnológica (Wizard I+D+i) 🤖**

| Paso | Vista | Acción y Resultado |
| :--- | :--- | :--- |
| **01. Discovery** | > 💡 **Nota:** [Captura del Buscador de Convocatorias]. | El usuario filtra y selecciona una convocatoria oficial entre cientos de opciones nacionales e internacionales. |
| **02. Ingesta** | > 💡 **Nota:** [Captura de Ficha de Evaluación AI]. | El agente analiza el PDF de la convocatoria y extrae: objetivos, financiamiento y fechas clave automáticamente. |
| **03. Ideación** | > 💡 **Nota:** [Captura de Grid de Ideas Generadas]. | El LLM propone 3-4 ideas de proyectos únicos alineados con la convocatoria. El usuario puede co-crear editando títulos y objetivos. |
| **04. Estructura** | > 💡 **Nota:** [Captura del Visualizador de Esquema Técnico]. | Se genera el esquema base (Markdown/PDF) del proyecto, listo para ser expandido con investigación académica. |
| **05. Entrega** | > 💡 **Nota:** [Captura de Reporte Final con Imágenes]. | El agente entrega un reporte técnico completo, justificado científicamente y con apoyo visual generado por IA. |

---

### **2. Centro de Gestión de Magazines 📚**

> 💡 **Nota:** Inserta aquí un GIF/Video corto mostrando la selección de artículos y la generación instantánea del PDF de la revista.

*   **Curaduría Inteligente**: Selecciona múltiples convocatorias en un "carrito" para consolidarlas.
*   **Diseño Automatizado**: Genera un PDF maquetado profesionalmente con un solo clic.
*   **Distribución**: Envío directo por correo electrónico a listas de suscriptores desde la misma interfaz.

---

## **🛠️ Stack Tecnológico**

### **Frontend & User Interface**
*   **Jinja2 Templates (Server-Side Rendering)**: Elegido para una integración directa y rápida con el backend de Python, permitiendo una entrega de contenido dinámica y SEO-friendly.
*   **HTML5 / CSS3 / Vanilla JS**: Interfaz ligera y optimizada sin la sobrecarga de frameworks pesados, garantizando tiempos de carga mínimos.

### **Backend & Core**
*   **Python 3.10+**: Lenguaje base por su excelencia en ecosistemas de IA y Ciencia de Datos.
*   **FastAPI**: Framework moderno de alto rendimiento para construir APIs, con soporte nativo para asincronía y validación de datos (Pydantic).
*   **Celery**: Sistema de cola de tareas distribuido para manejar procesos pesados (generación de PDFs, flujos de agentes) sin bloquear la API principal.

### **Inteligencia Artificial (Agentic AI)**
*   **Google Gemini Pro**: LLM principal para razonamiento complejo y generación de contenido.
*   **LangChain / LangGraph**: Orquestación de flujos de agentes, permitiendo grafos de estado complejos con bucles de retroalimentación y subagentes.
*   **ChromaDB**: Base de datos vectorial para RAG (Retrieval-Augmented Generation), permitiendo al agente tener "memoria" y contexto sobre documentos.

### **Infraestructura & Datos**
*   **PostgreSQL**: Base de datos relacional robusta para usuarios, metadatos y persistencia transaccional.
*   **Redis**: Utilizado como broker de mensajes para Celery y capa de caché de alto rendimiento.
*   **MinIO**: Almacenamiento de objetos compatible con S3 para gestionar archivos grandes (PDFs, imágenes generadas) de forma escalable y local.
*   **Docker Compose**: Orquestación de contenedores para un despliegue replicable y aislado de todos los servicios.

---

## **🏗️ Arquitectura del Proyecto**

La plataforma utiliza una **Arquitectura Distribuida basada en el Patrón de Orquestación**. El núcleo del sistema no ejecuta los procesos pesados de IA o maquetación directamente; en su lugar, actúa como un cerebro que coordina múltiples servicios especializados.

### **Diagrama de Flujo y Componentes**

```mermaid
graph TD
    Client[🖥️ Cliente Web]
    API[🚀 Intecmar API Gateway]
    
    subgraph "Persistencia y Memoria"
        Redis[⚡ Shared Redis - Broker de Tareas]
        DB[(🐘 PostgreSQL - Datos Transaccionales)]
        MinIO[(📦 MinIO S3 - Almacenamiento de Reportes/PDFs)]
        Chroma[(🔍 ChromaDB - Base Vectorial RAG)]
    end

    subgraph "Unidades de Procesamiento (Workers)"
        MagWorker[⚙️ Magazine Worker - Generador de Revistas]
        AgentWorker[🤖 Agent Worker - Cerebro de Vigilancia]
    end

    subgraph "Servicios Externos"
        Gemini[🧠 Google Gemini Pro - Inferencia LLM]
        Web[🌐 Internet - Arxiv/Tavily Search]
    end

    Client -->|Solicitudes HTTP| API
    API -->|Persistencia| DB
    API -->|Carga de Archivos| MinIO
    API -->|Encola Tareas| Redis
    
    Redis -->|Consumo| MagWorker
    Redis -->|Consumo| AgentWorker
    
    MagWorker -->|Exporta PDF| MinIO
    
    AgentWorker -->|Contexto RAG| Chroma
    AgentWorker -->|Razonamiento| Gemini
    AgentWorker -->|Investigación| Web
    AgentWorker -->|Actualiza Estado| Redis
```

### **✅ Ventajas de esta Arquitectura**
*   **Zero-Blocking UI**: El usuario nunca experimenta tiempos de espera en la interfaz. Mientras el agente investiga (un proceso que toma ~60s), el usuario puede seguir navegando por otras secciones.
*   **Escalabilidad Horizontal**: Si la demanda aumenta, podemos desplegar múltiples réplicas de los `Workers` sin sobrecargar la API principal.
*   **Resiliencia**: Si un proceso de IA falla, la tarea se reintenta automáticamente por Celery sin que la aplicación principal se caiga.
*   **Integridad de Datos**: Al usar servicios aislados (MinIO, Postgres, Chroma), garantizamos que cada tipo de dato se maneje de forma óptima según su naturaleza (relacional, binario o vectorial).

### **⚠️ Desventajas y Desafíos**
*   **Complejidad de Gestión**: Requiere monitorear múltiples contenedores y servicios interconectados (Redis, Workers, DB).
*   **Consumo de Memoria**: Los procesos de IA en los Workers y la base de datos vectorial ChromaDB tienen un consumo de RAM considerable.
*   **Latencia de Red**: Al ser servicios separados, existe un pequeño overhead en la comunicación entre contenedores (mitigado por el uso de redes Docker internas de baja latencia).

### **📈 Mejoras y Escalabilidad Futura**
*   **Migración a Kubernetes**: Para orquestar el auto-escalado de los Workers basado en la carga de la cola de Redis.
*   **Caché de Resultados (Redis)**: Implementar una capa de caché para evitar consultas redundantes a Gemini sobre temas ya investigados.
*   **Cluster de Base de Datos**: Mover hacia un cluster de PostgreSQL con réplicas de lectura para manejar miles de usuarios simultáneos.
*   **Monitoreo Avanzado**: Integración con Prometheus y Grafana para visualizar la salud de los agentes y cuellos de botella en tiempo real.

---

---

### **🌐 Servicios Externos y Ecosistema de Herramientas**

El agente no opera de forma aislada; utiliza un ecosistema de APIs de primer nivel para garantizar la veracidad y calidad de sus resultados:

*   **Google Gemini API (Pro/Flash)**: El motor cognitivo principal. Se encarga de la inferencia de lenguaje, el razonamiento lógico del grafo y la síntesis de información compleja.
*   **LangSmith (LangChain Ecosystem)**: Nuestro panel de **Observabilidad y Monitoreo**. Permite realizar trazas (tracing) de cada paso del agente en tiempo real, depurar cadenas de pensamiento y optimizar el rendimiento de los flujos agenticos.
*   **Brave Search API**: Motor de búsqueda de nueva generación que proporciona resultados limpios y privados, utilizado por el agente para ampliar el espectro de búsqueda más allá de los motores tradicionales.
*   **Tavily Search API**: Un buscador optimizado para agentes de IA que permite realizar investigaciones web precisas, filtradas y sin ruido publicitario.
*   **DuckDuckGo Tool**: Utilizado como herramienta de respaldo para búsquedas rápidas y anónimas de información general.
*   **Semantic Scholar & Arxiv API**: APIs académicas que el agente interroga para fundamentar las propuestas con literatura científica y técnica de vanguardia.

---

## **✨ Características Principales**

### **🤖 Agente de Vigilancia Tecnológica**
*   **Ingesta Inteligente**: Análisis automático de convocatorias y documentos PDF/Word cargados.
*   **Generación de Ideas**: Propone ideas de proyectos innovadores basándose en los requisitos de la convocatoria.
*   **Investigación Académica**: Busca y sintetiza papers relevantes de Arxiv y otras fuentes científicas.
*   **Reportes Automatizados**: Genera documentos técnicos detallados con esquemas de proyecto y justificaciones.
*   **Generación de Imágenes**: Crea visuales conceptuales para acompañar los proyectos (via subgrafo de imagen).

### **📚 Revista Digital**
*   **Gestión de Contenidos**: Creación y edición de artículos y publicaciones.
*   **Generación de PDF**: Motor de renderizado de alta calidad para exportar revistas completas.
*   **Visor Interactivo**: Experiencia de lectura fluida tipo flipbook.

### **🔐 Gestión de Usuarios**
*   **Autenticación Segura**: Sistema basado en JWT.
*   **Perfiles de Usuario**: Gestión de información personal y preferencias.
*   **Recuperación de Contraseña**: Flujo completo de reset via email.

---

---

## **🧠 Deep Dive: Motor de IA y RAG (Retrieval-Augmented Generation)**

La verdadera potencia de Intecmar AI no reside solo en el uso de LLMs, sino en cómo gestiona el conocimiento mediante una arquitectura de **Estado y Memoria Contextual**.

### **1. El Cerebro: Orquestación con LangGraph**
A diferencia de un chat simple, nuestro agente opera sobre un **Grafo de Estados**. Esto significa que:
*   **Memoria de Sesión**: El agente sabe qué convocatoria elegiste en el Paso 1 mientras genera el reporte en el Paso 5.
*   **Razonamiento Cíclico**: Si la información extraída no es suficiente, el agente puede decidir "volver atrás" o consultar una herramienta externa antes de dar una respuesta.

### **2. Implementación Lógica del RAG (Memoria de Corto Plazo)**
Cuando el usuario sube documentos adicionales (PDF, Word, Excel), se activa el pipeline de **RAG**:
1.  **Ingesta y Fragmentación**: Los archivos se cargan y se dividen en fragmentos lógicos (chunks) para que la IA pueda procesarlos sin perder el contexto.
2.  **Vectorización (Embeddings)**: Cada fragmento se convierte en un vector matemático utilizando modelos de **Google Gemini Embeddings**.
3.  **Indexación en ChromaDB**: Estos vectores se guardan en una base de datos vectorial efímera vinculada únicamente a la **session_id** del usuario.
4.  **Recuperación Semántica**: Durante la generación de la propuesta, el agente utiliza una **herramienta de búsqueda (Tool-Use)** para interrogar sus propios documentos, extrayendo solo la información relevante para justificar la propuesta técnica.

### **3. Generación de Imágenes Articulada (Visual Intelligence)**
El sistema no solo genera texto, sino que construye una identidad visual para cada propuesta técnica mediante un subgrafo especializado:
1.  **Análisis Conceptual**: El agente analiza la propuesta final para extraer "metáforas visuales" y conceptos técnicos clave.
2.  **Sintetizador de Prompts**: Un componente lógico traduce estos conceptos en prompts estructurados (descriptivos y técnicos) optimizados para modelos de generación de imágenes.
3.  **Orquestación de Subgrafo**: La generación no bloquea el flujo principal. El `Image_generator_subgraph` opera de forma coordinada para generar, procesar y almacenar los recursos visuales en **MinIO**.
4.  **Integración Dinámica**: Las imágenes resultantes se vinculan automáticamente al reporte final (Markdown/PDF), proporcionando esquemas conceptuales y visuales que mejoran la comprensión del proyecto.

### **4. Herramientas y Capacidades (ReAct Pattern)**
El agente implementa el patrón **ReAct (Reason + Act)**, permitiéndole usar "herramientas" según la lógica de la misión:
*   **Investigación Científica**: Consultas a **Arxiv** y **Semantic Scholar** para validar estados del arte.
*   **Web Researcher**: Uso de **Tavily/DuckDuckGo** para monitoreo de tendencias y convocatorias.
*   **Visualizer**: Motor lógico para la creación de esquemas técnicos y flujogramas.

### **5. Sistema de Notificaciones por Correo 📧**
La plataforma integra un sistema de comunicación automatizado para la distribución de resultados:
*   **Gestión de Destinatarios**: Permite configurar una lista de "correos favoritos" y remitentes personalizados a nivel de base de datos.
*   **Plantillas Branded**: Uso de **Jinja2** para renderizar correos elegantes y profesionales que incluyen el logo de la organización y un resumen del contenido.
*   **Distribución de Activos**: Envío automático de los PDFs generados (revistas o reportes técnicos) como adjuntos directamente desde la interfaz.
*   **Modo Demo vs Producción**: Controlado por la variable `DEMO_MODE` para evitar envíos accidentales durante el desarrollo.

### **6. Persistencia del Estado**
Toda la lógica del agente se guarda de forma persistente. Si el usuario cierra el navegador, puede retomar el "Wiki-Wizard" exactamente donde lo dejó, recuperando tanto el estado del grafo como la base de datos vectorial cargada previamente.

---

## **💾 Modelo de Datos**

Las entidades principales están diseñadas para soportar la relación entre usuarios, sus flujos de trabajo (agentes) y los recursos generados (revistas/documentos).

```mermaid
erDiagram
    User ||--o{ Magazine : generates
    User ||--o{ Flow : tracks
    User ||--o{ SavedItem : bookmarks
    User ||--o{ AgentSession : owns
    
    AgentSession ||--o{ AgentStep : contains
    
    User {
        int id PK
        string email UK
        string name
        string role
        string password_hash
        datetime created_at
    }
    
    AgentSession {
        string id PK
        int user_id FK
        string status
        string current_task_id
        datetime created_at
    }
    
    AgentStep {
        int id PK
        string session_id FK
        string step_type
        json input_data
        json output_data
        datetime created_at
    }
    
    Magazine {
        int id PK
        int user_id FK
        string title
        string filename
        int size_bytes
        datetime created_at
    }
    
    Flow {
        int id PK
        int user_id FK
        string task_id
        string type
        string status
        json meta
        datetime created_at
        datetime finished_at
    }
    
    Convocatoria {
        int id PK
        string title
        text description
        string url
        datetime deadline
        string type_financy
        string monto
        json requisitos
        json beneficios
    }
    
    SavedItem {
        int id PK
        int user_id FK
        string item_ref
        json item_metadata
    }

    Source {
        int id PK
        string name
        string url UK
        string type
        boolean is_active
    }
```

### **📋 Descripción de Modelos Clave**

1.  **User**: Gestiona la identidad y el acceso. Soporta roles personalizados (`admin`/`user`) y almacena metadatos de perfil. Es el eje central de la personalización de la plataforma.
2.  **AgentSession**: Representa el "hilo" de una investigación específica del agente I+D+i. Vincula a un usuario con un flujo de trabajo agéntico completo, permitiendo la persistencia a largo plazo.
3.  **AgentStep**: Captura el estado exacto de cada paso del grafo (ingesta, ideación, esquema, etc.). Almacena los `input_data` y `output_data` de cada nodo, permitiendo restaurar la sesión en cualquier punto sin perder información.
4.  **Convocatoria**: El núcleo de datos del agente. Almacena no solo el texto bruto, sino también metadatos estructurados (montos, requisitos, fechas) que el motor **RAG** utiliza para filtrar y priorizar oportunidades.
5.  **Flow**: Actúa como el libro de registro (ledger) de las tareas asíncronas globales (como la generación de revistas). Vincula las tareas de Celery con los usuarios.
6.  **Magazine**: Registro de las publicaciones digitales generadas. Almacena punteros a los archivos físicos en **MinIO** y metadatos de maquetación.
7.  **SavedItem**: Permite a los usuarios "marcar como favoritos" convocatorias o fuentes específicas.
8.  **Source**: Configuración dinámica de orígenes de datos (Scrapers/RSS).

---

## **⚙️ Configuración e Instalación**

### **Prerrequisitos**
*   Docker & Docker Compose (v20.10+)
*   Git

### **1. Clonar el Repositorio**
```bash
git clone  https://github.com/VerbaNexAI/API-CTM.git
cd API-CTM
```

### **2. Configurar Variables de Entorno**
Crea un archivo `.env` en la raíz del proyecto. Este archivo es crucial para la orquestación de servicios y la conexión con las IAs externas:

```ini
# --- Configuración de Red / Producción ---
# URL pública para links correctos en reportes/revistas
BASE_URL=http://localhost:8000

# --- Inteligencia Artificial ---
GEMINI_API_KEY=tu_clave_de_google_ai
NANO_BANANA_API_KEY=tu_clave_para_generacion_de_imagenes

# --- Motores de Búsqueda ---
TAVILY_API_KEY=tu_clave_de_tavily
BRAVE_API_KEY=tu_clave_de_brave

# --- Observabilidad (LangChain) ---
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=tu_clave_de_langsmith
LANGSMITH_PROJECT=Cotecmar

# --- Notificaciones (SMTP Gmail) ---
DEMO_MODE=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_TLS=true
SMTP_USER=tu_correo@gmail.com
SMTP_PASS=tu_password_de_aplicacion_gmail

# --- Configuración de Base de Datos ---
POSTGRES_USER=shared_user
POSTGRES_PASSWORD=shared_pass
POSTGRES_DB=intecmar_db
DATABASE_URL=postgresql+psycopg2://shared_user:shared_pass@shared_postgres:5432/intecmar_db

# --- Infraestructura y Seguridad ---
REDIS_URL=redis://shared_redis:6379/0
JWT_SECRET=tu_secreto_para_tokens
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# --- Almacenamiento (MinIO) ---
MINIO_ENDPOINT=http://shared-minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_SECURE=False
MINIO_BUCKET_NAME=intecmar-data

# --- Base de Datos Vectorial (ChromaDB) ---
CHROMA_HOST=chromadb
CHROMA_PORT=8000
```

> [!TIP]
> **Despliegue en Producción**: Cambia `BASE_URL` por tu dominio real. En `DATABASE_URL`, `REDIS_URL`, `MINIO_ENDPOINT` y `CHROMA_HOST`, el sistema usará los valores por defecto del `docker-compose.yml` (nombres de servicios internos) a menos que los sobreescribas aquí. Esto permite que el mismo archivo funcione en local y en la nube sin tocar el código.

### **3. Desplegar con Docker Compose**
Levanta toda la infraestructura con un solo comando:

```bash
docker-compose up --build -d
```
> Esto iniciará la API, Base de Datos, Redis, MinIO, ChromaDB y los Workers.

### **4. Migraciones Iniciales**
El contenedor `intecmar_api` ejecuta automáticamente las migraciones al inicio, pero puedes forzarlas manualmente si es necesario:

```bash
docker-compose exec intecmar_api python backend/scripts/migrate_convocatorias.py
```

### **5. Acceder a la Aplicación**
*   **Frontend/Landing**: [http://localhost:8000/landing](http://localhost:8000/landing)
*   **API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
*   **MinIO Console**: [http://localhost:9001](http://localhost:9001)

---

## **🔌 API Endpoints (v1)**

La API está versionada bajo el prefijo `/api/v1`. A continuación se detallan los módulos principales:

### **🔐 Autenticación y Usuarios**
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/auth/register` | Registro de nuevos usuarios administradores. |
| `POST` | `/auth/login` | Login y obtención de Bearer Token (JWT). |
| `GET` | `/auth/me` | Información del usuario actual. |
| `POST` | `/auth/forgot-password` | Iniciar recuperación de contraseña. |
| `POST` | `/auth/reset-password` | Confirmar nueva contraseña con token. |
| `GET` | `/users/me` | Perfil detallado del usuario. |
| `PUT` | `/users/me` | Actualizar bio/teléfono/nombre. |
| `POST` | `/users/me/profile-picture` | Subir avatar a MinIO. |

### **🤖 Agente de Vigilancia (I+D+i)**
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/agent/ingest` | Iniciar sesión y cargar texto/archivos (RAG). |
| `POST` | `/agent/generate-ideas` | Disparar brainstorming de ideas técnicas. |
| `POST` | `/agent/select-idea` | Confirmar idea para desarrollar el reporte. |
| `POST` | `/agent/research` | Iniciar investigación profunda y papers. |
| `POST` | `/agent/finalize` | Generar el esquema final del proyecto. |
| `POST` | `/agent/append-docs` | Añadir más documentos a una sesión activa. |
| `GET` | `/agent/history/{id}` | Recuperar estado completo de una sesión. |
| `GET` | `/agent_sessions` | Listar todas las sesiones del usuario. |
| `GET` | `/agent_tasks/{id}` | Polling del estado de la tarea del agente. |

### **📚 Revista y Convocatorias**
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/convocatorias` | Listar todas las convocatorias detectadas. |
| `POST` | `/generate` | Generar revista automática (celery). |
| `POST` | `/generate_pdf_from_ids` | Generar PDF de una selección específica. |
| `GET` | `/magazines` | Listar archivos PDF generados. |
| `GET` | `/saved` | Ver marcadores (bookmarks) del usuario. |
| `POST` | `/saved` | Guardar convocatoria en favoritos. |
| `GET` | `/history` | Historial unificado de actividad. |

### **⚙️ Utilidades y Sistema**
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/sources` | Lista de fuentes de datos configuradas. |
| `POST` | `/sources/search` | Búsqueda manual de convocatorias. |
| `POST` | `/upload_pdf` | Subida temporal de documentos. |
| `POST` | `/send_email` | Enviar revista por correo electrónico. |
| `GET` | `/tasks/stream` | Canal SSE para eventos en tiempo real. |
| `GET` | `/minio/{path}` | Proxy de acceso a archivos en MinIO (S3). |

### **🛠️ Guía de Integración para Desarrolladores Externos**

Si deseas construir un cliente externo o integrar la lógica de Intecmar AI en otro sistema, sigue estas pautas conceptuales:

#### **1. Seguridad y Cabeceras**
*   **Autenticación**: Todas las rutas (excepto login/register) requieren un token Bearer. Envíalo en la cabecera `Authorization: Bearer <TOKEN>`.
*   **Formatos**: La mayoría de los endpoints usan `application/json`. Las cargas de archivos (documentos de contexto, imágenes de perfil) utilizan `multipart/form-data`.

#### **2. Orquestación del Agente (Ciclo de Vida)**
La interacción con los agentes de I+D+i sigue un flujo de estado:
1.  **Inicio (Ingest)**: Al cargar el texto inicial, recibirás un `session_id`. Este ID es obligatorio para todas las peticiones futuras de esa sesión.
2.  **Transiciones de Estado**: Los pasos posteriores (`generate-ideas`, `select-idea`, `research`, `finalize`) avanzan el grafo de la IA. Estas peticiones retornan un `task_id`.
3.  **Ejecución Asíncrona**: La IA no responde en tiempo real; trabaja mediante workers de Celery. Debes monitorear el progreso de la tarea asignada.

#### **3. Monitoreo de Tareas y Tiempo Real**
*   **Polling**: Consulta el endpoint `/agent_tasks/{task_id}` hasta que el estado sea satisfactorio.
*   **Real-time (SSE)**: Conéctate al canal de eventos `/tasks/stream` (Server-Sent Events) para recibir actualizaciones automáticas del estado de las tareas sin sobrecargar el servidor.

#### **4. Acceso a Recursos (MinIO Proxy)**
No accedas directamente al almacenamiento S3. Utiliza la ruta unificada `/api/v1/minio/{path}` para recuperar PDFs, imágenes generadas o documentos de usuario. La API gestiona la seguridad y el streaming de estos archivos.

---

### **📚 Documentación Interactiva (Swagger / ReDoc)**

Para obtener el detalle técnico exacto de cada endpoint (esquemas JSON de entrada/salida, códigos de error y pruebas en tiempo real), Intecmar AI utiliza la documentación automática de FastAPI:

*   **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)  
    *(Permite probar los endpoints directamente desde el navegador)*.
*   **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)  
    *(Documentación técnica limpia y organizada)*.

> [!TIP]
> Todos los endpoints están enriquecidos con descripciones y metadatos directamente en el código fuente para garantizar que la documentación esté siempre sincronizada con la lógica del servidor.

---

## **🚀 Roadmap**

*   [ ] **Dashboard de Analítica**: Métricas de uso de los agentes y temas más buscados.
*   [ ] **Soporte Multi-LLM**: Alternar entre GPT-4, Gemini y Claude.
*   [ ] **App Móvil**: Versión React Native para consumir revistas y alertas.
*   [ ] **Colaboración en Tiempo Real**: Edición colaborativa de reportes generados.

---

<p align="center">
  <sub>Desarrollado con ❤️ para Intecmar</sub>
</p>
