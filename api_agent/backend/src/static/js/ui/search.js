import { store } from '../data/store.js';
import { getConvocatorias } from '../api/agent.js';
import { getElements } from './common.js';

// Initial Load
// Note: This script might be loaded before the UI is fully ready if not careful
// But usually main.js handles it. Let's export an init function.

export async function initInitialView() {
    if (store.convocatorias.length === 0) {
        await refreshConvocatorias();
    }
}

async function refreshConvocatorias() {
    try {
        store.convocatorias = await getConvocatorias();
        populateFilters();
        filterOptions();
    } catch (err) {
        console.error("Failed to fetch convocatorias", err);
        const { convocatoriasList } = getElements();
        if (convocatoriasList) {
            convocatoriasList.innerHTML = '<div class="text-red-500 text-xs p-4 text-center font-bold">Error al cargar datos</div>';
        }
    }
}

function populateFilters() {
    const types = [...new Set(store.convocatorias.map(c => c.type).filter(Boolean))];
    const sources = [...new Set(store.convocatorias.map(c => c.source).filter(Boolean))];
    const periods = [...new Set(store.convocatorias.map(c => {
        const date = c.deadline || c.fecha_inicio || c.fecha_cierre || c.created_at;
        return date ? new Date(date).getFullYear() : null;
    }).filter(Boolean))].sort((a, b) => b - a);

    const typeSelect = document.getElementById('filter-type');
    const sourceSelect = document.getElementById('filter-source');
    const periodSelect = document.getElementById('filter-period');

    if (typeSelect) {
        typeSelect.innerHTML = '<option value="">Tipos</option>' +
            types.map(t => `<option value="${t}">${t}</option>`).join('');
    }
    if (sourceSelect) {
        sourceSelect.innerHTML = '<option value="">Fuentes</option>' +
            sources.map(s => `<option value="${s}">${s}</option>`).join('');
    }
    if (periodSelect) {
        periodSelect.innerHTML = '<option value="">Periodo</option>' +
            periods.map(p => `<option value="${p}">${p}</option>`).join('');
    }
}

export function filterOptions() {
    const query = document.getElementById('search-input').value.toLowerCase();
    const type = document.getElementById('filter-type').value;
    const source = document.getElementById('filter-source').value;
    const period = document.getElementById('filter-period').value;
    const { convocatoriasList } = getElements();

    const filtered = store.convocatorias.filter(c => {
        const matchesQuery = c.title.toLowerCase().includes(query) ||
            (c.description && c.description.toLowerCase().includes(query)) ||
            (c.keywords && c.keywords.some(k => k.toLowerCase().includes(query)));
        const matchesType = !type || c.type === type;
        const matchesSource = !source || c.source === source;
        const cDate = c.deadline || c.fecha_inicio || c.fecha_cierre || c.created_at;
        const matchesPeriod = !period || (cDate && new Date(cDate).getFullYear().toString() === period);

        return matchesQuery && matchesType && matchesSource && matchesPeriod;
    });

    if (filtered.length === 0) {
        convocatoriasList.innerHTML = `
            <div class="flex flex-col items-center justify-center p-8 text-gray-400 text-center">
                <i class="ph ph-mask-sad text-3xl mb-2"></i>
                <p class="text-[10px] font-bold uppercase">No se encontraron resultados</p>
            </div>
        `;
        return;
    }

    convocatoriasList.innerHTML = filtered.map(c => {
        const isSelected = store.selectedValue === c.id;
        return `
            <div onclick="selectOption(${c.id})" class="p-4 rounded-2xl border ${isSelected ? 'border-cotecmar-light bg-blue-50 shadow-md transform scale-[1.02]' : 'border-gray-100 bg-white hover:border-gray-300 hover:shadow-sm'} cursor-pointer transition-all duration-300 group">
                <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg ${isSelected ? 'bg-cotecmar-dark text-white' : 'bg-gray-100 text-gray-400 group-hover:bg-blue-100 group-hover:text-cotecmar-light'} flex items-center justify-center transition-colors">
                        <i class="ph ph-article"></i>
                    </div>
                    <div class="flex-1 overflow-hidden">
                        <div class="font-bold text-gray-800 text-xs truncate">${c.title}</div>
                        <div class="text-[10px] text-gray-400 mt-0.5">${c.source || 'Fuente N/A'} • ${c.type || 'Tipo N/A'}</div>
                    </div>
                    ${isSelected ? '<i class="ph ph-check-circle-fill text-cotecmar-light"></i>' : ''}
                </div>
            </div>
        `;
    }).join('');
}

export function selectOption(id) {
    const item = store.convocatorias.find(c => c.id === id);
    if (!item) return;

    store.selectedValue = id;
    store.selectedCallText = `Título: ${item.title}\n\nDescripción: ${item.description || ''}\n\nObjetivo: ${item.objective || item.description || ''}\n\nRequisitos: ${JSON.stringify(item.requisitos || [])}`;

    const { noSelectionState, selectionDetails } = getElements();

    // Hide welcome, show details
    if (noSelectionState) noSelectionState.classList.add('hidden');
    if (selectionDetails) {
        selectionDetails.classList.remove('hidden');
        selectionDetails.classList.add('animate-slide-up');
    }

    // Populate Right Panel
    document.getElementById('prev-title').innerText = item.title;
    document.getElementById('prev-desc').innerText = item.description || item.objective || "Sin descripción disponible.";
    document.getElementById('prev-type').innerText = item.type || 'N/A';
    document.getElementById('prev-source').innerText = item.source || 'N/A';

    // Deadline / Date
    const deadlineEl = document.getElementById('prev-deadline');
    if (deadlineEl) {
        const dateStr = item.deadline || item.fecha_cierre || item.created_at;
        if (dateStr) {
            const date = new Date(dateStr);
            deadlineEl.innerText = date.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' }).toUpperCase();
            deadlineEl.classList.remove('hidden');
        } else {
            deadlineEl.classList.add('hidden');
        }
    }

    // Refresh list to show selection highlight
    filterOptions();
}

// Fallback for openDropdown if still called somewhere
export function openDropdown() { }
