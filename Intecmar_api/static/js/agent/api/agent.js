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

export async function ingestCall(text, files = []) {
    try {
        const formData = new FormData();
        formData.append('text', text);

        if (files && files.length > 0) {
            for (let i = 0; i < files.length; i++) {
                formData.append('files', files[i]);
            }
        }

        const token = localStorage.getItem('auth_token');
        const response = await fetch('/api/agent/ingest', {
            method: 'POST',
            headers: {
                ...(token && { 'Authorization': `Bearer ${token}` })
                // Let the browser set the Content-Type with boundary for FormData
            },
            body: formData
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

export async function generateIdeas(sessionId, thematicLine = null, methodology = null) {
    try {
        // DEBUG: Log ANTES del fetch para ver qué se envía
        console.log('📤 ABOUT TO SEND to /generate-ideas:', {
            session_id: sessionId,
            selected_thematic_line: thematicLine,
            selected_methodology: methodology
        });

        const response = await fetch('/api/agent/generate-ideas', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                session_id: sessionId,
                selected_thematic_line: thematicLine,
                selected_methodology: methodology
            })
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
    console.log("🚀 [API] selectIdea V2.0 - Sending data:", idea);
    try {
        const response = await fetch('/api/agent/select-idea', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                session_id: sessionId,
                selected_idea: {
                    idea_title: idea.idea_title || idea.title,
                    idea_description: idea.idea_description || idea.desc,
                    idea_objectives: idea.idea_objectives || idea.objectives,
                    idea_general_objective: idea.idea_general_objective || idea.general_objective,
                    duration_time: idea.duration_time || idea.suggested_duration_months,
                    executor_entity: idea.executor_entity,
                    executor_entity_logo: idea.executor_entity_logo,
                    coejecutors_entities: idea.coejecutors_entities,
                    coejecutors_entities_logos: idea.coejecutors_entities_logos,
                    collaborators_entities: idea.collaborators_entities,
                    collaborators_entities_logos: idea.collaborators_entities_logos
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

export async function finalizeProject(sessionId, config = {}) {
    try {
        const response = await fetch('/api/agent/finalize', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                session_id: sessionId,
                generation_config: config
            })
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

export async function researchCall(sessionId) {
    try {
        const response = await fetch('/api/agent/research', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ session_id: sessionId })
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Error starting research');
        }
        return await response.json();
    } catch (error) {
        console.error('API Research Error:', error);
        throw error;
    }
}

export async function appendDocsCall(sessionId, files) {
    try {
        const formData = new FormData();
        formData.append('session_id', sessionId);
        if (files && files.length > 0) {
            for (let i = 0; i < files.length; i++) {
                formData.append('files', files[i]);
            }
        }
        const token = localStorage.getItem('auth_token');
        const response = await fetch('/api/agent/append-docs', {
            method: 'POST',
            headers: { ...(token && { 'Authorization': `Bearer ${token}` }) },
            body: formData
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Error appending docs');
        }
        return await response.json();
    } catch (error) {
        console.error('API Append Docs Error:', error);
        throw error;
    }
}
export async function uploadAllianceLogo(sessionId, file) {
    try {
        const formData = new FormData();
        formData.append('session_id', sessionId);
        formData.append('file', file);

        const token = localStorage.getItem('auth_token');
        const response = await fetch('/api/agent/upload-alliance-logo', {
            method: 'POST',
            headers: { ...(token && { 'Authorization': `Bearer ${token}` }) },
            body: formData
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Error uploading logo');
        }

        return await response.json(); // { path, url, filename }
    } catch (error) {
        console.error('API Upload Logo Error:', error);
        throw error;
    }
}

export async function getPosterHistory(sessionId) {
    try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch(`/api/agent/poster-history/${sessionId}`, {
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        if (!response.ok) throw new Error('Error fetching poster history');
        return await response.json();
    } catch (error) {
        console.error('API Poster History Error:', error);
        throw error;
    }
}

export async function applyLogos(payload) {
    try {
        const response = await fetch('/api/agent/apply-logos', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Error applying logos');
        }

        return await response.json();
    } catch (error) {
        console.error('API Apply Logos Error:', error);
        throw error;
    }
}
