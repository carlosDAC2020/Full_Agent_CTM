/**
 * chat_logic.js
 * Utilidades de interfaz: navegación de paneles, timeline y terminal de logs.
 * NO contiene lógica de negocio - solo funciones de UI.
 */

// ==========================================
// NAVEGACIÓN DE PANELES
// ==========================================

/**
 * Cambia el panel visible en el área central
 * @param {string} panelId - ID del panel: 'ingest', 'ideas', 'schema', 'final'
 */
function switchPanel(panelId) {
    // 1. Ocultar todos los paneles
    document.querySelectorAll('.panel-view').forEach(el => el.classList.add('d-none'));

    // 2. Mostrar el panel objetivo
    const target = document.getElementById(`panel-${panelId}`);
    if (target) {
        target.classList.remove('d-none');
    }

    // 3. Actualizar indicadores del Timeline
    updateTimeline(panelId);

    // 4. Manejo de visibilidad del Input Area
    const inputArea = document.querySelector('.input-area-wrapper');
    if (inputArea) {
        if (panelId === 'ingest') {
            inputArea.classList.remove('d-none');
        } else {
            inputArea.classList.add('d-none');
        }
    }

    // 5. Actualizar título del header
    const titles = {
        'ingest': 'Nueva Evaluación',
        'ideas': 'Selección de Propuesta',
        'schema': 'Esquema Preliminar',
        'final': 'Documentos Finales'
    };
    const headerTitle = document.getElementById('current-view-title');
    if (headerTitle && titles[panelId]) {
        headerTitle.innerText = titles[panelId];
    }
}

// ==========================================
// TIMELINE (INDICADORES DE PASO)
// ==========================================

/**
 * Actualiza los indicadores visuales del timeline
 * @param {string} activeStep - Paso activo actual
 */
function updateTimeline(activeStep) {
    const steps = ['ingest', 'ideas', 'schema', 'final'];
    const activeIndex = steps.indexOf(activeStep);

    steps.forEach((step, index) => {
        const el = document.getElementById(`step-indicator-${index + 1}`);
        if (el) {
            el.classList.remove('active', 'completed');

            // Pasos anteriores: completados (verde)
            if (index < activeIndex) {
                el.classList.add('completed');
            }
            // Paso actual: activo (azul)
            if (index === activeIndex) {
                el.classList.add('active');
            }
        }
    });
}

// ==========================================
// TERMINAL DE LOGS
// ==========================================

/**
 * Agrega un mensaje al terminal de logs (estilo consola)
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - Tipo: 'info', 'success', 'error', 'progress'
 */
function logToTerminal(message, type = 'info') {
    const terminal = document.getElementById('loading-text');
    if (!terminal) return;

    // Limpiar mensaje de "esperando" inicial
    if (terminal.innerHTML.includes('Esperando entrada')) {
        terminal.innerHTML = '';
    }

    // Crear línea con formato
    const line = document.createElement('div');
    const timestamp = new Date().toLocaleTimeString('es-CO', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });

    // Colores según tipo
    const colors = {
        'info': '#00ff00',
        'success': '#00ffff',
        'error': '#ff6b6b',
        'progress': '#ffd93d'
    };

    const prefix = type === 'progress' ? '⟳' : '>';
    line.innerHTML = `<span style="color: #888;">[${timestamp}]</span> <span style="color: ${colors[type] || colors.info};">${prefix}</span> ${message}`;

    terminal.appendChild(line);
    terminal.scrollTop = terminal.scrollHeight; // Auto-scroll al final
}

/**
 * Limpia el terminal de logs
 */
function clearTerminal() {
    const terminal = document.getElementById('loading-text');
    if (terminal) {
        terminal.innerHTML = '> Sistema listo.<br>> Esperando entrada del usuario...<span class="blink">_</span>';
    }
}

// ==========================================
// UTILIDADES DE LOADING
// ==========================================

/**
 * Actualiza el estado visual del botón de envío
 * @param {boolean} loading - Si está en estado de carga
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
 * @param {string} status - 'online', 'processing', 'error'
 */
function setStatusBadge(status) {
    const badge = document.querySelector('.sidebar-right .badge');
    if (!badge) return;

    const configs = {
        'online': { text: 'ONLINE', classes: 'bg-success bg-opacity-10 text-success border-success' },
        'processing': { text: 'PROCESSING', classes: 'bg-warning bg-opacity-10 text-warning border-warning' },
        'error': { text: 'ERROR', classes: 'bg-danger bg-opacity-10 text-danger border-danger' }
    };

    const config = configs[status] || configs.online;
    badge.textContent = config.text;
    badge.className = `badge ${config.classes} border border-opacity-25`;
    badge.style.fontSize = '0.6em';
}

// ==========================================
// INICIALIZACIÓN
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    // Auto-resize del textarea
    const textarea = document.getElementById('mainInput');
    if (textarea) {
        textarea.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 200) + 'px';
        });

        // Enviar con Enter (Shift+Enter para nueva línea)
        textarea.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (typeof runIngest === 'function') {
                    runIngest();
                }
            }
        });
    }
});

/**
 * Rellena el input con texto sugerido
 * @param {string} text - Texto a insertar
 */
function fillInput(text) {
    const input = document.getElementById('mainInput');
    if (input) {
        input.value = text + " ";
        input.focus();
        // Trigger resize
        input.dispatchEvent(new Event('input'));
    }
}