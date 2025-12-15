export async function fetchSessions() {
    try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch('/api/sessions', {
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        if (!response.ok) throw new Error('Error fetching sessions');
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return [];
    }
}

export async function deleteSession(sessionId) {
    try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch(`/api/sessions/${sessionId}`, {
            method: 'DELETE',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        if (!response.ok) throw new Error('Error deleting session');
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}
