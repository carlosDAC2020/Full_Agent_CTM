import { mockDB, mockIdeas } from '../data/mocks.js';
import { store } from '../data/store.js';
import { ingestCall, getSessionHistory, generateIdeas } from '../api/agent.js';
import { pollTask } from '../api/tasks.js';

// DOM Elements
function getElements() {
    return {
        initialView: document.getElementById('initial-view'),
        resultsView: document.getElementById('results-view'),
        globalStepper: document.getElementById('global-stepper'),
        loader: document.getElementById('generic-loader'),
        loaderText: document.getElementById('loader-text'),
        step1: document.getElementById('step-1-ingest'),
        step2: document.getElementById('step-2-ideas'),
        step3: document.getElementById('step-3-schema'),
        step4: document.getElementById('step-4-final'),
        ideasContainer: document.getElementById('ideas-container'),
        ideaEditor: document.getElementById('idea-editor')
    };
}

export function updateFileStatus() {
    const input = document.getElementById('file-upload');
    const dropZone = document.getElementById('drop-zone');
    if (input.files.length > 0) {
        dropZone.classList.add('border-green-400', 'bg-green-50/50');
        document.getElementById('upload-text-main').innerText = input.files.length + " Archivo(s)";
    }
}

function updateStepper(step) {
    for (let i = 1; i <= 4; i++) {
        const el = document.getElementById(`step-dot-${i}`);
        if (!el) continue;
        if (i === step) el.className = "text-cotecmar-mid font-bold underline decoration-2 underline-offset-4";
        else if (i < step) el.className = "text-gray-800";
        else el.className = "text-gray-300";
    }
}

// Paso 1
export async function startAnalysis() {
    const { initialView, resultsView, globalStepper, loader, loaderText } = getElements();
    if (!store.selectedValue) return;

    // UI Transitions
    initialView.classList.add('animate-fade-out');
    setTimeout(() => {
        initialView.classList.add('hidden');
        resultsView.classList.remove('hidden');
        resultsView.classList.add('flex');
        globalStepper.classList.remove('hidden');
        document.getElementById('selected-label').innerText = mockDB[store.selectedValue].title;
    }, 500);

    // Call API
    loader.classList.remove('hidden');
    loaderText.innerText = "Iniciando ingesta de convocatoria...";
    updateStepper(1);

    try {
        // 1. Start Ingestion Task
        const { task_id, session_id } = await ingestCall(store.selectedCallText);
        store.sessionId = session_id;

        // 2. Poll Task Progress
        pollTask(
            task_id,
            (message) => {
                // Update loader text with progress message from backend
                loaderText.innerText = message || "Procesando...";
            },
            (result) => {
                // On Complete
                renderStep1Result(result.data);
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

function renderStep1Result(dataJson) {
    const { loader, step1 } = getElements();

    // Parse backend data (which is a JSON string inside the result wrapper)
    let data;
    try {
        data = typeof dataJson === 'string' ? JSON.parse(dataJson) : dataJson;
    } catch (e) { console.error("Error parsing JSON", e); return; }

    const callInfo = data.call_info || {};
    const docs = data.docs_paths || {}; // URLs of generated docs

    // Hide Loader
    loader.classList.add('hidden');

    // Populate UI
    document.getElementById('res-title').innerText = callInfo.title || "Sin Título";
    document.getElementById('res-objective').innerText = callInfo.objective || "Sin objetivos detectados";
    document.getElementById('res-funding').innerText = callInfo.funding || "No especificado";

    // Keywords
    const tagsDiv = document.getElementById('res-keywords');
    tagsDiv.className = "flex flex-wrap gap-2 mt-2"; // Better container styling
    tagsDiv.innerHTML = '';
    if (callInfo.keywords && Array.isArray(callInfo.keywords)) {
        callInfo.keywords.forEach(t => tagsDiv.innerHTML += `
            <span class="bg-blue-50 text-blue-700 border border-blue-100 px-2 py-1 rounded-md shadow-sm text-xs font-medium whitespace-nowrap">#${t}</span>
        `);
    }

    // Dates 
    document.getElementById('res-dates').innerText = callInfo.dates || "Fechas no detectadas";

    // Update Presentation Link: Use correct key 'presentation_oath_pdf' from state.py
    const presBtn = document.getElementById('btn-presentation-link');
    if (presBtn && docs.presentation_oath_pdf) {
        presBtn.href = docs.presentation_oath_pdf;
        presBtn.target = "_blank";
        presBtn.classList.remove('opacity-50', 'pointer-events-none');

        // Visual indicator that it is ready
        presBtn.classList.add('animate-pulse-slow');
        setTimeout(() => presBtn.classList.remove('animate-pulse-slow'), 3000);
    } else if (presBtn) {
        presBtn.classList.add('opacity-50', 'pointer-events-none');
    }

    step1.classList.remove('hidden');

}

// RESTORE SESSION LOGIC
export async function restoreSession(sessionId) {
    const { initialView, resultsView, globalStepper, loader, loaderText, step1, step2, step3, step4 } = getElements();
    store.sessionId = sessionId;

    // Switch Views
    initialView.classList.add('hidden');
    resultsView.classList.remove('hidden');
    resultsView.classList.add('flex');
    globalStepper.classList.remove('hidden');

    loader.classList.remove('hidden');
    loaderText.innerText = "Restaurando sesión...";

    // Reset Steps
    step1.classList.add('hidden');
    step2.classList.add('hidden');
    step3.classList.add('hidden');
    step4.classList.add('hidden');

    try {
        const historyData = await getSessionHistory(sessionId); // returns { steps_data: {...}, status, last_step }
        const stepsMap = historyData.steps_data || {};
        const lastStep = historyData.last_step;

        loader.classList.add('hidden');

        // 1. Restore Ingest Data (Always expected if session exists)
        if (stepsMap['ingest']) {
            renderStep1Result(stepsMap['ingest']);
            updateStepper(1);

            // Extract title for the header label
            let ingestData = typeof stepsMap['ingest'] === 'string' ? JSON.parse(stepsMap['ingest']) : stepsMap['ingest'];
            if (ingestData.call_info && ingestData.call_info.title) {
                document.getElementById('selected-label').innerText = ingestData.call_info.title;
            }
        }

        // 2. Logic based on last executed step
        if (!lastStep || lastStep === 'ingest') {
            // Stay on Step 1
            step1.classList.remove('hidden');
        }
        else if (lastStep === 'proposal_ideas') {
            // Step 1 done, move to Step 2
            step1.classList.add('hidden');
            step2.classList.remove('hidden');
            updateStepper(2);
            // Verify if we have ideas data to render
            if (stepsMap['proposal_ideas']) {
                // TODO: Render real ideas from 'proposal_ideas' output. 
                // For now, using mocks or check if data matches structure.
                renderIdeas(stepsMap['proposal_ideas']); // Pass the data to renderIdeas
            }
        }
        else if (lastStep === 'project_idea') {
            // Step 2 done, move to Step 3 (Schema)
            step1.classList.add('hidden');
            step2.classList.add('hidden');
            step3.classList.remove('hidden');
            updateStepper(3);

            // Restore selected idea to store (needed for renderSchema)
            if (stepsMap['project_idea'] && stepsMap['project_idea'].selected_idea) {
                const ideaData = stepsMap['project_idea'].selected_idea;
                store.currentSelectedIdea = {
                    title: ideaData.idea_title,
                    desc: ideaData.idea_description,
                    objectives: ideaData.idea_objectives || []
                };
            }

            // Render the schema with the saved data
            if (stepsMap['project_idea']) {
                renderSchema(stepsMap['project_idea']);
            }
        }
        // Add more steps logic as we implement them...

    } catch (err) {
        loader.classList.add('hidden');
        alert("Error restaurando sesión: " + err.message);
        location.reload();
    }
}


// Paso 2
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

function renderIdeas(data) {
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

// --- Dynamic Objectives Logic ---
// --- Dynamic Objectives Logic ---
window.addObjectiveInput = function (value = '') {
    const list = document.getElementById('objectives-list');
    const div = document.createElement('div');
    div.className = "flex gap-2 items-start group/item";
    div.innerHTML = `
        <textarea 
            class="flex-1 bg-gray-50 border border-gray-200 rounded-lg p-3 text-sm text-gray-600 focus:ring-2 focus:ring-cotecmar-light outline-none resize-y"
            rows="2"
            placeholder="Redactar objetivo...">${value}</textarea>
        <button onclick="removeObjectiveInput(this)" class="text-gray-400 hover:text-red-500 p-2 opacity-0 group-hover/item:opacity-100 transition-opacity mt-2">
            <i class="ph ph-trash"></i>
        </button>
    `;
    list.appendChild(div);
}

window.removeObjectiveInput = function (btn) {
    btn.parentElement.remove();
}

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
        idea.objectives.forEach(obj => window.addObjectiveInput(obj));
    } else {
        window.addObjectiveInput(''); // Start with one empty
    }
}

export function cancelEdit() {
    const { ideasContainer, ideaEditor } = getElements();
    ideaEditor.classList.add('hidden');
    ideasContainer.classList.remove('hidden');
}

// Paso 3
export async function confirmIdea() {
    const { step2, loader, loaderText, step3 } = getElements();

    // 1. Gather Data from Editor
    const editedTitle = document.getElementById('edit-title').value;
    const editedDesc = document.getElementById('edit-desc').value;

    // Gather objectives from dynamic inputs
    const objInputs = document.querySelectorAll('#objectives-list textarea');
    const editedObjs = Array.from(objInputs).map(input => input.value.trim()).filter(v => v !== '');

    if (!editedTitle || !editedDesc || editedObjs.length === 0) {
        alert("Por favor completa el título, descripción y al menos un objetivo.");
        return;
    }

    const selectedIdea = {
        title: editedTitle,
        desc: editedDesc,
        objectives: editedObjs
    };

    // Update store (optional/fallback)
    store.currentSelectedIdea = selectedIdea;

    // UI Transition
    step2.classList.add('hidden');
    loader.classList.remove('hidden');
    loaderText.innerText = "Estructurando esquema inicial del proyecto...";
    updateStepper(3);

    try {
        // 2. Call API
        // Note: selectIdea needs to be imported! 
        const { task_id } = await import('../api/agent.js').then(m => m.selectIdea(store.sessionId, selectedIdea));

        // 3. Poll Task
        pollTask(
            task_id,
            (message) => {
                loaderText.innerText = message || "Generando esquema...";
            },
            (result) => {
                // On Complete
                let data;
                try { data = typeof result.data === 'string' ? JSON.parse(result.data) : result.data; }
                catch (e) { console.error("Error parsing JSON", e); return; }

                renderSchema(data);
                loader.classList.add('hidden');
                step3.classList.remove('hidden');
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

function renderSchema(data) {
    // Data structure: data.initial_schema (Markdown string)
    // data.docs_paths.proyect_proposal_initial_schema_pdf (Link)

    const schemaTitle = document.getElementById('schema-title');
    const schemaDesc = document.getElementById('schema-desc'); // Mapping to Executive Summary for now
    const schemaObjs = document.getElementById('schema-objs');

    // Attempt to parse simple markdown to fill specific UI slots, or just dump it?
    // User requested: "podria toamr el q viene del .md q es tetxo"

    const mdContent = data.initial_schema || "";
    const pdfLink = data.docs_paths?.proyect_proposal_initial_schema_pdf;

    // Basic extraction (regex or split) to fill the structured view in step-3-schema
    // Since parsing MD is complex without library, we will put the raw or slightly formatted text.
    // Ideally we would use a markdown renderer. For now, populating known fields if available in `report_components` 
    // BUT `initial_schema` node might output text blocks.
    // Let's check `state.py`: initial_schema is Optional[str].
    // `report_components` might optionally be populated.

    // Fallback: Use the data we sent if schema is just raw text
    // Try multiple sources for the title
    let projectTitle = "Proyecto";
    if (store.currentSelectedIdea && store.currentSelectedIdea.title) {
        projectTitle = store.currentSelectedIdea.title;
    } else if (data.selected_idea && data.selected_idea.idea_title) {
        projectTitle = data.selected_idea.idea_title;
    }
    schemaTitle.innerText = projectTitle;

    // If output is just a big string, maybe put it in a container?
    // The current UI expects: Resumen Ejecutivo, Objetivos, Metodología.

    // Let's try to find sections in MD
    const getSection = (name) => {
        const regex = new RegExp(`#+\\s*${name}[\\s\\S]*?(?=#+|$)`, 'i');
        const match = mdContent.match(regex);
        return match ? match[0].replace(/#+.*/, '').trim() : "Contenido no generado.";
    };

    // Populate UI
    schemaDesc.innerText = getSection("Resumen Ejecutivo") || mdContent.slice(0, 500) + "..."; // Fallback

    schemaObjs.innerHTML = '';
    const objsSection = getSection("Objetivos");
    const objsLines = objsSection.split('\n').filter(l => l.trim().startsWith('-'));
    objsLines.forEach(l => schemaObjs.innerHTML += `<li>${l.replace('-', '').trim()}</li>`);

    // Document Links Container (Dynamic creation if not exists)
    let linksContainer = document.getElementById('schema-links');
    if (!linksContainer) {
        linksContainer = document.createElement('div');
        linksContainer.id = 'schema-links';
        linksContainer.className = "mt-6 flex justify-center gap-4";
        document.querySelector('#step-3-schema .doc-page').appendChild(linksContainer);
    }
    linksContainer.innerHTML = '';

    if (pdfLink) {
        linksContainer.innerHTML += `
            <a href="${pdfLink}" target="_blank" class="flex items-center gap-2 text-red-600 font-bold border border-red-200 bg-red-50 px-4 py-2 rounded-lg hover:bg-red-100 transition">
                <i class="ph ph-file-pdf"></i> Ver PDF Generado
            </a>
        `;
    }
    // Optional: TXT/MD download could be added here
}

// Paso 4
export function generateFinal() {
    const { step3, loader, loaderText, step4 } = getElements();
    step3.classList.add('hidden');
    loader.classList.remove('hidden');
    loaderText.innerText = "Realizando investigación profunda y redactando documentos finales...";
    updateStepper(4);

    setTimeout(() => {
        loader.classList.add('hidden');
        step4.classList.remove('hidden');
    }, 3000);
}
