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

export async function generateIdeas(sessionId) {
    try {
        const response = await fetch('/api/agent/generate-ideas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
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
            headers: { 'Content-Type': 'application/json' },
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
        const response = await fetch(`/api/agent/history/${sessionId}`);
        if (!response.ok) throw new Error('Error fetching session info');
        return await response.json();
    } catch (error) {
        console.error('API History Error:', error);
        throw error;
    }
}
