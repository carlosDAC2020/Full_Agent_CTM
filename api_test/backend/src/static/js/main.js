/**
 * main.js
 * Orquestador principal de la lógica del Frontend.
 * Maneja el estado global, la navegación del Wizard y la restauración de sesiones.
 */

// ==========================================
// 1. ESTADO GLOBAL
// ==========================================
const appState = {
    sessionId: null,
    currentStep: 1,
    ideas: []
};

// ==========================================
// 2. INICIALIZACIÓN
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    // Verificar si hay un ID de sesión en la URL para restaurar el estado
    const params = new URLSearchParams(window.location.search);
    if (params.has('session')) {
        const sessionId = params.get('session');
        loadSession(sessionId);
    }
});

// ==========================================
// 3. UTILIDADES DE INTERFAZ (UI)
// ==========================================

function updateStepperUI(step) {
    // Actualiza los círculos numerados arriba
    for (let i = 1; i <= 4; i++) {
        const el = document.getElementById(`step-indicator-${i}`);
        if (el) {
            el.classList.remove('active', 'completed');
            if (i < step) el.classList.add('completed');
            if (i === step) el.classList.add('active');
        }
    }
}

function switchView(stepNumber) {
    // Ocultar todas las vistas de pasos
    document.querySelectorAll('.step-view').forEach(el => el.classList.add('d-none'));
    
    // Mostrar la vista actual
    const view = document.getElementById(`view-step-${stepNumber}`);
    if (view) view.classList.remove('d-none');
    
    // Actualizar la barra de progreso
    updateStepperUI(stepNumber);
    appState.currentStep = stepNumber;
}

function toggleLoading(show, msg="Procesando...") {
    const overlay = document.getElementById('loading-overlay');
    const label = document.getElementById('loading-text');
    
    if (show) {
        if (label) label.innerText = msg;
        if (overlay) overlay.classList.remove('d-none');
    } else {
        if (overlay) overlay.classList.add('d-none');
    }
}

// ==========================================
// 4. LÓGICA DE RESTAURACIÓN DE SESIÓN
// ==========================================

async function loadSession(sessionId) {
    toggleLoading(true, "Restaurando sesión...");
    
    try {
        const history = await apiGetSessionHistory(sessionId);
        appState.sessionId = sessionId;
        
        const idDisplay = document.getElementById('session-id-display');
        if (idDisplay) idDisplay.innerText = `ID: ${sessionId}`;

        const steps = history.steps_data;

        // CASO 1: FINALIZADO (Paso 4)
        if (steps['generate_project'] || history.status === 'completed') {
            let finalData = steps['generate_project'];
            // A veces steps['generate_project'] es el objeto directo, a veces tiene 'output_data'
            // Depende de tu endpoint history. Asumimos estructura standard.
            
            // Parsear docs
            let docs = finalData.docs_paths;
            // Si docs_paths no está directo, buscar en data
            if (!docs && finalData.data) {
                 let innerData = typeof finalData.data === 'string' ? JSON.parse(finalData.data) : finalData.data;
                 docs = innerData.docs_paths;
            }

            renderFinalDocs(docs); 
            switchView(4);
        }
        // CASO 2: ESQUEMA GENERADO (Paso 3 - Esperando confirmación)
        else if (steps['project_idea']) {
            let schemaData = steps['project_idea'];
            
            // Intentar extraer docs
            let docs = schemaData.docs_paths;
            if (!docs && schemaData.data) {
                 let innerData = typeof schemaData.data === 'string' ? JSON.parse(schemaData.data) : schemaData.data;
                 docs = innerData.docs_paths;
            }

            renderSchemaDocs(docs);
            switchView(3); // Vamos al paso intermedio
        }
        // CASO 3: IDEAS GENERADAS (Paso 2)
        else if (steps['proposal_ideas']) {
            let ideasData = steps['proposal_ideas'];
            // Lógica de restauración de ideas (restoreIdeasView ya la tienes)
            restoreIdeasView(ideasData);
            switchView(2);
        }
        // CASO 4: INGESTA (Paso 1 completado)
        else if (steps['ingest']) {
            switchView(2);
        }
        else {
            switchView(1);
        }

    } catch (e) {
        console.error(e);
        alert("Error al cargar la sesión.");
        switchView(1);
    } finally {
        toggleLoading(false);
    }
}

// Helper para restaurar la vista de ideas desde el historial
function restoreIdeasView(ideasData) {
    let ideasPayload = ideasData;
    if (typeof ideasPayload === 'string') ideasPayload = JSON.parse(ideasPayload);
    
    // Extraer lista de ideas (ajustar según estructura exacta de respuesta)
    // Normalmente es: obj.proposal_ideas.ideas
    const ideasList = (ideasPayload.proposal_ideas && ideasPayload.proposal_ideas.ideas) 
                      ? ideasPayload.proposal_ideas.ideas 
                      : [];
    
    if (ideasList && ideasList.length > 0) {
        appState.ideas = ideasList;
        // renderIdeas viene de ui.js
        if (typeof renderIdeas === 'function') {
            renderIdeas(ideasList);
        }
        
        // Ocultar botón de generar porque ya están generadas
        const btn = document.getElementById('btnGenerateIdeas');
        if(btn) btn.classList.add('d-none');
    }
}

// ==========================================
// 5. LÓGICA DE EJECUCIÓN (PASO A PASO)
// ==========================================

// --- PASO 1: INGESTA ---
async function runIngest() {
    const textInput = document.getElementById('inputIngest');
    const text = textInput ? textInput.value : "";
    
    if (!text.trim()) return alert("Por favor ingresa el texto de la convocatoria.");

    toggleLoading(true, "Analizando convocatoria con IA...");

    try {
        const resp = await apiStartIngest(text);
        appState.sessionId = resp.session_id;
        
        const idDisplay = document.getElementById('session-id-display');
        if (idDisplay) idDisplay.innerText = `ID: ${resp.session_id}`;

        pollTask(resp.task_id, (result) => {
            toggleLoading(false);
            console.log("Ingesta completada:", result);
            switchView(2);
        });
    } catch (e) {
        console.error(e);
        alert("Error al iniciar ingesta");
        toggleLoading(false);
    }
}

// --- PASO 2: GENERAR IDEAS ---
async function generateIdeasAction() {
    if (!appState.sessionId) return alert("No hay sesión activa.");
    
    toggleLoading(true, "Brainstorming de ideas con Gemini...");
    
    try {
        const resp = await apiGenerateIdeas(appState.sessionId);
        
        pollTask(resp.task_id, (result) => {
            toggleLoading(false);
            
            // result.data es el objeto de estado del grafo
            // Accedemos a proposal_ideas -> ideas
            const ideas = result.data.proposal_ideas.ideas;
            appState.ideas = ideas;
            
            // Renderizar (ui.js)
            if (typeof renderIdeas === 'function') {
                renderIdeas(ideas);
            }
            
            // Ocultar botón
            const btn = document.getElementById('btnGenerateIdeas');
            if(btn) btn.classList.add('d-none');
        });
    } catch (e) {
        console.error(e);
        toggleLoading(false);
        alert("Error generando ideas.");
    }
}

// --- PASO 3: SELECCIONAR Y CONFIRMAR ---
// Esta función se llama desde el Modal de Edición en ui.js
async function submitSelectedIdea(ideaData) {
    if (!appState.sessionId) return;

    toggleLoading(true, "Generando esquema inicial y validando viabilidad...");
    
    try {
        const resp = await apiSelectIdea(appState.sessionId, ideaData);
        
        pollTask(resp.task_id, (result) => {
            toggleLoading(false);
            console.log("Esquema generado:", result);
            
            // 1. Obtener los datos del estado
            // Celery devuelve el estado como string en 'data', hay que parsearlo
            let stateData = result.data;
            if (typeof stateData === 'string') {
                stateData = JSON.parse(stateData);
            }

            // 2. Renderizar los documentos del esquema (PDF/MD)
            if (stateData.docs_paths) {
                renderSchemaDocs(stateData.docs_paths);
            }

            // 3. CAMBIO CLAVE: Mostrar la vista del Paso 3 y ESPERAR
            // Ya NO llamamos a runFinalization() aquí.
            switchView(3);

        }, (error) => {
            toggleLoading(false);
            console.error(error);
            alert("Error generando el esquema inicial.");
        });
    } catch (e) {
        console.error(e);
        toggleLoading(false);
        alert("Error de comunicación al seleccionar la idea.");
    }
}

// --- PASO 4: FINALIZAR (DOCS) ---
async function runFinalization() {
    // Actualizamos mensaje de carga sin ocultarlo
    const loadingLabel = document.getElementById('loading-text');
    if(loadingLabel) {
        loadingLabel.innerText = "Redactando reporte, investigando y diseñando póster...";
        loadingLabel.classList.add('text-blink');
    }
    
    try {
        const resp = await apiFinalize(appState.sessionId);
        
        pollTask(resp.task_id, (result) => {
            toggleLoading(false);
            if(loadingLabel) loadingLabel.classList.remove('text-blink');
            
            // Obtener rutas de docs
            const docs = result.data.docs_paths;
            
            // Renderizar links
            renderFinalDocs(docs);
            
            // Mostrar vista final
            switchView(4);
            
            // Feedback usuario
            alert("¡Proceso finalizado con éxito!");
        });
    } catch (e) {
        console.error(e);
        toggleLoading(false);
        alert("Error en la generación final de documentos.");
    }
}

// ==========================================
// 6. HELPER DE RENDERIZADO COMÚN
// ==========================================

function renderFinalDocs(docs) {
    const list = document.getElementById('final-docs-list');
    if (!list) return;
    
    list.innerHTML = '';

    if (!docs) {
        list.innerHTML = '<div class="alert alert-warning">No se encontraron documentos.</div>';
        return;
    }

    // Helper interno para crear items de lista
    const addLink = (label, url, icon, color='primary') => {
        if (url) {
            list.innerHTML += `
                <a href="${url}" target="_blank" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center mb-2 border rounded">
                    <div><span class="fs-4 me-2">${icon}</span> <strong>${label}</strong></div>
                    <span class="badge bg-${color} rounded-pill p-2">Descargar <i class="bi bi-download"></i></span>
                </a>`;
        }
    };

    // Renderizar los documentos disponibles
    addLink("Propuesta Técnica (PDF)", docs.proyect_proposal_pdf, "📄", "danger");
    addLink("Presentación Ejecutiva (PDF)", docs.presentation_oath_pdf, "📊", "warning");
    addLink("Póster Promocional", docs.poster_image_path, "🖼️", "info");
    addLink("Borrador Markdown", docs.proyect_proposal_md, "📝", "secondary");
}


// Función para mostrar los documentos del Paso 3 (Esquema Inicial)
function renderSchemaDocs(docs) {
    const list = document.getElementById('schema-docs-list');
    if (!list) return;
    
    list.innerHTML = ''; // Limpiar lista anterior

    if (!docs || (!docs.proyect_proposal_initial_schema_pdf && !docs.proyect_proposal_initial_schema_md)) {
        list.innerHTML = '<div class="alert alert-warning">No se encontraron documentos de esquema preliminar.</div>';
        return;
    }

    // Helper para crear el HTML del link
    const createLink = (label, url, icon) => {
        if (url) {
            return `
                <a href="${url}" target="_blank" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                    <div><span class="fs-5 me-2">${icon}</span> ${label}</div>
                    <span class="badge bg-secondary rounded-pill">Ver Documento</span>
                </a>`;
        }
        return '';
    };

    let html = '';
    html += createLink("Esquema Preliminar (PDF)", docs.proyect_proposal_initial_schema_pdf, "📄");
    html += createLink("Esquema Preliminar (Markdown)", docs.proyect_proposal_initial_schema_md, "📝");
    
    list.innerHTML = html;
}