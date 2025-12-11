/**
 * api.js
 * Capa de comunicación con la API del backend.
 * Incluye funciones para todas las operaciones del agente y polling con streaming.
 */

const API_BASE = '/api/agent';
const TASKS_BASE = '/api/tasks';
const SESSIONS_BASE = '/api/sessions';

// ==========================================
// POLLING CON SOPORTE DE STREAMING
// ==========================================

/**
 * Función de Polling a Celery con soporte para mensajes de progreso.
 * @param {string} taskId - ID de la tarea Celery
 * @param {function} onSuccess - Callback cuando la tarea completa exitosamente
 * @param {function} onError - Callback cuando hay error
 * @param {function} onProgress - Callback para mensajes de progreso (streaming)
 */
async function pollTask(taskId, onSuccess, onError, onProgress) {
    const interval = setInterval(async () => {
        try {
            const res = await fetch(`${TASKS_BASE}/${taskId}`);
            const data = await res.json();

            // CASO 1: EN PROGRESO (Streaming de mensajes)
            if (data.status === 'PROGRESS') {
                if (onProgress && data.info?.message) {
                    onProgress(data.info.message);
                }
            }
            // CASO 2: COMPLETADO EXITOSAMENTE
            else if (data.status === 'SUCCESS') {
                clearInterval(interval);
                
                // Parsear datos internos si vienen como string
                let resultPayload = data.result;
                if (resultPayload && typeof resultPayload.data === 'string') {
                    try {
                        resultPayload.data = JSON.parse(resultPayload.data);
                    } catch (e) {
                        console.warn("No se pudo parsear data:", e);
                    }
                }
                
                if (onSuccess) onSuccess(resultPayload);
            }
            // CASO 3: ERROR
            else if (data.status === 'FAILURE' || data.status === 'REVOKED') {
                clearInterval(interval);
                if (onError) {
                    onError(data);
                } else {
                    console.error("Error en tarea:", data);
                    alert("Error crítico en la ejecución del agente.");
                }
            }
        } catch (e) {
            console.error("Polling error:", e);
            clearInterval(interval);
            if (onError) onError({ error: e.message });
        }
    }, 1500); // Consultar cada 1.5 segundos
    
    return interval; // Retornar para poder cancelar si es necesario
}

// ==========================================
// API DEL AGENTE
// ==========================================

/**
 * 1. Iniciar Ingesta - Envía el texto de la convocatoria
 */
async function apiStartIngest(text) {
    const res = await fetch(`${API_BASE}/ingest`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ text: text })
    });
    return await res.json();
}

/**
 * 2. Generar Ideas de Proyecto
 */
async function apiGenerateIdeas(sessionId) {
    const res = await fetch(`${API_BASE}/generate-ideas`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ session_id: sessionId })
    });
    return await res.json();
}

/**
 * 3. Seleccionar Idea y Generar Esquema Inicial
 */
async function apiSelectIdea(sessionId, ideaObj) {
    const res = await fetch(`${API_BASE}/select-idea`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            session_id: sessionId,
            selected_idea: ideaObj
        })
    });
    return await res.json();
}

/**
 * 4. Finalizar - Generar Investigación y Documentos Finales
 */
async function apiFinalize(sessionId) {
    const res = await fetch(`${API_BASE}/finalize`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ session_id: sessionId })
    });
    return await res.json();
}

/**
 * 5. Obtener Historial de una Sesión específica
 */
async function apiGetSessionHistory(sessionId) {
    const res = await fetch(`${API_BASE}/history/${sessionId}`, {
        method: 'GET',
        headers: {'Content-Type': 'application/json'}
    });
    if (!res.ok) throw new Error("No se pudo cargar la sesión");
    return await res.json();
}

// ==========================================
// API DE SESIONES (HISTORIAL)
// ==========================================

/**
 * Lista todas las sesiones del historial
 */
async function apiListSessions() {
    const res = await fetch(SESSIONS_BASE);
    if (!res.ok) throw new Error("No se pudo cargar el historial");
    return await res.json();
}

/**
 * Obtiene los pasos de una sesión
 */
async function apiGetSessionSteps(sessionId) {
    const res = await fetch(`${SESSIONS_BASE}/${sessionId}/steps`);
    if (!res.ok) throw new Error("No se pudieron cargar los pasos");
    return await res.json();
}