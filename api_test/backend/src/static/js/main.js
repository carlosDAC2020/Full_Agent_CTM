/**
 * main.js
 * Orquestador principal del flujo del agente.
 * Maneja estado global, ejecución de pasos, y restauración de sesiones.
 */

// ==========================================
// 1. ESTADO GLOBAL
// ==========================================
const appState = {
    sessionId: null,
    currentStep: 'ingest',
    ideas: [],
    selectedIdea: null,
    stepsData: {}, // Datos de salida de cada paso
    pollInterval: null // Para poder cancelar polling si es necesario
};

// ==========================================
// 1.1 UTILIDADES UI (Integradas para evitar cache issues)
// ==========================================

// ==========================================
// 1.1 UTILIDADES UI (Integradas para evitar cache issues)
// ==========================================

/**
 * Mostrar notificación flotante central
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('central-toast-container');
    if (!container) return;

    // Colores por tipo
    const colors = {
        'success': 'alert-success border-success text-success',
        'error': 'alert-danger border-danger text-danger',
        'progress': 'alert-info border-info text-primary bg-white shadow-lg',
        'info': 'alert-secondary bg-white text-muted'
    };

    const cssClass = colors[type] || colors['info'];
    const icon = type === 'progress' ? '<span class="spinner-border spinner-border-sm me-2"></span>' :
        (type === 'success' ? '<i class="bi bi-check-circle-fill me-2"></i>' :
            (type === 'error' ? '<i class="bi bi-exclamation-triangle-fill me-2"></i>' : ''));

    const toastId = 'toast-' + Date.now();
    const html = `
        <div id="${toastId}" class="alert ${cssClass} d-flex align-items-center mb-2 fade-in-up" role="alert">
            ${icon}
            <div class="fw-medium">${message}</div>
        </div>
    `;

    // Si es mensaje de progreso, limpiar anteriores de progreso para no acumular
    if (type === 'progress') {
        container.innerHTML = html;
    } else {
        container.insertAdjacentHTML('beforeend', html);
        // Auto-eliminar mensajes de éxito/error tras 4s
        setTimeout(() => {
            const el = document.getElementById(toastId);
            if (el) el.remove();
        }, 4000);
    }
}

/**
 * Cambia el panel visible en el área central
 */
function switchPanel(panelId) {
    // 1. Ocultar todos los paneles
    document.querySelectorAll('.panel-view').forEach(el => el.classList.add('d-none'));

    // 2. Mostrar el seleccionado
    const target = document.getElementById(`panel-${panelId}`);
    if (target) {
        target.classList.remove('d-none');
        target.classList.add('fade-in-up');
    }

    // 3. Manejo del Input Flotante
    const inputWrapper = document.querySelector('.input-area-wrapper');
    if (inputWrapper) {
        if (panelId === 'ingest') {
            inputWrapper.style.display = 'flex';
        } else {
            inputWrapper.style.display = 'none';
        }
    }

    // 4. Actualizar Timeline (Sidebar Derecha)
    updateTimeline(panelId);

    // 5. Actualizar Wizard Central
    updateWizardStatus(panelId);

    // 6. Actualizar estado global
    appState.currentStep = panelId;
}

/**
 * Actualiza el encabezado del Wizard Central
 */
function updateWizardStatus(step) {
    const titleEl = document.getElementById('wizard-step-title');
    const descEl = document.getElementById('wizard-step-desc');
    const iconEl = document.getElementById('wizard-step-icon');

    if (!titleEl || !descEl || !iconEl) return;

    const config = {
        'ingest': {
            title: 'Ingesta de Información',
            desc: 'Analizando convocatoria y extrayendo datos clave.',
            icon: '<i class="bi bi-robot"></i>',
            bg: 'bg-primary'
        },
        'ideas': {
            title: 'Generación de Ideas',
            desc: 'Propuestas de valor basadas en la convocatoria.',
            icon: '<i class="bi bi-lightbulb"></i>',
            bg: 'bg-warning'
        },
        'schema': {
            title: 'Estructuración del Proyecto',
            desc: 'Definiendo esquema preliminar y validación.',
            icon: '<i class="bi bi-layout-text-window-reverse"></i>',
            bg: 'bg-info'
        },
        'final': {
            title: 'Finalización y Entregables',
            desc: 'Investigación profunda y documentos finales.',
            icon: '<i class="bi bi-check-circle-fill"></i>',
            bg: 'bg-success'
        }
    };

    const current = config[step] || config['ingest'];

    titleEl.textContent = current.title;
    descEl.textContent = current.desc;
    iconEl.innerHTML = current.icon;

    // Reset classes
    iconEl.className = `rounded-circle text-white d-flex align-items-center justify-content-center me-3 shadow-sm ${current.bg}`;
    iconEl.style.width = '48px';
    iconEl.style.height = '48px';
    iconEl.style.fontSize = '1.5rem';
}

/**
 * Escribe mensajes en la terminal de logs Y en toasts
 */
function logToTerminal(message, type = 'info') {
    // 1. Mostrar en Toast Central si es relevante
    if (typeof showToast === 'function') {
        if (['progress', 'success', 'error'].includes(type) || message.length > 20) {
            showToast(message, type);
        }
    }

    const terminal = document.getElementById('wizard-activity-log');
    if (!terminal) return;

    const now = new Date().toLocaleTimeString('es-CO', { hour12: false });
    let colorClass = 'text-dark';
    let icon = '<i class="bi bi-info-circle text-muted"></i>';

    if (type === 'error') { colorClass = 'text-danger'; icon = '<i class="bi bi-exclamation-circle-fill text-danger"></i>'; }
    if (type === 'success') { colorClass = 'text-success'; icon = '<i class="bi bi-check-circle-fill text-success"></i>'; }
    if (type === 'progress') { colorClass = 'text-primary'; icon = '<span class="spinner-border spinner-border-sm text-primary"></span>'; }

    const entryId = 'log-' + Date.now();
    const line = `
        <div id="${entryId}" class="wizard-log-entry d-flex align-items-start mb-2 fade-in-up">
            <div class="me-2 mt-1">${icon}</div>
            <div>
                <span class="text-muted small me-2">[${now}]</span>
                <span class="${colorClass}">${message}</span>
            </div>
        </div>
    `;

    terminal.insertAdjacentHTML('beforeend', line);

    // Auto-scroll
    terminal.scrollTop = terminal.scrollHeight;
}

/**
 * Limpia la terminal
 */
/**
 * Limpia el log del wizard
 */
function clearTerminal() {
    const terminal = document.getElementById('wizard-activity-log');
    if (terminal) {
        terminal.innerHTML = `
            <div class="d-flex align-items-start mb-2 text-muted">
                <i class="bi bi-info-circle me-2 mt-1"></i>
                <div>Esperando instrucciones...</div>
            </div>`;
    }
}

/**
 * Actualiza el estado visual del botón de envío
 */
function setButtonLoading(loading) {
    const btn = document.getElementById('btnSendIngest');
    if (!btn) return;

    if (loading) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
    } else {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-arrow-up"></i>';
    }
}

/**
 * Actualiza indicador de estado (badge ONLINE/PROCESSING)
 */
function setStatusBadge(status) {
    const badge = document.getElementById('wizard-status-badge');
    if (!badge) return;

    const configs = {
        'online': { text: 'En Espera', class: 'bg-soft-secondary text-secondary border-secondary', icon: 'bi-pause-circle' },
        'processing': { text: 'Procesando', class: 'bg-soft-primary text-primary border-primary progress-pulse', icon: 'bi-cpu-fill' },
        'error': { text: 'Error', class: 'bg-soft-danger text-danger border-danger', icon: 'bi-exclamation-octagon' }
    };

    const config = configs[status] || configs['online'];

    // Limpiar clases anteriores (manteniendo base)
    badge.className = `badge px-3 py-2 rounded-pill border border-opacity-25 ${config.class}`;
    badge.innerHTML = `<i class="bi ${config.icon} me-1 small"></i> ${config.text}`;
}

/**
 * Rellena el input con texto sugerido
 */
function fillInput(text) {
    const input = document.getElementById('mainInput');
    if (input) {
        input.value = text + " ";
        input.focus();
        input.dispatchEvent(new Event('input'));
    }
}

// Exportar globalmente por si acaso
window.switchPanel = switchPanel;
window.setButtonLoading = setButtonLoading;
window.setStatusBadge = setStatusBadge;
window.logToTerminal = logToTerminal;


// ==========================================
// 2. INICIALIZACIÓN
// ==========================================
document.addEventListener('DOMContentLoaded', async () => {
    // 1. Cargar historial de sesiones en sidebar
    await loadSessionsList();

    // 2. Verificar si hay sesión en la URL para restaurar
    const params = new URLSearchParams(window.location.search);
    if (params.has('session')) {
        const sessionId = params.get('session');
        await loadSession(sessionId);
    } else {
        // Iniciar en panel de ingesta
        switchPanel('ingest');
    }

    // 3. Configurar botón de nueva evaluación
    const newChatBtn = document.querySelector('.btn-new-chat');
    if (newChatBtn) {
        newChatBtn.addEventListener('click', startNewSession);
    }
});

// ==========================================
// 3. GESTIÓN DE HISTORIAL (SIDEBAR)
// ==========================================

/**
 * Carga la lista de sesiones en el sidebar izquierdo
 */
async function loadSessionsList() {
    const container = document.getElementById('history-list-container');
    if (!container) return;

    try {
        const sessions = await apiListSessions();

        if (sessions.length === 0) {
            container.innerHTML = `
                <div class="text-center py-3 text-white-50 small">
                    <i class="bi bi-inbox"></i><br>
                    Sin historial
                </div>`;
            return;
        }

        container.innerHTML = sessions.map(session => {
            const statusIcon = session.status === 'completed'
                ? '<i class="bi bi-check-circle-fill text-success me-2"></i>'
                : '<i class="bi bi-clock-history text-warning me-2"></i>';

            const isActive = appState.sessionId === session.id;
            const activeClass = isActive ? 'active' : '';

            return `
                <a href="javascript:void(0)" 
                   class="session-item list-group-item list-group-item-action bg-transparent text-white border-0 px-2 rounded mb-1 py-2 d-flex align-items-center ${activeClass}"
                   onclick="loadSession('${session.id}')">
                    ${statusIcon}
                    <span class="text-truncate small">${session.title_preview}</span>
                </a>`;
        }).join('');

    } catch (e) {
        console.error('Error cargando historial:', e);
        container.innerHTML = `
            <div class="text-center py-3 text-danger small">
                Error cargando historial
            </div>`;
    }
}

/**
 * Inicia una nueva sesión limpia
 */
function startNewSession() {
    // Limpiar estado
    appState.sessionId = null;
    appState.currentStep = 'ingest';
    appState.ideas = [];
    appState.selectedIdea = null;
    appState.stepsData = {};

    // Limpiar URL
    window.history.pushState({}, '', '/');

    // Limpiar UI
    document.getElementById('mainInput').value = '';
    clearTerminal();

    // Ir a panel de ingesta
    switchPanel('ingest');

    // Actualizar historial para quitar clase active
    loadSessionsList();
}

// ==========================================
// 4. RESTAURACIÓN DE SESIÓN
// ==========================================

/**
 * Carga y restaura una sesión existente
 */
async function loadSession(sessionId) {
    logToTerminal(`Cargando sesión ${sessionId.substring(0, 8)}...`, 'info');
    setStatusBadge('processing');

    try {
        const history = await apiGetSessionHistory(sessionId);

        appState.sessionId = sessionId;
        appState.stepsData = history.steps_data || {};

        // Actualizar URL sin recargar
        window.history.pushState({}, '', `?session=${sessionId}`);

        // Determinar el paso actual basado en el historial
        const steps = history.steps_data;

        // CASO 1: COMPLETADO
        if (steps['generate_project'] || history.status === 'completed') {
            logToTerminal('Sesión completada. Mostrando documentos finales.', 'success');
            displayFinalResults(steps['generate_project']);
            switchPanel('final');
        }
        // CASO 2: ESQUEMA GENERADO
        else if (steps['project_idea']) {
            logToTerminal('Sesión en paso 3. Mostrando esquema.', 'info');
            displaySchemaResults(steps['project_idea']);
            switchPanel('schema');
        }
        // CASO 3: IDEAS GENERADAS
        else if (steps['proposal_ideas']) {
            logToTerminal('Sesión en paso 2. Mostrando ideas.', 'info');
            displayIdeasResults(steps['proposal_ideas']);
            switchPanel('ideas');
        }
        // CASO 4: INGESTA COMPLETADA
        else if (steps['ingest']) {
            logToTerminal('Ingesta completada. Mostrando información.', 'info');
            displayIngestResults(steps['ingest']);
            // Mostrar botón para generar ideas
            showGenerateIdeasButton();
            switchPanel('ingest');
        }
        // CASO 5: SESIÓN VACÍA
        else {
            switchPanel('ingest');
        }

        // Actualizar historial para marcar sesión activa
        await loadSessionsList();
        setStatusBadge('online');

    } catch (e) {
        console.error('Error cargando sesión:', e);
        logToTerminal('Error al cargar la sesión.', 'error');
        setStatusBadge('error');
        switchPanel('ingest');
    }
}

// ==========================================
// 5. EJECUCIÓN DE PASOS
// ==========================================

/**
 * PASO 1: Ejecutar Ingesta
 */
async function runIngest() {
    const input = document.getElementById('mainInput');
    const text = input ? input.value.trim() : '';

    if (!text) {
        alert('Por favor ingresa el texto de la convocatoria.');
        return;
    }

    setButtonLoading(true);
    setStatusBadge('processing');
    logToTerminal('Iniciando análisis de convocatoria...', 'progress');

    try {
        const resp = await apiStartIngest(text);
        appState.sessionId = resp.session_id;

        // Actualizar URL
        window.history.pushState({}, '', `?session=${resp.session_id}`);

        logToTerminal(`Sesión iniciada: ${resp.session_id.substring(0, 8)}...`, 'info');

        // Iniciar polling con callback de progreso
        pollTask(
            resp.task_id,
            // onSuccess
            (result) => {
                setButtonLoading(false);
                setStatusBadge('online');
                logToTerminal('Ingesta completada exitosamente.', 'success');

                appState.stepsData['ingest'] = result.data;
                displayIngestResults(result.data);
                showGenerateIdeasButton();

                // Actualizar historial
                loadSessionsList();
            },
            // onError
            (error) => {
                setButtonLoading(false);
                setStatusBadge('error');
                logToTerminal('Error en la ingesta: ' + (error.error || 'Desconocido'), 'error');
            },
            // onProgress
            (message) => {
                logToTerminal(message, 'progress');
            }
        );

    } catch (e) {
        console.error('Error en ingesta:', e);
        setButtonLoading(false);
        setStatusBadge('error');
        logToTerminal('Error de comunicación con el servidor.', 'error');
    }
}

/**
 * PASO 2: Generar Ideas
 */
async function generateIdeasAction() {
    if (!appState.sessionId) {
        alert('No hay sesión activa.');
        return;
    }

    setStatusBadge('processing');
    logToTerminal('Generando ideas de proyecto con IA...', 'progress');

    // Ocultar botón de generar
    const btn = document.getElementById('btnGenerateIdeas');
    if (btn) btn.disabled = true;

    try {
        const resp = await apiGenerateIdeas(appState.sessionId);

        pollTask(
            resp.task_id,
            // onSuccess
            (result) => {
                setStatusBadge('online');
                logToTerminal('Ideas generadas exitosamente.', 'success');

                appState.stepsData['proposal_ideas'] = result.data;
                displayIdeasResults(result.data);
                switchPanel('ideas');
            },
            // onError
            (error) => {
                setStatusBadge('error');
                logToTerminal('Error generando ideas: ' + (error.error || 'Desconocido'), 'error');
                if (btn) btn.disabled = false;
            },
            // onProgress
            (message) => {
                logToTerminal(message, 'progress');
            }
        );

    } catch (e) {
        console.error('Error generando ideas:', e);
        setStatusBadge('error');
        logToTerminal('Error de comunicación.', 'error');
        if (btn) btn.disabled = false;
    }
}

/**
 * PASO 3: Seleccionar Idea y Generar Esquema
 */
async function submitSelectedIdea(ideaData) {
    if (!appState.sessionId) return;

    setStatusBadge('processing');
    logToTerminal('Generando esquema inicial del proyecto...', 'progress');

    try {
        const resp = await apiSelectIdea(appState.sessionId, ideaData);

        pollTask(
            resp.task_id,
            // onSuccess
            (result) => {
                setStatusBadge('online');
                logToTerminal('Esquema generado exitosamente.', 'success');

                appState.stepsData['project_idea'] = result.data;
                appState.selectedIdea = ideaData;

                displaySchemaResults(result.data);
                switchPanel('schema');
            },
            // onError
            (error) => {
                setStatusBadge('error');
                logToTerminal('Error generando esquema: ' + (error.error || 'Desconocido'), 'error');
            },
            // onProgress
            (message) => {
                logToTerminal(message, 'progress');
            }
        );

    } catch (e) {
        console.error('Error seleccionando idea:', e);
        setStatusBadge('error');
        logToTerminal('Error de comunicación.', 'error');
    }
}

/**
 * PASO 4: Finalizar - Investigación y Documentos
 */
async function runFinalization() {
    if (!appState.sessionId) return;

    setStatusBadge('processing');
    logToTerminal('Iniciando investigación académica y generación de documentos...', 'progress');

    // Deshabilitar botón
    const btn = document.querySelector('#panel-schema button.btn-cotecmar');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Procesando...';
    }

    try {
        const resp = await apiFinalize(appState.sessionId);

        pollTask(
            resp.task_id,
            // onSuccess
            (result) => {
                setStatusBadge('online');
                logToTerminal('¡Proceso completado exitosamente!', 'success');

                appState.stepsData['generate_project'] = result.data;
                displayFinalResults(result.data);
                switchPanel('final');

                // Actualizar historial
                loadSessionsList();
            },
            // onError
            (error) => {
                setStatusBadge('error');
                logToTerminal('Error en finalización: ' + (error.error || 'Desconocido'), 'error');
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = '<i class="bi bi-check-circle me-2"></i>Aprobar y Generar Final';
                }
            },
            // onProgress
            (message) => {
                logToTerminal(message, 'progress');
            }
        );

    } catch (e) {
        console.error('Error en finalización:', e);
        setStatusBadge('error');
        logToTerminal('Error de comunicación.', 'error');
    }
}

// ==========================================
// 6. FUNCIONES DE DISPLAY
// ==========================================

/**
 * Muestra los resultados de la ingesta
 */
function displayIngestResults(data) {
    const container = document.getElementById('ingest-result');
    if (!container) return;

    // Extraer call_info
    let callInfo = data?.call_info || data;
    if (typeof callInfo === 'string') {
        try { callInfo = JSON.parse(callInfo); } catch (e) { }
    }

    // Actualizar contenido
    const titleEl = document.getElementById('call-title');
    const entityEl = document.getElementById('call-entity');
    const reqsEl = document.getElementById('call-requirements');

    if (titleEl && callInfo.title) {
        titleEl.textContent = callInfo.title;
    }

    if (entityEl && callInfo.entity) {
        entityEl.innerHTML = `<strong>Entidad:</strong> ${callInfo.entity}`;
    }

    if (reqsEl && callInfo.requirements && Array.isArray(callInfo.requirements)) {
        reqsEl.innerHTML = `
            <strong>Requisitos principales:</strong>
            <ul class="mb-0 mt-2">
                ${callInfo.requirements.slice(0, 5).map(r => `<li class="small">${r}</li>`).join('')}
            </ul>`;
    }

    container.classList.remove('d-none');
}

/**
 * Muestra el botón para generar ideas
 */
function showGenerateIdeasButton() {
    let btn = document.getElementById('btnGenerateIdeas');

    if (!btn) {
        // Crear el botón si no existe
        const container = document.getElementById('ingest-result');
        if (container) {
            const btnDiv = document.createElement('div');
            btnDiv.className = 'text-center mt-4';
            btnDiv.innerHTML = `
                <button class="btn btn-cotecmar btn-lg px-5 shadow" id="btnGenerateIdeas" onclick="generateIdeasAction()">
                    <i class="bi bi-lightbulb me-2"></i>Generar Ideas de Proyecto
                </button>`;
            container.appendChild(btnDiv);
        }
    } else {
        btn.classList.remove('d-none');
        btn.disabled = false;
    }
}

/**
 * Muestra las ideas generadas
 */
function displayIdeasResults(data) {
    // Extraer lista de ideas
    let ideas = [];
    if (data?.proposal_ideas?.ideas) {
        ideas = data.proposal_ideas.ideas;
    } else if (Array.isArray(data)) {
        ideas = data;
    }

    appState.ideas = ideas;

    // Usar la función de ui.js para renderizar
    if (typeof renderIdeas === 'function') {
        renderIdeas(ideas);
    }
}

/**
 * Muestra los documentos del esquema
 */
function displaySchemaResults(data) {
    const list = document.getElementById('schema-docs-list');
    if (!list) return;

    list.innerHTML = '';

    const docs = data?.docs_paths || {};

    if (!docs.proyect_proposal_initial_schema_pdf && !docs.proyect_proposal_initial_schema_md) {
        list.innerHTML = '<div class="alert alert-info">Documentos en preparación...</div>';
        return;
    }

    const createLink = (label, url, icon) => {
        if (!url) return '';
        return `
            <a href="${url}" target="_blank" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                <div><span class="fs-5 me-2">${icon}</span> ${label}</div>
                <span class="badge bg-secondary rounded-pill">Ver</span>
            </a>`;
    };

    list.innerHTML =
        createLink('Esquema Preliminar (PDF)', docs.proyect_proposal_initial_schema_pdf, '📄') +
        createLink('Esquema Preliminar (MD)', docs.proyect_proposal_initial_schema_md, '📝');
}

/**
 * Muestra los documentos finales
 */
function displayFinalResults(data) {
    const list = document.getElementById('final-docs-list');
    if (!list) return;

    list.innerHTML = '';

    const docs = data?.docs_paths || {};

    const addLink = (label, url, icon, color = 'primary') => {
        if (!url) return;
        list.innerHTML += `
            <a href="${url}" target="_blank" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center mb-2 border rounded">
                <div><span class="fs-4 me-2">${icon}</span> <strong>${label}</strong></div>
                <span class="badge bg-${color} rounded-pill p-2">Descargar <i class="bi bi-download"></i></span>
            </a>`;
    };

    addLink('Propuesta Técnica (PDF)', docs.proyect_proposal_pdf, '📄', 'danger');
    addLink('Presentación Ejecutiva (PDF)', docs.presentation_oath_pdf, '📊', 'warning');
    addLink('Póster Promocional', docs.poster_image_path, '🖼️', 'info');
    addLink('Borrador Markdown', docs.proyect_proposal_md, '📝', 'secondary');

    if (list.innerHTML === '') {
        list.innerHTML = '<div class="alert alert-warning">No se encontraron documentos.</div>';
    }
}
