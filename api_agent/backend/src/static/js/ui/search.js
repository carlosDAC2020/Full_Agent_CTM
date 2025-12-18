import { store } from '../data/store.js';
import { getConvocatorias } from '../api/agent.js';

export async function openDropdown() {
    const el = document.getElementById('dropdown-options');
    if (el) {
        el.classList.remove('hidden');
        if (store.convocatorias.length === 0) {
            await refreshConvocatorias();
        }
        filterOptions();
    }
}

async function refreshConvocatorias() {
    try {
        store.convocatorias = await getConvocatorias();
    } catch (err) {
        console.error("Failed to fetch convocatorias", err);
    }
}

export function filterOptions() {
    const query = document.getElementById('search-input').value.toLowerCase();
    const opts = document.getElementById('dropdown-options');

    const filtered = store.convocatorias.filter(c =>
        c.title.toLowerCase().includes(query) ||
        (c.description && c.description.toLowerCase().includes(query)) ||
        (c.keywords && c.keywords.some(k => k.toLowerCase().includes(query)))
    );

    if (filtered.length === 0) {
        opts.innerHTML = '<div class="px-4 py-3 text-gray-500 text-sm">No se encontraron convocatorias</div>';
        return;
    }

    opts.innerHTML = filtered.map(c => `
        <div onclick="selectOption(${c.id})" class="px-4 py-3 hover:bg-blue-50 cursor-pointer flex items-center gap-3 border-l-4 border-transparent hover:border-cotecmar-light">
            <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center"><i class="ph ph-atom"></i></div>
            <div>
                <div class="font-bold text-gray-800 text-sm">${c.title}</div>
                <div class="text-xs text-gray-400">${(c.keywords || []).slice(0, 3).join(', ')}</div>
            </div>
        </div>
    `).join('');

    opts.classList.remove('hidden');
}

export function selectOption(id) {
    const item = store.convocatorias.find(c => c.id === id);
    if (!item) return;

    store.selectedValue = id;
    // Construct the full text from available fields
    store.selectedCallText = `Título: ${item.title}\n\nDescripción: ${item.description || ''}\n\nObjetivo: ${item.objective || ''}\n\nRequisitos: ${JSON.stringify(item.requisitos || [])}`;

    document.getElementById('search-input').value = item.title;
    document.getElementById('dropdown-options').classList.add('hidden');

    // Show preview
    document.getElementById('prev-title').innerText = item.title;
    document.getElementById('prev-desc').innerText = item.description || item.objective || "Sin descripción";
    document.getElementById('preview-panel').classList.remove('hidden');

    // As per user request: "intenta q cuando se seleciona alguna convocatriia se mantenga lo de ingresar archviso"
    // The preview panel might be hiding something or we need to ensure the upload area is still reachable.
    // Looking at the layout, preview-panel is usually below or replacing some part.
}
