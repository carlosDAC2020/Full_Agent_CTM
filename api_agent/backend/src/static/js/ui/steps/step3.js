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
