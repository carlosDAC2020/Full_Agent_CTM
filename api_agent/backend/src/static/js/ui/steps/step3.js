import { store } from '../../data/store.js';
import { selectIdea } from '../../api/agent.js'; // Note: check if selectIdea is exported in api/agent.js
import { pollTask } from '../../api/tasks.js';
import { getElements, updateStepper } from '../common.js';
import { loadHistory } from '../sidebar.js';

// Paso 3: Confirmar Idea y Generar Esquema
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
        const { task_id } = await selectIdea(store.sessionId, selectedIdea);

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
                loadHistory(store.sessionId);
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

export function renderSchema(data) {
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
            // Estilo coincidente con Step 4 (más sutil)
            badge.className = "bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs border border-gray-200 font-medium";
            badge.textContent = keyword;
            keywordsContainer.appendChild(badge);
        });
    } else {
        keywordsContainer.innerHTML = '<span class="text-xs text-gray-400 italic">No especificadas</span>';
    }
}

// Función auxiliar: Renderizar contenido del esquema
function renderSchemaContent(markdown) {
    const container = document.getElementById('schema-content');
    const rawContainerText = document.getElementById('schema-raw-text');

    container.innerHTML = '';
    // Populate RAW view as well
    if (rawContainerText) {
        rawContainerText.textContent = markdown || "No content.";
    }

    if (!markdown || markdown.trim() === '') {
        container.innerHTML = '<p class="text-sm text-gray-400 italic">No hay contenido disponible</p>';
        return;
    }

    // Usar marked.js para renderizar el Markdown a HTML
    // Configuramos marked para que se vea bien con Tailwind Typography (o estilos básicos)
    try {
        const htmlContent = marked.parse(markdown);

        // Creamos un contenedor con estilos para el contenido renderizado
        const proseWrapper = document.createElement('div');
        proseWrapper.className = 'prose prose-sm prose-blue max-w-none text-gray-700 space-y-2';
        // Estilos específicos para que se vea profesional
        proseWrapper.innerHTML = htmlContent;

        container.appendChild(proseWrapper);
    } catch (e) {
        console.error("Error rendering markdown:", e);
        container.innerHTML = `<div class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">${markdown}</div>`;
    }
}

// Nueva función de Toggle (Exportada a window para click handlers)
export function toggleSchemaView(mode) {
    const renderContent = document.getElementById('schema-content');
    const rawContent = document.getElementById('schema-raw');
    const btnRender = document.getElementById('btn-view-render');
    const btnRaw = document.getElementById('btn-view-raw');

    if (mode === 'raw') {
        // Show Raw
        renderContent.classList.add('hidden');
        rawContent.classList.remove('hidden');

        // Buttons Update
        btnRender.className = "px-3 py-1 rounded-md text-xs font-bold transition-all text-gray-500 hover:text-gray-700";
        btnRaw.className = "px-3 py-1 rounded-md text-xs font-bold transition-all bg-gray-800 text-green-400 shadow-sm";
    } else {
        // Show Rendered
        rawContent.classList.add('hidden');
        renderContent.classList.remove('hidden');

        // Buttons Update
        btnRaw.className = "px-3 py-1 rounded-md text-xs font-bold transition-all text-gray-500 hover:text-gray-700";
        btnRender.className = "px-3 py-1 rounded-md text-xs font-bold transition-all bg-white text-gray-800 shadow-sm";
    }
}
window.toggleSchemaView = toggleSchemaView;
// parseMarkdownSections function removed as it is no longer needed

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
