import { fetchSessions, deleteSession } from '../api/sessions.js';
import { restoreSession } from './wizard.js'; // Import logic
import { store } from '../data/store.js';

export function toggleSidebar() {
    const sb = document.getElementById('sidebar');
    if (!sb) return;
    sb.classList.toggle('w-64');
    sb.classList.toggle('w-0');
    sb.classList.toggle('p-0');
}

// Mapeo de step_type a nombres amigables y colores
const STEP_INFO = {
    'ingest': { name: 'Evaluación', color: 'bg-blue-500/90', icon: 'ph-file-magnifying-glass' },
    'proposal_ideas': { name: 'Ideas', color: 'bg-yellow-500/90', icon: 'ph-lightbulb' },
    'project_idea': { name: 'Esquema', color: 'bg-purple-500/90', icon: 'ph-file-text' },
    'generate_project': { name: 'Final', color: 'bg-green-500/90', icon: 'ph-check-circle' }
};

export async function loadHistory(activeSessionId = null) {
    const historyList = document.getElementById('history-list');
    if (!historyList) return;

    // Use passed ID or fallback to store
    const currentId = activeSessionId || store.sessionId;

    // Loading state (only if empty)
    if (historyList.children.length === 0) {
        historyList.innerHTML = '<div class="text-xs text-blue-300/60 px-3 py-2 italic">Cargando historial...</div>';
    }

    const sessions = await fetchSessions();
    historyList.innerHTML = '';

    if (sessions.length === 0) {
        historyList.innerHTML = '<div class="text-xs text-blue-300/60 px-3 py-2 italic">No hay historial reciente</div>';
        return;
    }

    sessions.forEach(session => {
        const item = document.createElement('div');
        const date = session.created_at ? new Date(session.created_at).toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit' }) : '--/--';
        const isActive = session.id === currentId;

        // Obtener información del paso
        const stepInfo = STEP_INFO[session.last_step] || { name: 'Iniciado', color: 'bg-gray-500/90', icon: 'ph-circle-dashed' };

        item.className = "group relative mb-1.5";

        // Active State Styling
        const activeClasses = isActive
            ? "bg-blue-800/40 border-l-4 border-l-cotecmar-light border-y border-r border-y-blue-500/30 border-r-blue-500/30 shadow-md"
            : "hover:bg-blue-900/30 border border-transparent hover:border-blue-700/30";

        item.innerHTML = `
            <div class="relative px-3 py-3 rounded-r-lg ${isActive ? 'rounded-l-sm' : 'rounded-lg'} transition-all duration-200 cursor-pointer ${activeClasses}">
                <!-- Área clickeable para restaurar -->
                <div class="pr-8" data-session-id="${session.id}">
                    <!-- Título -->
                    <div class="text-xs font-semibold ${isActive ? 'text-white' : 'text-blue-50'} leading-tight mb-2 group-hover:text-white transition-colors line-clamp-2">
                        ${session.title_preview || 'Nueva Sesión'}
                    </div>
                    
                    <!-- Metadata row -->
                    <div class="flex items-center gap-2 flex-wrap">
                        <!-- Badge del paso -->
                        <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold text-white ${stepInfo.color} shadow-sm">
                            <i class="ph-fill ${stepInfo.icon}"></i>
                            ${stepInfo.name}
                        </span>
                        
                        <!-- Fecha -->
                        <span class="text-[10px] text-blue-300/70 font-medium">
                            <i class="ph ph-calendar-blank text-[9px]"></i>
                            ${date}
                        </span>
                    </div>
                </div>
                
                <!-- Botón eliminar (visible al hover) -->
                <button 
                    class="absolute right-2 top-2 opacity-0 group-hover:opacity-100 transition-all duration-200 text-red-400 hover:text-red-300 hover:scale-110 p-1.5 rounded-md hover:bg-red-900/30"
                    data-delete-id="${session.id}"
                    title="Eliminar sesión"
                >
                    <i class="ph-fill ph-trash text-sm"></i>
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
