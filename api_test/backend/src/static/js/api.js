const API_BASE = '/api/agent';
const TASKS_BASE = '/api/tasks';

/**
 * Función genérica para hacer Polling a Celery
 * @param {string} taskId - ID de la tarea
 * @param {function} onSuccess - Callback con los datos finales
 */
async function pollTask(taskId, onSuccess, onError) {
    const statusText = document.getElementById('loading-text');
    
    const interval = setInterval(async () => {
        try {
            const res = await fetch(`${TASKS_BASE}/${taskId}`);
            const data = await res.json();
            
            if (statusText) statusText.innerText = `Estado Agente: ${data.status}...`;

            if (data.status === 'SUCCESS') {
                clearInterval(interval);
                // Celery devuelve: { status: "completed", data: "JSON_STRING", ... }
                // Parseamos el JSON interno "data" que viene de Python
                let resultPayload = data.result; 
                if (typeof resultPayload.data === 'string') {
                    resultPayload.data = JSON.parse(resultPayload.data);
                }
                onSuccess(resultPayload);
            } 
            else if (data.status === 'FAILURE' || data.status === 'REVOKED') {
                clearInterval(interval);
                if (onError) onError(data);
                else alert("Error crítico en la ejecución del agente.");
            }
        } catch (e) {
            console.error("Polling error:", e);
            clearInterval(interval);
        }
    }, 2000); // Consultar cada 2s
}

// 1. Ingesta
async function apiStartIngest(text) {
    const res = await fetch(`${API_BASE}/ingest`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text: text})
    });
    return await res.json();
}

// 2. Generar Ideas
async function apiGenerateIdeas(sessionId) {
    const res = await fetch(`${API_BASE}/generate-ideas`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({session_id: sessionId})
    });
    return await res.json();
}

// 3. Seleccionar Idea (Generar Esquema)
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

// 4. Finalizar (Generar Documentos)
async function apiFinalize(sessionId) {
    const res = await fetch(`${API_BASE}/finalize`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({session_id: sessionId})
    });
    return await res.json();
}

// 5. Obtener Historial de Sesión
async function apiGetSessionHistory(sessionId) {
    const res = await fetch(`${API_BASE}/history/${sessionId}`, {
        method: 'GET',
        headers: {'Content-Type': 'application/json'}
    });
    if (!res.ok) throw new Error("No se pudo cargar la sesión");
    return await res.json();
}