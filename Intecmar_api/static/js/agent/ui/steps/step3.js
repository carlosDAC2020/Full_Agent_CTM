import { store } from '../../data/store.js';
import { selectIdea, getPosterHistory, applyLogos } from '../../api/agent.js';
import { pollTask } from '../../api/tasks.js';
import { getElements, updateStepper, getAssetUrl } from '../common.js';
import { loadHistory } from '../sidebar.js';
import { generateFinal } from './step4.js';

let baseImageMode = 'current'; // 'current' or 'history'
let selectedBaseImagePath = null;

// Listen for updates from Alliance Modal (Synchronization across steps)
window.addEventListener('poster-updated', (e) => {
    console.log("📢 [step3.js] Poster Update Event received", e.detail);
    const generalInfo = e.detail?.report_components?.general_info;
    if (generalInfo) {
        console.log("📊 [step3.js] Updating alliances with:", generalInfo);
        // Sync store.currentSelectedIdea so Step 3 displays latest alliance data
        if (store.currentSelectedIdea) {
            console.log("🔄 [step3.js] Syncing store.currentSelectedIdea");
            store.currentSelectedIdea.executor_entity = generalInfo.executor_entity;
            store.currentSelectedIdea.executor_entity_logo = generalInfo.executor_entity_logo;
            store.currentSelectedIdea.coejecutors_entities = generalInfo.coejecutors_entities || [];
            store.currentSelectedIdea.coejecutors_entities_logos = generalInfo.coejecutors_entities_logos || [];
            store.currentSelectedIdea.collaborators_entities = generalInfo.collaborators_entities || [];
            store.currentSelectedIdea.collaborators_entities_logos = generalInfo.collaborators_entities_logos || [];
        }
        renderAlliances(generalInfo, store.currentSelectedIdea || {});
    } else {
        console.warn("⚠️ [step3.js] Event received but no general_info found in detail");
    }
});

// Paso 3: Confirmar Idea y Generar Esquema
export async function confirmIdea() {
    const { step2, loader, loaderText, step3 } = getElements();

    // 1. Gather Data from Editor
    const editedTitle = document.getElementById('edit-title').value;
    const editedDesc = document.getElementById('edit-desc').value;
    const duration = document.getElementById('edit-duration').value;
    const executor = document.getElementById('edit-executor').value;

    // Gather objectives
    const objInputs = document.querySelectorAll('#objectives-list textarea');
    const editedObjs = Array.from(objInputs).map(input => input.value.trim()).filter(v => v !== '');

    if (!editedTitle || !editedDesc || editedObjs.length === 0) {
        alert("Por favor completa el título, descripción y al menos un objetivo.");
        return;
    }

    // Helper functions for dynamic lists (defined below)
    const coejecutors = getListsData('coejecutor');
    const collaborators = getListsData('collaborator');

    // Get logos from store temporal
    const logos = store.allianceLogos || {};

    const selectedIdea = {
        idea_title: editedTitle,
        idea_description: editedDesc,
        idea_objectives: editedObjs,
        idea_general_objective: document.getElementById('edit-general-objective')?.value || '',
        duration_time: duration, // Backend expects string in ProposalIdea or int? State says str/int adaptable

        executor_entity: executor,
        executor_entity_logo: logos['executor'] || store.currentSelectedIdea?.executor_entity_logo,

        coejecutors_entities: coejecutors.names,
        coejecutors_entities_logos: coejecutors.logos, // Array ordenado

        collaborators_entities: collaborators.names,
        collaborators_entities_logos: collaborators.logos
    };

    // Update store
    store.currentSelectedIdea = selectedIdea;
    console.log("📤 PREPARING TO SEND selectIdea:", selectedIdea);

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

// Regenerate Schema without going back to step 2
export async function regenerateInitialSchema() {
    const { step3, loader, loaderText } = getElements();
    const selectedIdea = store.currentSelectedIdea;

    if (!selectedIdea) {
        console.error("❌ No selected idea found in store for regeneration");
        return;
    }

    console.log("🔄 REGENERATING SCHEMA with:", selectedIdea);

    // UI Transition
    step3.classList.add('hidden');
    loader.classList.remove('hidden');
    loaderText.innerText = "Regenerando esquema inicial del proyecto...";
    loaderText.classList.remove('text-red-500');

    try {
        // reuse selectIdea logic
        const { task_id } = await selectIdea(store.sessionId, selectedIdea);

        pollTask(
            task_id,
            (message) => {
                loaderText.innerText = message || "Regenerando esquema...";
            },
            (result) => {
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
window.regenerateInitialSchema = regenerateInitialSchema;

function getListsData(type) {
    const listContainer = document.getElementById(`${type}s-list`);
    const items = listContainer.querySelectorAll('.group\\/ally'); // Escapar slash para querySelector
    const names = [];
    const logos = [];

    items.forEach((item, index) => {
        const input = item.querySelector(`input[type="text"]`);
        const fileInput = item.querySelector(`input[type="file"]`);

        console.log(`🔍 getListsData (${type}) - Item ${index}:`, {
            inputFound: !!input,
            inputValue: input?.value,
            fileInputFound: !!fileInput
        });

        if (input) {
            names.push(input.value);

            // Extract ID from onchange string: handleLogoUpload(this, 'ID')
            let logoId = null;
            if (fileInput) {
                const onchangeStr = fileInput.getAttribute('onchange');
                const match = onchangeStr ? onchangeStr.match(/'([^']+)'/) : null;
                if (match) {
                    logoId = match[1];
                }
            }

            const logoPath = logoId ? store.allianceLogos?.[logoId] : null;
            logos.push(logoPath || null);

            console.log(`   - Logo ID: ${logoId}, Path found in store: ${logoPath}`);
        }
    });
    return { names, logos };
}

export function renderSchema(data) {
    console.log("🚀 Rendering schema with data:", data);

    // 1. Extraer información general
    const generalInfo = data.report_components?.general_info || {};

    // Si el backend devuelve la idea seleccionada, actualizamos el store para que esté sincronizado
    if (data.selected_idea) {
        console.log("📥 Updating store.currentSelectedIdea with backend data");
        // Mezclamos para no perder campos que el backend quizás no mapeó pero el frontend sí tiene
        store.currentSelectedIdea = { ...store.currentSelectedIdea, ...data.selected_idea };
    }

    const selectedIdea = store.currentSelectedIdea || {};

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
    // State: suggested_duration_months (int) o duration_time (str)
    // GeneralInfo: duration_months (int)
    let durationVal = generalInfo.duration_months || selectedIdea.duration_time || selectedIdea.suggested_duration_months;
    const duration = durationVal ? `${durationVal} meses` : 'No especificado';
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
            badge.className = "bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs border border-gray-200 font-medium";
            badge.textContent = keyword;
            keywordsContainer.appendChild(badge);
        });
    } else {
        keywordsContainer.innerHTML = '<span class="text-xs text-gray-400 italic">No especificadas</span>';
    }

    // Renderizar Alianzas (buscar en generalInfo O selectedIdea)
    renderAlliances(generalInfo, selectedIdea);
}

// Función auxiliar: Renderizar alianzas del proyecto
function renderAlliances(generalInfo, selectedIdea) {
    const executorSection = document.getElementById('executor-section');
    const coejecutorsSection = document.getElementById('coejecutors-section');
    const collaboratorsSection = document.getElementById('collaborators-section');
    const noAlliancesPlaceholder = document.getElementById('no-alliances-placeholder');

    let hasAnyAlliance = false;

    // Reset all sections
    executorSection?.classList.add('hidden');
    coejecutorsSection?.classList.add('hidden');
    collaboratorsSection?.classList.add('hidden');
    noAlliancesPlaceholder?.classList.remove('hidden');

    // Consolidar datos de alianzas (Priorizar generalInfo del backend, luego selectedIdea)
    const executorEntity = generalInfo.executor_entity || selectedIdea.executor_entity;
    const executorLogo = generalInfo.executor_entity_logo || selectedIdea.executor_entity_logo;

    const coejecutorsEntities = (generalInfo.coejecutors_entities && generalInfo.coejecutors_entities.length > 0)
        ? generalInfo.coejecutors_entities
        : (selectedIdea.coejecutors_entities || []);
    const coejecutorsLogos = (generalInfo.coejecutors_entities_logos && generalInfo.coejecutors_entities_logos.length > 0)
        ? generalInfo.coejecutors_entities_logos
        : (selectedIdea.coejecutors_entities_logos || []);

    const collaboratorsEntities = (generalInfo.collaborators_entities && generalInfo.collaborators_entities.length > 0)
        ? generalInfo.collaborators_entities
        : (selectedIdea.collaborators_entities || []);
    const collaboratorsLogos = (generalInfo.collaborators_entities_logos && generalInfo.collaborators_entities_logos.length > 0)
        ? generalInfo.collaborators_entities_logos
        : (selectedIdea.collaborators_entities_logos || []);

    // Ejecutor
    if (executorEntity) {
        hasAnyAlliance = true;
        executorSection?.classList.remove('hidden');

        const executorName = document.getElementById('executor-name');
        const executorLogoContainer = document.getElementById('executor-logo-container');
        const executorLogoImg = document.getElementById('executor-logo-img');

        if (executorName) executorName.textContent = executorEntity;

        if (executorLogo && executorLogoContainer && executorLogoImg) {
            executorLogoContainer.classList.remove('hidden');
            const logoUrl = executorLogo.startsWith('/api/')
                ? executorLogo
                : '/api/minio_agent/' + executorLogo;
            executorLogoImg.src = logoUrl;
        } else if (executorLogoContainer) {
            executorLogoContainer.classList.add('hidden');
        }
    }

    // Coejecutores
    if (coejecutorsEntities.length > 0) {
        hasAnyAlliance = true;
        coejecutorsSection?.classList.remove('hidden');

        const coejecutorsDisplay = document.getElementById('coejecutors-display');
        if (coejecutorsDisplay) {
            coejecutorsDisplay.innerHTML = '';
            coejecutorsEntities.forEach((name, index) => {
                const logo = coejecutorsLogos[index];
                const badge = createAllianceBadge(name, logo, 'blue');
                coejecutorsDisplay.appendChild(badge);
            });
        }
    }

    // Colaboradores
    if (collaboratorsEntities.length > 0) {
        hasAnyAlliance = true;
        collaboratorsSection?.classList.remove('hidden');

        const collaboratorsDisplay = document.getElementById('collaborators-display');
        if (collaboratorsDisplay) {
            collaboratorsDisplay.innerHTML = '';
            collaboratorsEntities.forEach((name, index) => {
                const logo = collaboratorsLogos[index];
                const badge = createAllianceBadge(name, logo, 'purple');
                collaboratorsDisplay.appendChild(badge);
            });
        }
    }

    // Mostrar/ocultar placeholder
    if (hasAnyAlliance) {
        noAlliancesPlaceholder?.classList.add('hidden');
    }
}

// Función auxiliar: Crear badge de alianza con logo opcional
function createAllianceBadge(name, logoPath, color = 'gray') {
    const colorClasses = {
        blue: 'bg-blue-50 border-blue-100 text-blue-800',
        purple: 'bg-purple-50 border-purple-100 text-purple-800',
        gray: 'bg-gray-50 border-gray-200 text-gray-700'
    };

    const badge = document.createElement('div');
    badge.className = `flex items-center gap-1.5 px-2 py-1 rounded-lg border text-xs font-medium ${colorClasses[color] || colorClasses.gray}`;

    if (logoPath) {
        const logoUrl = logoPath.startsWith('/api/') ? logoPath : '/api/minio_agent/' + logoPath;
        badge.innerHTML = `
            <img src="${logoUrl}" class="w-5 h-5 rounded object-contain bg-white border border-gray-100" alt="">
            <span>${name}</span>
        `;
    } else {
        badge.innerHTML = `<span>${name}</span>`;
    }

    return badge;
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
        // Configurar opciones de marked para mejor compatibilidad
        marked.use({
            breaks: true, // Interpretar saltos de línea simples como <br>
            gfm: true     // GitHub Flavored Markdown
        });

        const htmlContent = marked.parse(markdown);

        // Creamos un contenedor con estilos para el contenido renderizado
        const proseWrapper = document.createElement('div');
        // 'prose' activa los estilos tipográficos. 'prose-sm' ajusta el tamaño. 
        // 'prose-blue' da color a enlaces y acentos. 'max-w-none' usa todo el ancho disponible.
        proseWrapper.className = 'prose prose-sm prose-slate max-w-none text-gray-700 space-y-2 prose-headings:font-bold prose-headings:text-gray-800 prose-h1:text-2xl prose-h3:text-lg prose-h3:mt-6 prose-h3:text-blue-700 prose-strong:text-gray-900 prose-ul:list-disc prose-ul:pl-4 prose-blockquote:border-l-4 prose-blockquote:border-blue-500 prose-blockquote:bg-blue-50 prose-blockquote:py-2 prose-blockquote:px-4 prose-blockquote:not-italic prose-blockquote:text-gray-600 prose-blockquote:rounded-r-lg';

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

// Config Modal Functions
export function openConfigModal(isRegen = false) {
    const modal = document.getElementById('config-modal');
    const regenContainer = document.getElementById('regen-options-container');
    const posterContainer = document.getElementById('poster-override-container');
    const actionTxt = document.getElementById('txt-modal-action');

    // Load current config or defaults (Min: 200)
    const currentConfig = store.generationConfig || { charLimit: 2050, refStyle: 'APA' };

    // Set UI
    document.getElementById('char-limit-range').value = currentConfig.charLimit;
    document.getElementById('char-limit-input').value = currentConfig.charLimit;

    // Reset regeneration/poster fields
    if (posterContainer) document.getElementById('poster-prompt-override').value = '';
    const regenChecks = document.getElementsByName('regen-section');
    for (const check of regenChecks) {
        check.checked = false;
        // Hide limits
        const limitDiv = document.getElementById(`limit-${check.value}`);
        if (limitDiv) limitDiv.classList.add('hidden');
    }
    const redoAcademic = document.getElementById('redo-academic');
    if (redoAcademic) redoAcademic.checked = false;

    // Toggle specific containers
    if (isRegen) {
        regenContainer?.classList.remove('hidden');
        posterContainer?.classList.remove('hidden');
        if (actionTxt) actionTxt.innerText = "Regenerar Seleccionados";
    } else {
        regenContainer?.classList.add('hidden');
        posterContainer?.classList.add('hidden');
        if (actionTxt) actionTxt.innerText = "Confirmar e Investigar";
    }

    const radios = document.getElementsByName('ref-style');
    for (const radio of radios) {
        if (radio.value === currentConfig.refStyle) {
            radio.checked = true;
        }
    }

    modal.classList.remove('hidden');

    // Reset History State
    baseImageMode = 'current';
    selectedBaseImagePath = null;
    const currentRadio = document.querySelector('input[name="apply-mode"][value="current"]');
    if (currentRadio) currentRadio.checked = true;
    const historyDiv = document.getElementById('base-history-selector');
    if (historyDiv) historyDiv.classList.add('hidden');
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
window.toggleBaseHistory = toggleBaseHistory;

async function loadBaseImageHistory() {
    const grid = document.getElementById('base-history-grid');
    if (!grid) return;

    grid.innerHTML = '<div class="col-span-2 text-center text-slate-400 py-6"><i class="ph ph-spinner animate-spin text-xl"></i></div>';

    try {
        const history = await getPosterHistory(store.sessionId);

        // De-duplicate by base_image_path to avoid repeating the same background
        const uniqueBases = [];
        const seenPaths = new Set();

        // We iterate in natural order first, or reverse if we want the LATEST metadata for that base
        // Given the original code used .reverse() later, let's de-duplicate first.
        history.forEach(item => {
            if (item.base_image_path && !seenPaths.has(item.base_image_path)) {
                seenPaths.add(item.base_image_path);
                uniqueBases.push(item);
            }
        });

        grid.innerHTML = '';

        if (uniqueBases.length === 0) {
            grid.innerHTML = '<div class="col-span-2 text-center text-xs text-slate-400 py-4 italic">No hay versiones anteriores disponibles.</div>';
            return;
        }

        uniqueBases.reverse().forEach((item, idx) => {
            const div = document.createElement('div');
            const isActive = selectedBaseImagePath === item.base_image_path;
            div.className = `group/base relative aspect-[3/4] rounded-xl overflow-hidden border-2 cursor-pointer transition-all ${isActive ? 'border-blue-500 shadow-lg ring-4 ring-blue-500/10' : 'border-slate-200 hover:border-blue-300'}`;
            div.onclick = () => selectBaseImage(item.base_image_path, div);

            const url = item.base_image_url || getAssetUrl(item.base_image_path);

            div.innerHTML = `
                <img src="${url}" class="w-full h-full object-cover transition-transform group-hover/base:scale-110">
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover/base:opacity-100 transition-opacity"></div>
                <div class="absolute bottom-2 left-2 right-2 text-white text-[9px] font-bold truncate drop-shadow-md">
                    ${new Date(item.timestamp).toLocaleDateString()}
                </div>
                ${isActive ? '<div class="absolute top-2 right-2 bg-blue-500 text-white w-6 h-6 rounded-full flex items-center justify-center shadow-lg border-2 border-white"><i class="ph-bold ph-check text-xs"></i></div>' : ''}
             `;
            grid.appendChild(div);
        });

    } catch (e) {
        console.error(e);
        grid.innerHTML = '<div class="col-span-2 text-center text-red-500 text-xs py-4 font-bold">Error cargando historial</div>';
    }
}

export function selectBaseImage(path, element) {
    selectedBaseImagePath = path;
    const grid = document.getElementById('base-history-grid');
    if (!grid) return;

    Array.from(grid.children).forEach(child => {
        child.classList.remove('border-blue-500', 'shadow-lg', 'ring-4', 'ring-blue-500/10');
        child.classList.add('border-slate-200');
        const check = child.querySelector('.ph-check')?.parentNode;
        if (check) check.remove();
    });

    element.classList.remove('border-slate-200');
    element.classList.add('border-blue-500', 'shadow-lg', 'ring-4', 'ring-blue-500/10');

    const iconDiv = document.createElement('div');
    iconDiv.className = "absolute top-2 right-2 bg-blue-500 text-white w-6 h-6 rounded-full flex items-center justify-center shadow-lg border-2 border-white animate-bounce-in";
    iconDiv.innerHTML = '<i class="ph-bold ph-check text-xs"></i>';
    element.appendChild(iconDiv);
}
window.selectBaseImage = selectBaseImage;

export function closeConfigModal() {
    document.getElementById('config-modal').classList.add('hidden');
}

export function saveConfig() {
    // Get values
    const charLimit = document.getElementById('char-limit-input').value;
    const refStyle = document.querySelector('input[name="ref-style"]:checked').value;

    // Save to store
    store.generationConfig = {
        charLimit: parseInt(charLimit),
        refStyle: refStyle
    };

    console.log("✅ Configuration Saved:", store.generationConfig);

    // Feedback (Visual)
    const saveBtn = document.querySelector('#btn-modal-action');
    const originalContent = saveBtn.innerHTML;
    saveBtn.innerHTML = '<i class="ph-bold ph-check"></i> Guardado!';
    saveBtn.classList.add('bg-green-600');

    setTimeout(() => {
        closeConfigModal();
        // Reset button state after closing
        setTimeout(() => {
            saveBtn.innerHTML = originalContent;
            saveBtn.classList.remove('bg-green-600');
        }, 500);
    }, 800);
}

export function saveConfigAndGenerate() {
    // 1. Get values
    const charLimit = document.getElementById('char-limit-input').value;
    const refStyle = document.querySelector('input[name="ref-style"]:checked').value;

    // Selective Regeneration fields
    const sectionsToRegen = [];
    const sectionLimits = {};
    const regenChecks = document.getElementsByName('regen-section');
    for (const check of regenChecks) {
        if (check.checked) {
            sectionsToRegen.push(check.value);
            const limitInput = document.getElementsByName(`section-limit-${check.value}`)[0];
            if (limitInput) {
                sectionLimits[check.value] = parseInt(limitInput.value);
            }
        }
    }

    const redoTheoretical = document.getElementById('redo-academic')?.checked || false;
    const posterOverride = document.getElementById('poster-prompt-override')?.value || null;

    store.generationConfig = {
        charLimit: parseInt(charLimit),
        refStyle: refStyle,
        sections_to_regenerate: sectionsToRegen,
        redo_theoretical_framework: redoTheoretical,
        section_char_limits: sectionLimits,
        poster_prompt_override: posterOverride,
        base_image_path: baseImageMode === 'history' ? selectedBaseImagePath : null
    };

    console.log("🚀 [UI] Unified Generation Config:", store.generationConfig);

    // Default: Full Generation (Now supports historical image override in backend)
    closeConfigModal();
    generateFinal();
}
