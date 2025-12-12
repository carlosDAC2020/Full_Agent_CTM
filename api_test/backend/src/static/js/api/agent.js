// Basic wrapper expecting a JSON response
export async function ingestCall(text, title = "") {
    try {
        const response = await fetch('/api/agent/ingest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                // Si el backend soportara título en el input_data lo mandaríamos, 
                // pero por ahora solo 'text'. 
                // El backend extraerá info de ahí.
            })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Error ingestion failed');
        }

        return await response.json(); // { task_id, session_id }
    } catch (error) {
        console.error('API Ingest Error:', error);
        throw error;
    }
}

export async function getSessionHistory(sessionId) {
    try {
        const response = await fetch(`/api/agent/history/${sessionId}`);
        if (!response.ok) throw new Error('Error fetching session info');
        return await response.json();
    } catch (error) {
        console.error('API History Error:', error);
        throw error;
    }
}
