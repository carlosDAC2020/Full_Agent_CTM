import { mockDB } from '../data/mocks.js';
import { store } from '../data/store.js';

export function openDropdown() {
    const el = document.getElementById('dropdown-options');
    if (el) el.classList.remove('hidden');
}

export function filterOptions() {
    const opts = document.getElementById('dropdown-options');
    // En el futuro, esto podría filtrar real
    opts.innerHTML = `
        <div onclick="selectOption('minciencias')" class="px-4 py-3 hover:bg-blue-50 cursor-pointer flex items-center gap-3 border-l-4 border-transparent hover:border-cotecmar-light">
            <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center"><i class="ph ph-atom"></i></div>
            <div><div class="font-bold text-gray-800 text-sm">Convocatoria 966 Colombia Inteligente</div><div class="text-xs text-gray-400">IA, Cuántica</div></div>
        </div>
    `;
    opts.classList.remove('hidden');
}

export function selectOption(val) {
    store.selectedValue = val;
    document.getElementById('search-input').value = mockDB[val].title;
    document.getElementById('dropdown-options').classList.add('hidden');

    // Show preview
    document.getElementById('prev-title').innerText = mockDB[val].title;
    document.getElementById('prev-desc').innerText = mockDB[val].objective;
    document.getElementById('preview-panel').classList.remove('hidden');
}
