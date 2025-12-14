import { mockDB, mockIdeas } from '../data/mocks.js';
import { store } from '../data/store.js';
import { ingestCall, getSessionHistory, generateIdeas, finalizeProject } from '../api/agent.js';
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
        else if (lastStep === 'generate_project' || lastStep === 'generate_proyect' || lastStep === 'final') {
            // Step 3 done, move to Step 4
            step1.classList.add('hidden');
            step2.classList.add('hidden');
            step3.classList.add('hidden');
            step4.classList.remove('hidden');
            updateStepper(4);

            // Renderizar resultados finales
            // Buscamos en 'generate_project', 'generate_proyect' o 'report'
            const finalData = stepsMap['generate_project'] || stepsMap['generate_proyect'] || stepsMap['report'];

            if (finalData) {
                const data = typeof finalData === 'string' ? JSON.parse(finalData) : finalData;
                renderFinalResult(data);
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
window.addObjectiveInput = function (value = '') {
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

window.removeObjectiveInput = function (btn) {
    btn.parentElement.remove();
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
    console.log("Rendering schema with data:", data);

    // 1. Extraer información general
    const generalInfo = data.report_components?.general_info || {};
    const selectedIdea = data.selected_idea || store.currentSelectedIdea || {};

    // 2. Renderizar información general
    renderGeneralInfo(generalInfo, selectedIdea);

    // 3. Parsear y renderizar contenido del esquema
    const mdContent = data.initial_schema || "";
    renderSchemaContent(mdContent);

    // 4. Renderizar enlaces a documentos
    renderDocumentLinks(data.docs_paths);
}

// Función auxiliar: Renderizar información general
function renderGeneralInfo(generalInfo, selectedIdea) {
    // Título
    const title = generalInfo.project_title || selectedIdea.idea_title || selectedIdea.title || 'Sin título';
    document.getElementById('general-title').textContent = title;

    // Duración
    const duration = generalInfo.duration_months
        ? `${generalInfo.duration_months} meses`
        : 'No especificado';
    document.getElementById('general-duration').textContent = duration;

    // Línea Temática
    const thematic = generalInfo.thematic_line || 'No especificado';
    document.getElementById('general-thematic').textContent = thematic;

    // Palabras Clave
    const keywordsContainer = document.getElementById('general-keywords');
    keywordsContainer.innerHTML = '';

    const keywords = generalInfo.keywords || [];
    if (keywords.length > 0) {
        keywords.forEach(keyword => {
            const badge = document.createElement('span');
            badge.className = 'px-2 py-1 bg-blue-500 text-white rounded-md text-xs font-semibold shadow-sm';
            badge.textContent = keyword;
            keywordsContainer.appendChild(badge);
        });
    } else {
        keywordsContainer.innerHTML = '<span class="text-xs text-gray-400 italic">No especificadas</span>';
    }
}

// Función auxiliar: Parsear Markdown en secciones
function parseMarkdownSections(markdown) {
    const sections = [];
    const lines = markdown.split('\n');
    let currentSection = null;

    lines.forEach(line => {
        // Detectar encabezados (## o ###)
        const headerMatch = line.match(/^(#{1,3})\s+(.+)/);
        if (headerMatch) {
            // Guardar sección anterior si existe
            if (currentSection) {
                sections.push(currentSection);
            }
            // Crear nueva sección
            currentSection = {
                level: headerMatch[1].length,
                title: headerMatch[2].trim(),
                content: []
            };
        } else if (currentSection && line.trim()) {
            // Agregar contenido a la sección actual
            currentSection.content.push(line);
        }
    });

    // Guardar última sección
    if (currentSection) {
        sections.push(currentSection);
    }

    return sections;
}

// Función auxiliar: Renderizar contenido del esquema
function renderSchemaContent(markdown) {
    const container = document.getElementById('schema-content');
    container.innerHTML = '';

    if (!markdown || markdown.trim() === '') {
        container.innerHTML = '<p class="text-sm text-gray-400 italic">No hay contenido disponible</p>';
        return;
    }

    const sections = parseMarkdownSections(markdown);

    if (sections.length === 0) {
        // Si no se detectaron secciones, mostrar el contenido completo
        container.innerHTML = `<div class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">${markdown}</div>`;
        return;
    }

    // Renderizar cada sección
    sections.forEach((section, index) => {
        const sectionDiv = document.createElement('div');
        sectionDiv.className = 'mb-6 pb-6 border-b border-gray-200 last:border-b-0';

        // Título de la sección
        const titleClass = section.level === 1
            ? 'text-lg font-bold text-gray-900'
            : 'text-base font-bold text-gray-800';

        const title = document.createElement('h4');
        title.className = `${titleClass} mb-3 pb-2 border-b-2 border-blue-500 flex items-center gap-2`;
        title.innerHTML = `
            <span class="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">
                ${index + 1}
            </span>
            ${section.title}
        `;
        sectionDiv.appendChild(title);

        // Contenido de la sección
        const contentDiv = document.createElement('div');
        contentDiv.className = 'text-sm text-gray-700 leading-relaxed space-y-2 pl-8';

        // Procesar el contenido
        section.content.forEach(line => {
            const trimmedLine = line.trim();
            if (trimmedLine) {
                // Detectar listas
                if (trimmedLine.startsWith('-') || trimmedLine.startsWith('*')) {
                    const listItem = document.createElement('div');
                    listItem.className = 'flex items-start gap-2';
                    listItem.innerHTML = `
                        <i class="ph-fill ph-check-circle text-green-500 text-sm mt-0.5 flex-shrink-0"></i>
                        <span>${trimmedLine.substring(1).trim()}</span>
                    `;
                    contentDiv.appendChild(listItem);
                } else {
                    // Párrafo normal
                    const p = document.createElement('p');
                    p.textContent = trimmedLine;
                    contentDiv.appendChild(p);
                }
            }
        });

        sectionDiv.appendChild(contentDiv);
        container.appendChild(sectionDiv);
    });
}

// Función auxiliar: Renderizar enlaces a documentos
function renderDocumentLinks(docsPaths) {
    const mdLink = document.getElementById('link-md');
    const pdfLink = document.getElementById('link-pdf');

    if (docsPaths) {
        // Markdown
        if (docsPaths.proyect_proposal_initial_schema_md) {
            mdLink.href = docsPaths.proyect_proposal_initial_schema_md;
            mdLink.classList.remove('opacity-50', 'pointer-events-none');
        } else {
            mdLink.href = '#';
            mdLink.classList.add('opacity-50', 'pointer-events-none');
        }

        // PDF
        if (docsPaths.proyect_proposal_initial_schema_pdf) {
            pdfLink.href = docsPaths.proyect_proposal_initial_schema_pdf;
            pdfLink.classList.remove('opacity-50', 'pointer-events-none');
        } else {
            pdfLink.href = '#';
            pdfLink.classList.add('opacity-50', 'pointer-events-none');
        }
    } else {
        // No hay documentos disponibles
        mdLink.href = '#';
        mdLink.classList.add('opacity-50', 'pointer-events-none');
        pdfLink.href = '#';
        pdfLink.classList.add('opacity-50', 'pointer-events-none');
    }
}

// Paso 4
// Paso 4
export async function generateFinal() {
    const { step3, loader, loaderText, step4 } = getElements();

    // UI Transition
    step3.classList.add('hidden');
    loader.classList.remove('hidden');
    loaderText.innerText = "Realizando investigación profunda, generando imágenes y redactando documentos finales...";
    updateStepper(4);

    try {
        // 1. Iniciar Tarea (API Real)
        const { task_id } = await finalizeProject(store.sessionId);

        // 2. Polling
        pollTask(
            task_id,
            (message) => {
                loaderText.innerText = message || "Procesando...";
            },
            (result) => {
                // Completado
                loader.classList.add('hidden');
                step4.classList.remove('hidden');

                // Renderizar datos reales
                if (result.data) {
                    const data = typeof result.data === 'string' ? JSON.parse(result.data) : result.data;
                    renderFinalResult(data);
                }
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

// Función auxiliar: Renderizar resultados finales
function renderFinalResult(data) {
    console.log("Rendering final result:", data);
    const docs = data.docs_paths || {};
    const generalInfo = data.report_components?.general_info || {};
    const selectedIdea = data.selected_idea || {};
    const callInfo = data.call_info || {};

    // ----------------------------------------------------
    // COLUMNA IZQUIERDA: Poster + Botones
    // ----------------------------------------------------

    // 1. Configurar Poster
    const posterImg = document.getElementById('final-poster-img');
    const posterPlaceholder = document.getElementById('final-poster-placeholder');
    const posterOverlay = document.getElementById('poster-overlay');
    const viewPosterBtn = document.getElementById('btn-view-poster');

    if (docs.poster_image_path) {
        posterImg.src = docs.poster_image_path;
        posterImg.classList.remove('hidden');
        posterPlaceholder.classList.add('hidden');
        posterOverlay.classList.remove('hidden');

        // Botón ver en HD
        viewPosterBtn.onclick = () => window.open(docs.poster_image_path, '_blank');
    } else {
        posterImg.classList.add('hidden');
        posterPlaceholder.classList.remove('hidden');
        posterOverlay.classList.add('hidden');
    }

    // 2. Configurar Botón PDF
    const pdfBtn = document.getElementById('final-btn-pdf');
    if (docs.proyect_proposal_pdf) {
        pdfBtn.href = docs.proyect_proposal_pdf;
        pdfBtn.classList.remove('opacity-50', 'pointer-events-none');
        pdfBtn.classList.add('ring-2', 'ring-red-100', 'bg-red-50');
    } else {
        pdfBtn.classList.add('opacity-50', 'pointer-events-none');
        pdfBtn.href = '#';
    }

    // 3. Configurar Botón Markdown
    const mdBtn = document.getElementById('final-btn-md');
    if (docs.proyect_proposal_md) {
        mdBtn.href = docs.proyect_proposal_md;
        mdBtn.classList.remove('opacity-50', 'pointer-events-none');
        mdBtn.classList.add('ring-2', 'ring-gray-200', 'bg-gray-50');
    } else {
        mdBtn.classList.add('opacity-50', 'pointer-events-none');
        mdBtn.href = '#';
    }

    // ----------------------------------------------------
    // COLUMNA DERECHA: Información General
    // ----------------------------------------------------

    // Título
    const title = generalInfo.project_title || selectedIdea.idea_title || callInfo.title || "Proyecto Generado";
    document.getElementById('final-info-title').innerText = title;

    // Duración
    const duration = generalInfo.duration_months ? `${generalInfo.duration_months} meses` : "No especificada";
    document.getElementById('final-info-duration').innerText = duration;

    // Línea Temática
    const thematic = generalInfo.thematic_line || "General";
    document.getElementById('final-info-thematic').innerText = thematic;

    // Palabras Clave
    const keywordsContainer = document.getElementById('final-info-keywords');
    keywordsContainer.innerHTML = '';

    const keywords = generalInfo.keywords || callInfo.keywords || [];

    if (keywords.length > 0) {
        keywords.forEach(kw => {
            const badge = document.createElement('span');
            badge.className = "bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs border border-gray-200";
            badge.innerText = kw;
            keywordsContainer.appendChild(badge);
        });
    } else {
        keywordsContainer.innerHTML = '<span class="text-gray-400 text-sm italic">Sin palabras clave</span>';
    }
}

