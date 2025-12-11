// Estado simulado
const uiState = {
    currentStep: 'ingest'
};

// --- UTILIDADES VISUALES ---

function switchPanel(panelId) {
    // 1. Ocultar todos
    document.querySelectorAll('.panel-view').forEach(el => el.classList.add('d-none'));
    
    // 2. Mostrar objetivo
    const target = document.getElementById(`panel-${panelId}`);
    if(target) target.classList.remove('d-none');
    
    // 3. Actualizar Timeline
    updateTimeline(panelId);

    // 4. Manejo del Input Flotante
    const inputArea = document.querySelector('.input-area-wrapper');
    if(panelId === 'ingest') {
        inputArea.classList.remove('d-none'); // Mostrar solo en ingesta
    } else {
        inputArea.classList.add('d-none');    // Ocultar en el resto
    }
}

function updateTimeline(activeStep) {
    // Mapeo de pasos a IDs numéricos (ingest->1, ideas->2, etc.)
    const steps = ['ingest', 'ideas', 'schema', 'final'];
    const activeIndex = steps.indexOf(activeStep);

    steps.forEach((step, index) => {
        const el = document.getElementById(`step-indicator-${index + 1}`);
        if(el) {
            el.classList.remove('active', 'completed');
            if(index < activeIndex) el.classList.add('completed'); // Pasos anteriores verdes
            if(index === activeIndex) el.classList.add('active');  // Paso actual azul
        }
    });
}

function logToTerminal(message) {
    const terminal = document.querySelector('.logs-terminal');
    if(!terminal) return;
    
    const line = document.createElement('div');
    line.innerText = `> ${message}`;
    terminal.appendChild(line);
    terminal.scrollTop = terminal.scrollHeight; // Auto-scroll
}

// --- SIMULACIÓN DEL FLUJO (MOCK) ---

// 1. Ejecutar Ingesta (Click en flecha)
async function runIngest() {
    const text = document.getElementById('mainInput').value;
    if(!text) return alert("Escribe algo...");

    // UI Feedback
    logToTerminal("Iniciando análisis de convocatoria...");
    const btn = document.querySelector('.send-btn');
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
    
    // Simular retardo de red (2 seg)
    setTimeout(() => {
        logToTerminal("Datos extraídos correctamente.");
        logToTerminal("Generando propuestas de valor...");
        
        // Simular otro retardo (1 seg)
        setTimeout(() => {
            switchPanel('ideas');
            btn.innerHTML = '<i class="bi bi-arrow-up"></i>'; // Restaurar botón
        }, 1500);
    }, 2000);
}

// 2. Seleccionar Idea (Click en tarjeta)
function selectIdeaMock(id) {
    logToTerminal(`Idea #${id} seleccionada.`);
    logToTerminal("Estructurando esquema preliminar...");
    
    // Simular carga
    document.body.style.cursor = 'wait';
    
    setTimeout(() => {
        document.body.style.cursor = 'default';
        logToTerminal("Esquema generado (PDF/MD).");
        switchPanel('schema');
    }, 1500);
}

// 3. Finalizar (Click en Aprobar)
function runFinalizationMock() {
    logToTerminal("Iniciando investigación profunda...");
    const btn = document.querySelector('#panel-schema button');
    const originalText = btn.innerHTML;
    btn.innerHTML = 'Procesando... <span class="spinner-border spinner-border-sm"></span>';
    
    // Simulación de pasos largos
    setTimeout(() => logToTerminal("Buscando en Semantic Scholar..."), 1000);
    setTimeout(() => logToTerminal("Redactando Justificación..."), 2500);
    setTimeout(() => logToTerminal("Generando Póster con DALL-E 3..."), 4000);
    
    setTimeout(() => {
        switchPanel('final');
        logToTerminal("Proceso finalizado exitosamente.");
    }, 5500);
}

// --- INIT ---
document.addEventListener('DOMContentLoaded', () => {
    // Iniciar en Ingesta
    switchPanel('ingest');
    
    // Auto-resize textarea
    const tx = document.getElementById('mainInput');
    if(tx) {
        tx.addEventListener("input", function() {
            this.style.height = "auto";
            this.style.height = (this.scrollHeight) + "px";
        });
    }
});

// Función helper para rellenar desde sugerencias
function fillInput(text) {
    const input = document.getElementById('mainInput');
    input.value = text + " ";
    input.focus();
}