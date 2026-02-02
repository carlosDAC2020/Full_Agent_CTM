import { store } from '../../data/store.js';
import { generateIdeas } from '../../api/agent.js';
import { pollTask } from '../../api/tasks.js';
import { getElements, updateStepper } from '../common.js';
import { loadHistory } from '../sidebar.js';

// Paso 2: Generar Ideas
export async function goToStep2(thematicLine = null, methodology = null) {
    const { step1, loader, loaderText, step2 } = getElements();

    console.log('🚀 goToStep2 RECEIVED args:', { thematicLine, methodology });
    console.log('🚀 goToStep2 STORE values:', {
        selectedThematicLine: store.selectedThematicLine,
        selectedMethodology: store.selectedMethodology
    });

    // FIX: Priorizar store como fuente de verdad, luego argumentos, luego DOM
    if (!thematicLine) {
        thematicLine = store.selectedThematicLine;
    }
    if (!methodology) {
        methodology = store.selectedMethodology;
    }

    // Fallback final al DOM solo si todo lo demás falló
    if (!thematicLine) {
        const domThematic = document.getElementById('config-thematic-line');
        thematicLine = domThematic?.value || "General / No especificada";
    }
    if (!methodology) {
        const domMethod = document.getElementById('config-methodology');
        methodology = domMethod?.value || "No especificada";
    }

    console.log('🚀 goToStep2 FINAL values to send:', { thematicLine, methodology });

    // UI Transition
    step1.classList.add('hidden');
    loader.classList.remove('hidden');

    let loadingMsg = "Analizando oportunidades y generando ideas innovadoras...";
    if (methodology && methodology !== "No especificada") {
        loadingMsg = `Generando ideas bajo el marco ${methodology}...`;
    }
    loaderText.innerText = loadingMsg;
    updateStepper(2);

    try {
        // 1. Start Generate Ideas Task
        const { task_id } = await generateIdeas(store.sessionId, thematicLine, methodology);

        // 2. Poll Task Progress
        pollTask(
            task_id,
            (message) => {
                loaderText.innerText = message || "Generando ideas...";
            },
            (result) => {
                // On Complete
                let data;
                try { data = typeof result.data === 'string' ? JSON.parse(result.data) : result.data; }
                catch (e) { console.error("Error parsing JSON", e); return; }

                renderIdeas(data);
                loader.classList.add('hidden');
                step2.classList.remove('hidden');
                loadHistory(store.sessionId); // Refresh status
            },
            (error) => {
                loaderText.innerText = "Error: " + error;
                loaderText.classList.add('text-red-500');
            }
        );

    } catch (err) {
        loaderText.innerText = "Error de conexión: " + err.message;
        loaderText.classList.add('text-red-500');
    }
}

export function renderIdeas(data) {
    const { ideasContainer } = getElements();
    ideasContainer.innerHTML = '';

    // Mostrar criterios seleccionados
    const thematicDisp = document.getElementById('display-selected-thematic');
    const methodologyDisp = document.getElementById('display-selected-methodology');

    console.log('👀 RenderIdeas - Received Data:', {
        selected_thematic_line: data?.selected_thematic_line,
        selected_methodology: data?.selected_methodology
    });

    if (thematicDisp) {
        thematicDisp.innerText = data?.selected_thematic_line || "General / No especificada";
    }
    if (methodologyDisp) {
        methodologyDisp.innerText = data?.selected_methodology || "No especificado";
    }

    // Data structure from backend: data.proposal_ideas.ideas (Array)
    const ideas = data?.proposal_ideas?.ideas || [];

    if (ideas.length === 0) {
        ideasContainer.innerHTML = '<p class="text-gray-500 italic col-span-2 text-center">No se generaron ideas. Intenta de nuevo.</p>';
        return;
    }

    ideas.forEach(idea => {
        // Map backend keys (idea_title) to internal if needed, or use directly
        // Backend: { idea_title, idea_description, idea_objectives: [] }

        const card = document.createElement('div');
        card.className = "bg-white p-5 rounded-xl border border-gray-200 hover:border-cotecmar-mid hover:shadow-lg transition-all cursor-pointer group relative";

        // Store for editing
        // Adapter for frontend structure expectation in openEditIdea
        // Store for editing
        // Adapter for frontend structure expectation in openEditIdea
        const ideaObj = {
            title: idea.idea_title,
            desc: idea.idea_description,
            objectives: idea.idea_specific_objectives || idea.idea_objectives || [], // Fallback por si cambia nombre en backend
            suggested_duration_months: idea.suggested_duration_months,
            general_objective: idea.idea_general_objective,
            // Alianzas
            executor_entity: idea.executor_entity,
            executor_entity_logo: idea.executor_entity_logo,
            coejecutors_entities: idea.coejecutors_entities,
            coejecutors_entities_logos: idea.coejecutors_entities_logos,
            collaborators_entities: idea.collaborators_entities,
            collaborators_entities_logos: idea.collaborators_entities_logos
        };

        card.onclick = () => openEditIdea(ideaObj);

        card.innerHTML = `
            <div class="flex justify-between items-start mb-2">
                <div class="font-bold text-gray-800 group-hover:text-cotecmar-mid transition-colors">${idea.idea_title}</div>
                <i class="ph ph-pencil-simple text-gray-300 group-hover:text-cotecmar-mid"></i>
            </div>
            <p class="text-xs text-gray-500 line-clamp-3">${idea.idea_description}</p>
        `;
        ideasContainer.appendChild(card);
    });
}

// --- Logic for Editing Ideas (Internal to Step 2) ---

// --- Logic for Editing Ideas (Internal to Step 2) ---

function openEditIdea(idea) {
    const { ideasContainer, ideaEditor } = getElements();
    store.currentSelectedIdea = idea;

    // Ocultar el banner de criterios, header y el grid de ideas
    const banner = document.getElementById('selected-criteria-banner');
    const header = document.getElementById('ideas-header');
    if (banner) banner.classList.add('hidden');
    if (header) header.classList.add('hidden');

    ideasContainer.classList.add('hidden');
    ideaEditor.classList.remove('hidden');

    document.getElementById('edit-title').value = idea.title || '';

    const descTextarea = document.getElementById('edit-desc');
    descTextarea.value = idea.desc || '';
    autoResizeTextarea(descTextarea);

    // Nuevo: Objetivo General
    const generalObjInput = document.getElementById('edit-general-objective');
    if (generalObjInput) {
        generalObjInput.value = idea.general_objective || '';
        autoResizeTextarea(generalObjInput);
    }

    // Nuevo: Duración
    document.getElementById('edit-duration').value = idea.suggested_duration_months || '';

    // Nuevo: Ejecutor
    document.getElementById('edit-executor').value = idea.executor_entity || '';
    if (idea.executor_entity_logo) {
        showPreview('executor', idea.executor_entity_logo);
        store.allianceLogos = store.allianceLogos || {};
        store.allianceLogos['executor'] = idea.executor_entity_logo;
    } else {
        clearLogo('executor', false);
    }

    // Clear and populate objectives
    document.getElementById('objectives-list').innerHTML = '';
    if (idea.objectives && Array.isArray(idea.objectives)) {
        idea.objectives.forEach(obj => addObjectiveInput(obj));
    } else {
        addObjectiveInput(''); // Start with one empty
    }

    // Nuevo: Poblar Coejecutores
    document.getElementById('coejecutors-list').innerHTML = '';
    if (idea.coejecutors_entities && Array.isArray(idea.coejecutors_entities)) {
        idea.coejecutors_entities.forEach((name, index) => {
            const logo = idea.coejecutors_entities_logos ? idea.coejecutors_entities_logos[index] : null;
            addAllianceInput('coejecutor', name, logo);
        });
    }

    // Nuevo: Poblar Colaboradores
    document.getElementById('collaborators-list').innerHTML = '';
    if (idea.collaborators_entities && Array.isArray(idea.collaborators_entities)) {
        idea.collaborators_entities.forEach((name, index) => {
            const logo = idea.collaborators_entities_logos ? idea.collaborators_entities_logos[index] : null;
            addAllianceInput('collaborator', name, logo);
        });
    }
}

export function cancelEdit() {
    const { ideasContainer, ideaEditor } = getElements();
    ideaEditor.classList.add('hidden');
    ideasContainer.classList.remove('hidden');

    // Mostrar de nuevo el banner de criterios y header
    const banner = document.getElementById('selected-criteria-banner');
    const header = document.getElementById('ideas-header');
    if (banner) banner.classList.remove('hidden');
    if (header) header.classList.remove('hidden');

    // Limpiar store temporal de logos para no afectar siguiente edición si se cancela?
    // Mejor mantener simple.
}

// Auto-resize textarea to fit content
function autoResizeTextarea(textarea) {
    if (!textarea) return;
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Initialize auto-resize on all textareas in the editor
function initAutoResizeTextareas() {
    const textareas = document.querySelectorAll('#idea-editor textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', () => autoResizeTextarea(textarea));
    });
}

// Dynamic Objectives Logic
export function addObjectiveInput(value = '') {
    const list = document.getElementById('objectives-list');
    const div = document.createElement('div');
    const index = list.children.length + 1;

    div.className = "flex gap-3 items-start group/item bg-gray-50 p-3 rounded-xl border-2 border-gray-200 hover:border-gray-300 transition-all";
    div.innerHTML = `
        <div class="flex-shrink-0 w-8 h-8 bg-cotecmar-mid/10 text-cotecmar-mid rounded-lg flex items-center justify-center font-bold text-sm mt-1">
            ${index}
        </div>
        <textarea 
            class="flex-1 bg-white border-2 border-gray-200 rounded-lg px-3 py-2.5 text-sm text-gray-700 leading-relaxed
                   focus:border-cotecmar-light focus:ring-4 focus:ring-cotecmar-light/20 outline-none transition-all
                   hover:border-gray-300 resize-none objective-textarea"
            rows="1"
            placeholder="Ej: Desarrollar un prototipo funcional con precisión del 85% en 12 meses...">${value}</textarea>
        <button 
            onclick="removeObjectiveInput(this)" 
            class="flex-shrink-0 text-gray-400 hover:text-red-500 hover:bg-red-50 p-2 rounded-lg opacity-0 group-hover/item:opacity-100 transition-all mt-1"
            title="Eliminar objetivo">
            <i class="ph-fill ph-trash text-lg"></i>
        </button>
    `;
    list.appendChild(div);

    // Auto-resize the textarea after adding
    const textarea = div.querySelector('textarea');
    if (textarea) {
        autoResizeTextarea(textarea);
        textarea.addEventListener('input', () => autoResizeTextarea(textarea));
    }

    renumberObjectives();
}

export function removeObjectiveInput(btn) {
    if (btn && btn.parentElement) btn.parentElement.remove();
    renumberObjectives();
}

function renumberObjectives() {
    const list = document.getElementById('objectives-list');
    const items = list.children;
    for (let i = 0; i < items.length; i++) {
        const numberBadge = items[i].querySelector('div');
        if (numberBadge) {
            numberBadge.textContent = i + 1;
        }
    }
}

// --- LOGICA DE ALIANZAS Y LOGOS (NUEVO) ---

// Subir logo
export async function handleLogoUpload(input, typeOrId) {
    const file = input.files[0];
    if (!file) return;

    // Mostrar loading o algo? Poner opacidad
    const previewImg = document.getElementById(`preview-${typeOrId}-logo`);
    if (previewImg) previewImg.style.opacity = '0.5';

    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_id', store.sessionId);

    try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch('/api/agent/upload-alliance-logo', {
            method: 'POST',
            headers: { ...(token && { 'Authorization': `Bearer ${token}` }) },
            body: formData
        });

        if (!response.ok) throw new Error("Error upload");

        const result = await response.json();

        // Guardar path en store temporal
        store.allianceLogos = store.allianceLogos || {};
        store.allianceLogos[typeOrId] = result.path; // Guardamos path relativo para guardar en DB

        // Mostrar preview
        showPreview(typeOrId, result.url); // URL para mostrar en img src

    } catch (e) {
        console.error("Error upload logo", e);
        alert("Error subiendo logo");
    } finally {
        if (previewImg) previewImg.style.opacity = '1';
    }
}

function showPreview(typeOrId, src) {
    // Si viene de DB (path minio), convertir a URL proxy si no lo es ya
    let url = src;
    if (!src.startsWith('http') && !src.startsWith('/api/')) {
        url = `/api/minio_agent/${src}`;
    }

    const img = document.getElementById(`preview-${typeOrId}-logo`);
    const container = document.getElementById(`preview-container-${typeOrId}`) || img.parentElement.parentElement.querySelector(`#preview-container-${typeOrId}`); // fallback busqueda

    // Caso especial para dinámicos que tienen estructura diferente o IDs directos
    // En dinamico: id="preview-{uniqueId}-logo", container es el padre (div relative)
    const dynamicContainer = document.getElementById(`preview-container-${typeOrId}`);

    if (img) {
        img.src = url;
        if (dynamicContainer) {
            dynamicContainer.classList.remove('hidden');
        } else {
            // Fallback para ejecutor static
            const staticContainer = document.getElementById(`preview-container-${typeOrId}`);
            if (staticContainer) staticContainer.classList.remove('hidden');
        }
    }
}

export function clearLogo(typeOrId, clearStore = true) {
    const container = document.getElementById(`preview-container-${typeOrId}`);
    const input = document.getElementById(`edit-${typeOrId}-logo`) || document.querySelector(`input[onchange*="${typeOrId}"]`);

    if (container) container.classList.add('hidden');
    if (input) input.value = '';

    if (clearStore && store.allianceLogos) {
        delete store.allianceLogos[typeOrId];
    }
}

// Agregar input dinámico de alianza
export function addAllianceInput(type, value = '', logoPath = '') {
    const list = document.getElementById(`${type}s-list`);
    const id = `${type}-${Date.now()}-${Math.floor(Math.random() * 1000)}`; // ID único robusto

    // Si viene logoPath previo (edicion), guardarlo en store con este ID
    if (logoPath) {
        store.allianceLogos = store.allianceLogos || {};
        store.allianceLogos[id] = logoPath;
    }

    const div = document.createElement('div');
    div.className = "flex gap-2 items-center group/ally animate-fade-in";
    div.innerHTML = `
        <input type="text" value="${value}" placeholder="Nombre de la entidad" data-ally-type="${type}"
            class="flex-1 bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-700 focus:border-blue-300 outline-none transition-colors">
        
        <div class="relative">
            <label class="flex items-center justify-center w-9 h-9 bg-gray-100 hover:bg-gray-200 rounded-lg cursor-pointer transition-colors text-gray-500 hover:text-blue-600" title="Subir Logo">
                <i class="ph ph-image"></i>
                <input type="file" accept="image/*" class="hidden" onchange="handleLogoUpload(this, '${id}')">
            </label>
        </div>

        <div id="preview-container-${id}" class="${logoPath ? '' : 'hidden'} w-9 h-9 rounded-lg border border-gray-200 bg-white p-0.5 relative flex-shrink-0">
            <img id="preview-${id}-logo" class="w-full h-full object-contain" src="${logoPath ? (logoPath.startsWith('/api/') ? logoPath : '/api/minio_agent/' + logoPath) : ''}">
             <button onclick="clearLogo('${id}')" class="absolute -top-1 -right-1 w-3 h-3 bg-red-500 text-white rounded-full flex items-center justify-center hover:scale-110 transition-transform">
                <i class="ph-bold ph-x text-[8px]"></i>
            </button>
        </div>

        <button onclick="this.parentElement.remove(); clearLogo('${id}')" class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-all">
            <i class="ph ph-trash"></i>
        </button>
    `;
    list.appendChild(div);
}

// Attach to window for HTML onclick compatibility
window.addObjectiveInput = addObjectiveInput;
window.removeObjectiveInput = removeObjectiveInput;
window.handleLogoUpload = handleLogoUpload;
window.clearLogo = clearLogo;
window.addAllianceInput = addAllianceInput;

