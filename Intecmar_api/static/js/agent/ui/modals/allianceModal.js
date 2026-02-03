import { store } from '../../data/store.js';
import { uploadAllianceLogo, getPosterHistory, applyLogos } from '../../api/agent.js';
import { getAssetUrl } from '../common.js';

// State local del modal
let localAlliances = {
    executor: { name: '', logo: '' },
    coexecutors: [],
    collaborators: []
};

// Exponer funciones globales
window.openAllianceModal = openAllianceModal;
window.closeAllianceModal = closeAllianceModal;
window.addModalAllianceItem = addModalAllianceItem;
window.removeModalAllianceItem = removeModalAllianceItem;
window.handleModalLogoUpload = handleModalLogoUpload;
window.updateLocalAllianceName = updateLocalAllianceName;
window.saveAllianceChanges = saveAllianceChanges;


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
               oninput="updateLocalAllianceName('${type}', ${index}, this.value)">
        
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


export function updateLocalAllianceName(type, index, value) {
    if (type === 'executor') {
        localAlliances.executor.name = value;
    } else if (type === 'coexecutor') {
        localAlliances.coexecutors[index].name = value;
    } else if (type === 'collaborator') {
        localAlliances.collaborators[index].name = value;
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

    // 2. Identify base image (Always the latest/current for this modal)
    let baseImagePath = '';
    const history = store.finalResult?.generation_history || [];
    if (history.length > 0) {
        const latest = history[history.length - 1];
        baseImagePath = latest.base_image_path || latest.poster_path;
    } else {
        baseImagePath = store.finalResult?.docs?.poster_image_path;
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
            console.log("✅ Apply logos success, updating store...");

            // Defensive: ensure store.finalResult exists
            if (!store.finalResult) {
                console.warn("⚠️ store.finalResult was null, initializing...");
                store.finalResult = {};
            }

            // Update store
            if (!store.finalResult.report_components) store.finalResult.report_components = {};
            store.finalResult.report_components.general_info = newGeneralInfo;

            // Update docs poster path
            if (!store.finalResult.docs_paths) store.finalResult.docs_paths = {};
            store.finalResult.docs_paths.poster_image_path = result.poster_path;

            // Sync store.currentSelectedIdea (Crucial for Step 3 synchronization)
            if (store.currentSelectedIdea) {
                console.log("🔄 [allianceModal.js] Syncing store.currentSelectedIdea for Step 3...");
                store.currentSelectedIdea.executor_entity = newGeneralInfo.executor_entity;
                store.currentSelectedIdea.executor_entity_logo = newGeneralInfo.executor_entity_logo;
                store.currentSelectedIdea.coejecutors_entities = newGeneralInfo.coejecutors_entities || [];
                store.currentSelectedIdea.coejecutors_entities_logos = newGeneralInfo.coejecutors_entities_logos || [];
                store.currentSelectedIdea.collaborators_entities = newGeneralInfo.collaborators_entities || [];
                store.currentSelectedIdea.collaborators_entities_logos = newGeneralInfo.collaborators_entities_logos || [];
            } else {
                console.warn("⚠️ [allianceModal.js] store.currentSelectedIdea is null, cannot sync.");
            }

            // Append history item
            if (!store.finalResult.generation_history) store.finalResult.generation_history = [];
            store.finalResult.generation_history.push(result.new_history_item);

            console.log("📢 Dispatching poster-updated event with:", store.finalResult);

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
