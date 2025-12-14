import { store } from '../../data/store.js';
import { generateIdeas } from '../../api/agent.js';
import { pollTask } from '../../api/tasks.js';
import { getElements, updateStepper } from '../common.js';
import { loadHistory } from '../sidebar.js';

// Paso 2: Generar Ideas
export async function goToStep2() {
    const { step1, loader, loaderText, step2 } = getElements();

    // UI Transition
    step1.classList.add('hidden');
    loader.classList.remove('hidden');
    loaderText.innerText = "Analizando oportunidades y generando ideas innovadoras...";
    updateStepper(2);

    try {
        // 1. Start Generate Ideas Task
        const { task_id } = await generateIdeas(store.sessionId);

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
        const ideaObj = {
            title: idea.idea_title,
            desc: idea.idea_description,
            objectives: idea.idea_objectives || []
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

function openEditIdea(idea) {
    const { ideasContainer, ideaEditor } = getElements();
    store.currentSelectedIdea = idea;
    ideasContainer.classList.add('hidden');
    ideaEditor.classList.remove('hidden');

    document.getElementById('edit-title').value = idea.title;
    document.getElementById('edit-desc').value = idea.desc;

    // Clear and populate objectives
    document.getElementById('objectives-list').innerHTML = '';
    if (idea.objectives && Array.isArray(idea.objectives)) {
        idea.objectives.forEach(obj => addObjectiveInput(obj));
    } else {
        addObjectiveInput(''); // Start with one empty
    }
}

export function cancelEdit() {
    const { ideasContainer, ideaEditor } = getElements();
    ideaEditor.classList.add('hidden');
    ideasContainer.classList.remove('hidden');
}

// Dynamic Objectives Logic - Exported if needed by HTML onclicks, or attached to window
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
                   hover:border-gray-300 resize-none"
            rows="3"
            placeholder="Ej: Desarrollar un prototipo funcional con precisión del 85% en 12 meses...">${value}</textarea>
        <button 
            onclick="removeObjectiveInput(this)" 
            class="flex-shrink-0 text-gray-400 hover:text-red-500 hover:bg-red-50 p-2 rounded-lg opacity-0 group-hover/item:opacity-100 transition-all mt-1"
            title="Eliminar objetivo">
            <i class="ph-fill ph-trash text-lg"></i>
        </button>
    `;
    list.appendChild(div);

    // Renumerar todos los objetivos
    renumberObjectives();
}

export function removeObjectiveInput(btn) {
    // Si se llama desde HTML inline (onclick="removeObjectiveInput(this)"), 
    // asegurarse de que la función esté disponible globalmente o manejar el evento de otra forma.
    // Como estamos modulando, lo ideal es asignar al window para compatibilidad con el HTML existente.
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

// Attach to window for HTML onclick compatibility
window.addObjectiveInput = addObjectiveInput;
window.removeObjectiveInput = removeObjectiveInput;
