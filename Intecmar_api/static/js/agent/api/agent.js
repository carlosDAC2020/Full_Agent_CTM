// Helper to get auth headers
function getAuthHeaders() {
    const token = localStorage.getItem('auth_token');
    return {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };
}

// Basic wrapper expecting a JSON response
export async function getConvocatorias() {
    try {
        const response = await fetch('/api/agent/convocatorias', {
            headers: getAuthHeaders()
        });
        if (!response.ok) throw new Error('Error fetching convocatorias');
        return await response.json();
    } catch (error) {
        console.error('API Convocatorias Error:', error);
        throw error;
    }
}

export async function ingestCall(text, title = "") {
    try {
        const response = await fetch('/api/agent/ingest', {
            method: 'POST',
            headers: getAuthHeaders(),
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

export async function generateIdeas(sessionId) {
    try {
        const response = await fetch('/api/agent/generate-ideas', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ session_id: sessionId })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Error generating ideas');
        }

        return await response.json(); // { task_id, session_id }
    } catch (error) {
        console.error('API Gen Ideas Error:', error);
        throw error;
    }
}

export async function selectIdea(sessionId, idea) {
    try {
        const response = await fetch('/api/agent/select-idea', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                session_id: sessionId,
                selected_idea: {
                    idea_title: idea.title,
                    idea_description: idea.desc,
                    idea_objectives: idea.objectives
                }
            })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Error selecting idea');
        }

        return await response.json(); // { task_id, session_id }
    } catch (error) {
        console.error('API Select Idea Error:', error);
        throw error;
    }
}

export async function getSessionHistory(sessionId) {
    try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch(`/api/agent/history/${sessionId}`, {
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        if (!response.ok) throw new Error('Error fetching session info');
        return await response.json();
    } catch (error) {
        console.error('API History Error:', error);
        throw error;
    }
}

export async function finalizeProject(sessionId) {
    try {
        const response = await fetch('/api/agent/finalize', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ session_id: sessionId })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Error finalizing project');
        }

        return await response.json(); // { task_id, session_id }
    } catch (error) {
        console.error('API Finalize Error:', error);
        throw error;
    }
}
