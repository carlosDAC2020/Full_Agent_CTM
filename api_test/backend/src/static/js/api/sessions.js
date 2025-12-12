export async function fetchSessions() {
    try {
        const response = await fetch('/api/sessions');
        if (!response.ok) throw new Error('Error fetching sessions');
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return [];
    }
}
