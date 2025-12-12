import { fetchSessions } from '../api/sessions.js';
import { restoreSession } from './wizard.js'; // Import logic

export function toggleSidebar() {
    const sb = document.getElementById('sidebar');
    if (!sb) return;
    sb.classList.toggle('w-64');
    sb.classList.toggle('w-0');
    sb.classList.toggle('p-0');
}

export async function loadHistory() {
    const historyList = document.getElementById('history-list');
    if (!historyList) return;

    // Loading state could go here
    const sessions = await fetchSessions();
    historyList.innerHTML = '';

    if (sessions.length === 0) {
        historyList.innerHTML = '<div class="text-xs text-gray-400 px-2 italic">No hay historial reciente</div>';
        return;
    }

    sessions.forEach(session => {
        const item = document.createElement('div');
        const date = session.created_at ? new Date(session.created_at).toLocaleDateString() : 'Fecha desc.';

        item.className = "px-3 py-2 hover:bg-blue-900/30 cursor-pointer rounded-lg transition-colors group";
        item.onclick = () => restoreSession(session.id); // Click Handler

        item.innerHTML = `
            <div class="font-bold text-xs text-blue-100 truncate group-hover:text-white">${session.title_preview || 'Nueva Sesión'}</div>
            <div class="flex justify-between items-center mt-1">
                <span class="text-[10px] text-blue-400 uppercase tracking-wider">${session.status || 'Activo'}</span>
                <span class="text-[10px] text-gray-400">${date}</span>
            </div>
        `;
        historyList.appendChild(item);
    });
}
