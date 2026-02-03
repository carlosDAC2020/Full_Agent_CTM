import { store } from '../../data/store.js';
import { uploadAllianceLogo, getPosterHistory, applyLogos } from '../../api/agent.js';
import { getAssetUrl } from '../common.js';

// State local del modal
let localAlliances = {
    executor: { name: '', logo: '' },
    coexecutors: [],
    collaborators: []
};
let baseImageMode = 'current'; // 'current' or 'history'
let selectedBaseImagePath = null;

// Exponer funciones globales
window.openAllianceModal = openAllianceModal;
window.closeAllianceModal = closeAllianceModal;
window.addModalAllianceItem = addModalAllianceItem;
window.removeModalAllianceItem = removeModalAllianceItem;
window.handleModalLogoUpload = handleModalLogoUpload;
window.saveAllianceChanges = saveAllianceChanges;
window.toggleBaseHistory = toggleBaseHistory;
window.selectBaseImage = selectBaseImage;


export function openAllianceModal() {
    const modal = document.getElementById('alliance-modal');
    modal.classList.remove('hidden');

    // Cargar datos actuales desde store
    // data source: store.finalResult.report_components.general_info (or selected_idea as fallback)
    const data = store.finalResult || {};
    const generalInfo = data.report_components?.general_info ||
        data.selected_idea || {}; // Fallback logic

    // Initialize local state
    localAlliances.executor = {
        name: generalInfo.executor_entity || '',
        logo: generalInfo.executor_entity_logo || ''
    };

    // Coexecutors
    localAlliances.coexecutors = [];
    if (generalInfo.coejecutors_entities && Array.isArray(generalInfo.coejecutors_entities)) {
        generalInfo.coejecutors_entities.forEach((name, idx) => {
            const logo = (generalInfo.coejecutors_entities_logos && generalInfo.coejecutors_entities_logos[idx]) || '';
            localAlliances.coexecutors.push({ name, logo });
        });
    }

    // Collaborators
    localAlliances.collaborators = [];
    if (generalInfo.collaborators_entities && Array.isArray(generalInfo.collaborators_entities)) {
        generalInfo.collaborators_entities.forEach((name, idx) => {
            const logo = (generalInfo.collaborators_entities_logos && generalInfo.collaborators_entities_logos[idx]) || '';
            localAlliances.collaborators.push({ name, logo });
        });
    }

    // Reset History Mode
    baseImageMode = 'current';
    selectedBaseImagePath = null;
    document.querySelector('input[name="apply-mode"][value="current"]').checked = true;
    document.getElementById('base-history-selector').classList.add('hidden');

    // Render Form
    renderModalForm();
}

export function closeAllianceModal() {
    document.getElementById('alliance-modal').classList.add('hidden');
}

function renderModalForm() {
    // 1. Executor
    const execNameInput = document.getElementById('modal-executor-name');
    const execPreview = document.getElementById('modal-executor-preview');
    const execPlaceholder = document.getElementById('modal-executor-placeholder');

    execNameInput.value = localAlliances.executor.name;

    if (localAlliances.executor.logo) {
        execPreview.src = getAssetUrl(localAlliances.executor.logo);
        execPreview.classList.remove('hidden');
        execPlaceholder.classList.add('hidden');
    } else {
        execPreview.src = '';
        execPreview.classList.add('hidden');
        execPlaceholder.classList.remove('hidden');
    }

    // 2. Coexecutors
    const coexecList = document.getElementById('modal-coexecutors-list');
    coexecList.innerHTML = '';
    localAlliances.coexecutors.forEach((item, index) => {
        coexecList.appendChild(createAllianceItemRow('coexecutor', index, item));
    });

    // 3. Collaborators
    const collabList = document.getElementById('modal-collaborators-list');
    collabList.innerHTML = '';
    localAlliances.collaborators.forEach((item, index) => {
        collabList.appendChild(createAllianceItemRow('collaborator', index, item));
    });
}

function createAllianceItemRow(type, index, item) {
    const div = document.createElement('div');
    div.className = "flex gap-3 items-center bg-gray-50 border border-gray-100 p-2 rounded-xl group";

    // Logo Upload Logic
    const hasLogo = !!item.logo;
    const logoUrl = item.logo ? getAssetUrl(item.logo) : '';

    div.innerHTML = `
        <div class="w-12 h-12 bg-white border border-gray-200 rounded-lg flex items-center justify-center relative overflow-hidden flex-shrink-0 cursor-pointer hover:border-blue-400 transition-colors">
            <img class="${hasLogo ? '' : 'hidden'} w-full h-full object-contain p-1" src="${logoUrl}" id="preview-${type}-${index}">
            <i class="ph ph-upload-simple text-gray-400 ${hasLogo ? 'hidden' : ''}" id="icon-${type}-${index}"></i>
            <input type="file" accept="image/*" class="absolute inset-0 opacity-0 z-10 cursor-pointer" 
                   onchange="handleModalLogoUpload(this, '${type}', ${index})">
        </div>
        <input type="text" value="${item.name}" placeholder="Nombre entidad..." 
               class="flex-1 bg-transparent border-none outline-none text-sm font-medium text-gray-700 placeholder-gray-400"
               oninput="localAlliances.${type === 'coexecutor' ? 'coexecutors' : 'collaborators'}[${index}].name = this.value">
        
        <button onclick="removeModalAllianceItem('${type}', ${index})" class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors">
            <i class="ph ph-trash"></i>
        </button>
    `;
    return div;
}

export function addModalAllianceItem(type) {
    if (type === 'coexecutor') {
        localAlliances.coexecutors.push({ name: '', logo: '' });
    } else {
        localAlliances.collaborators.push({ name: '', logo: '' });
    }
    renderModalForm();
}

export function removeModalAllianceItem(type, index) {
    if (type === 'coexecutor') {
        localAlliances.coexecutors.splice(index, 1);
    } else {
        localAlliances.collaborators.splice(index, 1);
    }
    renderModalForm();
}

export async function handleModalLogoUpload(input, type, index = null) {
    if (!input.files || !input.files[0]) return;
    const file = input.files[0];

    // Show loading state if needed
    // ...

    try {
        const result = await uploadAllianceLogo(store.sessionId, file);

        if (type === 'executor') {
            localAlliances.executor.logo = result.path;
        } else if (type === 'coexecutor') {
            localAlliances.coexecutors[index].logo = result.path;
        } else if (type === 'collaborator') {
            localAlliances.collaborators[index].logo = result.path;
        }

        renderModalForm();

    } catch (error) {
        console.error("Upload failed", error);
        alert("Error subiendo logo: " + error.message);
    }
}

export function toggleBaseHistory(show) {
    baseImageMode = show ? 'history' : 'current';
    const container = document.getElementById('base-history-selector');
    if (show) {
        container.classList.remove('hidden');
        loadBaseImageHistory();
    } else {
        container.classList.add('hidden');
    }
}

async function loadBaseImageHistory() {
    const grid = document.getElementById('base-history-grid');
    grid.innerHTML = '<div class="col-span-3 text-center text-gray-400 py-4"><i class="ph ph-spinner animate-spin"></i> Cargando historial...</div>';

    try {
        const history = await getPosterHistory(store.sessionId);
        // Filter items that have base_image_path
        const validItems = history.filter(item => item.base_image_path); // Or base_image_url if processed

        grid.innerHTML = '';

        if (validItems.length === 0) {
            grid.innerHTML = '<div class="col-span-3 text-center text-xs text-gray-400 py-2">No se encontraron versiones anteriores.</div>';
            return;
        }

        // Reverse to show newest first
        validItems.reverse().forEach((item, idx) => {
            const div = document.createElement('div');
            const isActive = selectedBaseImagePath === item.base_image_path;
            div.className = `relative aspect-[2/3] rounded-lg overflow-hidden border-2 cursor-pointer transition-all ${isActive ? 'border-blue-500 ring-2 ring-blue-500/20' : 'border-gray-200 hover:border-blue-300'}`;
            div.onclick = () => selectBaseImage(item.base_image_path, div);

            // Check if url or path
            const url = item.base_image_url || getAssetUrl(item.base_image_path);

            div.innerHTML = `
                <img src="${url}" class="w-full h-full object-cover">
                <div class="absolute bottom-0 left-0 right-0 bg-black/60 text-white text-[9px] px-2 py-1 truncate">
                    ${new Date(item.timestamp).toLocaleTimeString()}
                </div>
                ${isActive ? '<div class="absolute top-2 right-2 bg-blue-500 text-white w-5 h-5 rounded-full flex items-center justify-center"><i class="ph-bold ph-check text-xs"></i></div>' : ''}
             `;
            grid.appendChild(div);
        });

    } catch (e) {
        console.error(e);
        grid.innerHTML = '<div class="col-span-3 text-center text-red-400 text-xs">Error cargando historial</div>';
    }
}

export function selectBaseImage(path, element) {
    selectedBaseImagePath = path;
    // Update visuals
    const grid = document.getElementById('base-history-grid');
    Array.from(grid.children).forEach(child => {
        child.classList.remove('border-blue-500', 'ring-2', 'ring-blue-500/20');
        child.classList.add('border-gray-200');
        // Remove check icon
        const icon = child.querySelector('.ph-check')?.parentNode;
        if (icon) icon.remove();
    });

    element.classList.remove('border-gray-200');
    element.classList.add('border-blue-500', 'ring-2', 'ring-blue-500/20');
    // Add check icon
    if (!element.querySelector('.ph-check')) {
        const iconDiv = document.createElement('div');
        iconDiv.className = "absolute top-2 right-2 bg-blue-500 text-white w-5 h-5 rounded-full flex items-center justify-center";
        iconDiv.innerHTML = '<i class="ph-bold ph-check text-xs"></i>';
        element.appendChild(iconDiv);
    }
}

async function saveAllianceChanges() {
    // 1. Construct new ReportSchema-like object
    const newGeneralInfo = {
        // Preserve other fields if needed, but for now we focus on alliances
        // We might need to merge with existing general_info
        ...((store.finalResult?.report_components?.general_info) || {}),

        executor_entity: localAlliances.executor.name,
        executor_entity_logo: localAlliances.executor.logo,

        coejecutors_entities: localAlliances.coexecutors.map(i => i.name),
        coejecutors_entities_logos: localAlliances.coexecutors.map(i => i.logo),

        collaborators_entities: localAlliances.collaborators.map(i => i.name),
        collaborators_entities_logos: localAlliances.collaborators.map(i => i.logo)
    };

    // 2. Identify base image
    let baseImagePath = '';

    if (baseImageMode === 'history' && selectedBaseImagePath) {
        baseImagePath = selectedBaseImagePath;
    } else {
        // Current logic
        const history = store.finalResult?.generation_history || [];
        if (history.length > 0) {
            // Use latest base image
            const latest = history[history.length - 1];
            baseImagePath = latest.base_image_path || latest.poster_path;
        } else {
            // Fallback from main docs
            baseImagePath = store.finalResult?.docs?.poster_image_path;
        }
    }

    if (!baseImagePath) {
        alert("No se encontró imagen base para aplicar logos. Selecciona una del historial.");
        return;
    }

    // 3. Call API
    const btn = document.querySelector('#alliance-modal button[onclick="saveAllianceChanges()"]');
    const originalText = btn.innerHTML;
    btn.innerHTML = `<i class="ph ph-spinner animate-spin"></i> Aplicando...`;
    btn.disabled = true;

    try {
        const payload = {
            session_id: store.sessionId,
            base_image_path: baseImagePath,
            report_components: {
                general_info: newGeneralInfo
                // other components not needed for applying logos usually? 
                // apply_logos_to_image uses 'report_components.general_info' mostly.
            }
        };

        const result = await applyLogos(payload);

        if (result.status === 'success') {
            // Update store
            if (!store.finalResult.report_components) store.finalResult.report_components = {};
            store.finalResult.report_components.general_info = newGeneralInfo;

            // Update docs poster path
            if (!store.finalResult.docs) store.finalResult.docs = {};
            store.finalResult.docs.poster_image_path = result.poster_path;

            // Append history item
            if (!store.finalResult.generation_history) store.finalResult.generation_history = [];
            store.finalResult.generation_history.push(result.new_history_item);

            // Refresh View via Event to avoid circular dependency
            window.dispatchEvent(new CustomEvent('poster-updated', { detail: store.finalResult }));

            closeAllianceModal();
        }

    } catch (e) {
        console.error(e);
        alert("Error aplicando cambios: " + e.message);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}
