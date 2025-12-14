# CTM Agent Platform API Documentation

## Descripción General

Esta API proporciona la interfaz backend para la Plataforma de Agentes CTM. Está construida sobre **FastAPI** y utiliza una arquitectura asíncrona basada en **Celery** y **Redis** para manejar tareas de larga duración (procesamiento de LLMs, generación de documentos, etc.).

La API está diseñada para soportar un flujo de trabajo secuencial donde el usuario interactúa con un agente inteligente para analizar convocatorias, generar ideas y producir entregables finales.

## Arquitectura

El sistema sigue un patrón de **Asynchronous Task Queue**:

1.  **FastAPI** recibe las peticiones HTTP y delega el procesamiento pesado a **Celery**.
2.  Los endpoints de acción (`/api/agent/...`) retornan inmediatamente un `task_id` y un `session_id`.
3.  El cliente debe hacer polling al endpoint de tareas (`/api/tasks/{task_id}`) para recibir actualizaciones de estado (streaming) y el resultado final.
4.  **MinIO** se utiliza para el almacenamiento de objetos (documentos generados), y la API se encarga de generar URLs firmadas para el acceso seguro.
5.  **PostgreSQL** almacena el historial persistente de las sesiones y pasos del agente.

## Flujo de Trabajo Típico

1.  **Ingesta**: Enviar texto de convocatoria -> Recibir `task_id`.
2.  **Polling**: Consultar estado de la tarea hasta completar.
3.  **Ideación**: Solicitar generación de ideas -> Recibir `task_id`.
4.  **Selección**: Enviar idea seleccionada -> Recibir `task_id` (Generación de esquema).
5.  **Finalización**: Solicitar documentos finales -> Recibir `task_id`.

## Referencia de API

### 🤖 Agent Actions (`/api/agent`)

Endpoints principales para controlar el flujo del agente.

#### `POST /api/agent/ingest`
Inicia una nueva sesión analizando el texto de una convocatoria.

*   **Body**:
    ```json
    {
      "text": "Texto completo de la convocatoria..."
    }
    ```
*   **Respuesta**:
    ```json
    {
      "task_id": "uuid-task-...",
      "session_id": "uuid-session-..."
    }
    ```

#### `POST /api/agent/generate-ideas`
Genera propuestas de valor basadas en la información ingerida.

*   **Body**:
    ```json
    {
      "session_id": "uuid-session-..."
    }
    ```
*   **Respuesta**: `{"task_id": "...", "session_id": "..."}`

#### `POST /api/agent/select-idea`
Confirma una idea seleccionada y genera el esquema inicial del proyecto.

*   **Body**:
    ```json
    {
      "session_id": "uuid-session-...",
      "selected_idea": { "idea_title": "...", "idea_description": "..." }
    }
    ```
*   **Respuesta**: `{"task_id": "...", "session_id": "..."}`

#### `POST /api/agent/finalize`
Ejecuta la investigación profunda y genera todos los entregables finales (PDFs, Markdown, etc.).

*   **Body**:
    ```json
    {
      "session_id": "uuid-session-..."
    }
    ```
*   **Respuesta**: `{"task_id": "...", "session_id": "..."}`

#### `GET /api/agent/history/{session_id}`
Recupera el estado completo de una sesión para restaurar la interfaz de usuario.
*   **Respuesta**: Objeto con estado de la sesión, fecha de creación y mapa de datos de todos los pasos ejecutados.

---

### 🔄 Tasks (`/api/tasks`)

Endpoint para monitoreo de tareas asíncronas.

#### `GET /api/tasks/{task_id}`
Obtiene el estado actual y resultado de una tarea.

*   **Respuesta (En Progreso)**:
    ```json
    {
      "task_id": "...",
      "status": "PROGRESS",
      "info": { "message": "Analizando requisitos..." }
    }
    ```
*   **Respuesta (Completado)**:
    ```json
    {
      "task_id": "...",
      "status": "SUCCESS",
      "result": {
        "status": "completed",
        "data": { ... } // Datos del paso (incluye URLs firmadas de MinIO)
      }
    }
    ```

---

### 🗂️ Sessions (`/api/sessions`)

Gestión del historial de evaluaciones.

#### `GET /api/sessions`
Lista las sesiones recientes (últimas 50).
*   **Respuesta**: Array de sesiones con ID, estado, fecha y vista previa del título.

#### `GET /api/sessions/{session_id}/steps`
Lista los pasos individuales completados en una sesión.
*   **Respuesta**: Array de objetos con tipo de paso y timestamp.
