import { fetchSessions, deleteSession } from '../api/sessions.js';
import { restoreSession } from './wizard.js'; // Import logic

export function toggleSidebar() {
    const sb = document.getElementById('sidebar');
    if (!sb) return;
    sb.classList.toggle('w-64');
    sb.classList.toggle('w-0');
    sb.classList.toggle('p-0');
}

// Mapeo de step_type a nombres amigables y colores
const STEP_INFO = {
    'ingest': { name: 'Evaluación', color: 'bg-blue-500', icon: 'ph-file-magnifying-glass' },
    'proposal_ideas': { name: 'Ideas', color: 'bg-yellow-500', icon: 'ph-lightbulb' },
    'project_idea': { name: 'Esquema', color: 'bg-purple-500', icon: 'ph-file-text' },
    'generate_project': { name: 'Final', color: 'bg-green-500', icon: 'ph-check-circle' }
};

export async function loadHistory() {
    const historyList = document.getElementById('history-list');
    if (!historyList) return;

    // Loading state
    historyList.innerHTML = '<div class="text-xs text-gray-400 px-2 italic">Cargando...</div>';

    const sessions = await fetchSessions();
    historyList.innerHTML = '';

    if (sessions.length === 0) {
        historyList.innerHTML = '<div class="text-xs text-gray-400 px-2 italic">No hay historial reciente</div>';
        return;
    }

    sessions.forEach(session => {
        const item = document.createElement('div');
        const date = session.created_at ? new Date(session.created_at).toLocaleDateString() : 'Fecha desc.';

        // Obtener información del paso
        const stepInfo = STEP_INFO[session.last_step] || { name: 'Iniciado', color: 'bg-gray-500', icon: 'ph-circle' };

        item.className = "px-3 py-2 hover:bg-blue-900/30 rounded-lg transition-colors group relative";

        item.innerHTML = `
            <div class="flex items-start gap-2">
                <!-- Área clickeable para restaurar -->
                <div class="flex-1 cursor-pointer" data-session-id="${session.id}">
                    <div class="font-bold text-xs text-blue-100 truncate group-hover:text-white pr-6">
                        ${session.title_preview || 'Nueva Sesión'}
                    </div>
                    <div class="flex items-center gap-2 mt-1">
                        <!-- Badge del paso -->
                        <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[9px] font-bold text-white ${stepInfo.color}">
                            <i class="ph ${stepInfo.icon} text-[10px]"></i>
                            ${stepInfo.name}
                        </span>
                        <span class="text-[10px] text-gray-400">${date}</span>
                    </div>
                </div>
                
                <!-- Botón eliminar (visible al hover) -->
                <button 
                    class="opacity-0 group-hover:opacity-100 transition-opacity absolute right-2 top-2 text-red-400 hover:text-red-300 p-1 rounded hover:bg-red-900/20"
                    data-delete-id="${session.id}"
                    title="Eliminar sesión"
                >
                    <i class="ph ph-trash text-sm"></i>
                </button>
            </div>
        `;

        // Event listener para restaurar sesión
        const clickableArea = item.querySelector('[data-session-id]');
        clickableArea.addEventListener('click', () => restoreSession(session.id));

        // Event listener para eliminar sesión
        const deleteBtn = item.querySelector('[data-delete-id]');
        deleteBtn.addEventListener('click', async (e) => {
            e.stopPropagation(); // Evitar que se active el click de restaurar

            if (confirm(`¿Estás seguro de eliminar la sesión "${session.title_preview}"?`)) {
                try {
                    await deleteSession(session.id);
                    // Recargar el historial
                    loadHistory();
                } catch (error) {
                    alert('Error al eliminar la sesión: ' + error.message);
                }
            }
        });

        historyList.appendChild(item);
    });
}
