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

// Global Filter Setters
export function setStatusFilter(value) {
    store.statusFilter = value;
    updatePillStyles('status-pill', value);
    filterOptions();
}

export function setCategoryFilter(value) {
    store.categoryFilter = value;
    updatePillStyles('category-pill', value);
    filterOptions();
}

function updatePillStyles(pillClass, activeValue) {
    const pills = document.querySelectorAll(`.${pillClass}`);
    pills.forEach(pill => {
        const onclick = pill.getAttribute('onclick');
        if (onclick && onclick.includes(`'${activeValue}'`)) {
            pill.classList.remove('border-gray-200', 'text-gray-500');
            pill.classList.add('border-blue-200', 'bg-blue-50', 'text-cotecmar-mid', 'active-filter', 'shadow-blue-900/5');
        } else {
            pill.classList.remove('border-blue-200', 'bg-blue-50', 'text-cotecmar-mid', 'active-filter', 'shadow-blue-900/5');
            pill.classList.add('border-gray-200', 'text-gray-500');
        }
    });
}

async function refreshConvocatorias() {
    try {
        const raw = await getConvocatorias();
        // User request: "no traigas eventos"
        store.convocatorias = raw.filter(c => {
            const type = (c.type || '').toLowerCase();
            const title = (c.title || '').toLowerCase();
            const desc = (c.description || '').toLowerCase();
            return !type.includes('evento') && !title.includes('evento') && !desc.includes('evento');
        });

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
    const periods = [...new Set(store.convocatorias.map(c => {
        const date = c.deadline || c.fecha_inicio || c.fecha_cierre || c.created_at;
        return date ? new Date(date).getFullYear() : null;
    }).filter(Boolean))].sort((a, b) => b - a);

    const periodSelect = document.getElementById('filter-period');
    if (periodSelect) {
        periodSelect.innerHTML = '<option value="">Periodo</option>' +
            periods.map(p => `<option value="${p}">${p}</option>`).join('');
    }
}

export function filterOptions() {
    const query = document.getElementById('search-input').value.toLowerCase();
    const status = store.statusFilter;
    const category = store.categoryFilter;
    const period = document.getElementById('filter-period').value;
    const { convocatoriasList } = getElements();

    const now = new Date();

    const filtered = store.convocatorias.filter(c => {
        // Query search
        const matchesQuery = c.title.toLowerCase().includes(query) ||
            (c.description && c.description.toLowerCase().includes(query)) ||
            (c.keywords && c.keywords.some(k => k.toLowerCase().includes(query)));

        // Status Filter
        let matchesStatus = true;
        const deadline = c.deadline ? new Date(c.deadline) : null;
        if (status === 'active') {
            matchesStatus = !deadline || deadline >= now;
        } else if (status === 'closed') {
            matchesStatus = deadline && deadline < now;
        }

        // Category Filter
        let matchesCategory = true;
        const type = (c.type || '').toLowerCase();
        if (category === 'nac') {
            matchesCategory = type.includes('nac');
        } else if (category === 'int') {
            matchesCategory = type.includes('int');
        }

        // Period Filter
        const cDate = c.deadline || c.fecha_inicio || c.fecha_cierre || c.created_at;
        const matchesPeriod = !period || (cDate && new Date(cDate).getFullYear().toString() === period);

        return matchesQuery && matchesStatus && matchesCategory && matchesPeriod;
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
        const date = c.deadline ? new Date(c.deadline).toLocaleDateString('es-ES', { day: '2-digit', month: 'short' }) : 'S/F';

        return `
            <div onclick="selectOption(${c.id})" class="p-4 rounded-2xl border ${isSelected ? 'border-cotecmar-light bg-blue-50/80 shadow-md transform scale-[1.02]' : 'border-gray-100 bg-white hover:border-gray-300 hover:shadow-sm'} cursor-pointer transition-all duration-300 group">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl ${isSelected ? 'bg-cotecmar-dark text-white' : 'bg-blue-50 text-cotecmar-light group-hover:bg-blue-100'} flex items-center justify-center transition-colors shadow-sm">
                        <i class="ph ph-article text-lg"></i>
                    </div>
                    <div class="flex-1 overflow-hidden">
                        <div class="font-bold text-gray-800 text-[11px] truncate leading-tight">${c.title}</div>
                        <div class="flex items-center gap-2 mt-1">
                            <span class="text-[9px] text-gray-400 font-medium">${c.source || 'Fuente'}</span>
                            <span class="w-1 h-1 bg-gray-200 rounded-full"></span>
                            <span class="text-[9px] text-orange-500 font-bold uppercase">${date}</span>
                        </div>
                    </div>
                    ${isSelected ? '<i class="ph ph-check-circle-fill text-cotecmar-light text-lg"></i>' : '<i class="ph ph-caret-right text-gray-300 group-hover:text-cotecmar-light transition-colors"></i>'}
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
