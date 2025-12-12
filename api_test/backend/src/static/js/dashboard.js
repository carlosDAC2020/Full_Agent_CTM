// --- DATOS MOCK ---
const mockDB = {
    'minciencias': {
        title: "Convocatoria 966 Colombia Inteligente",
        objective: "Impulsar proyectos en tecnologías cuánticas e IA que generen un impacto medible en territorios.",
        funding: "No especificado",
        dates: "Cierre: Pendiente",
        tags: ["IA", "Cuántica", "Territorio"],
    }
};

const mockIdeas = [
    {
        id: 1,
        title: "Sistema de Monitoreo Fluvial con IA",
        desc: "Implementación de redes neuronales convolucionales para la detección de obstáculos en ríos de bajo calado.",
        objectives: ["Diseñar el modelo de visión por computadora.", "Validar datasets con imágenes satelitales.", "Prototipar dashboard de alertas."]
    },
    {
        id: 2,
        title: "Optimización Energética Cuántica Naval",
        desc: "Uso de algoritmos cuánticos para optimizar la distribución de carga y consumo de combustible en buques OPV.",
        objectives: ["Simular escenarios de carga con Qiskit.", "Comparar eficiencia vs algoritmos clásicos.", "Proponer arquitectura híbrida."]
    },
        {
        id: 3,
        title: "Gemelos Digitales para Astilleros 4.0",
        desc: "Creación de un entorno virtual para simular procesos de soldadura robótica utilizando aprendizaje por refuerzo.",
        objectives: ["Escanear planta física.", "Entrenar agentes de RL.", "Reducir desperdicio de material en un 15%."]
    }
];

let selectedValue = "";
let currentSelectedIdea = null;

// --- DOM Elements Generales ---
const initialView = document.getElementById('initial-view');
const resultsView = document.getElementById('results-view');
const previewPanel = document.getElementById('preview-panel');
const globalStepper = document.getElementById('global-stepper');
const loader = document.getElementById('generic-loader');
const loaderText = document.getElementById('loader-text');

// --- Funciones de Búsqueda (Heredadas y simplificadas) ---
function openDropdown() { document.getElementById('dropdown-options').classList.remove('hidden'); }
function filterOptions() {
    const input = document.getElementById('search-input');
    const opts = document.getElementById('dropdown-options');
    opts.innerHTML = `
        <div onclick="selectOption('minciencias')" class="px-4 py-3 hover:bg-blue-50 cursor-pointer flex items-center gap-3 border-l-4 border-transparent hover:border-cotecmar-light">
            <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center"><i class="ph ph-atom"></i></div>
            <div><div class="font-bold text-gray-800 text-sm">Convocatoria 966 Colombia Inteligente</div><div class="text-xs text-gray-400">IA, Cuántica</div></div>
        </div>
    `;
    opts.classList.remove('hidden');
}

function selectOption(val) {
    selectedValue = val;
    document.getElementById('search-input').value = mockDB[val].title;
    document.getElementById('dropdown-options').classList.add('hidden');
    
    // Show preview
    document.getElementById('prev-title').innerText = mockDB[val].title;
    document.getElementById('prev-desc').innerText = mockDB[val].objective;
    previewPanel.classList.remove('hidden');
}

function updateFileStatus() {
    const input = document.getElementById('file-upload');
    const dropZone = document.getElementById('drop-zone');
    if(input.files.length > 0) {
        dropZone.classList.add('border-green-400', 'bg-green-50/50');
        document.getElementById('upload-text-main').innerText = input.files.length + " Archivo(s)";
    }
}

// --- FLUJO DE PROCESO ---

// 1. Iniciar Análisis (Paso 1)
function startAnalysis() {
    if (!selectedValue) return;
    
    initialView.classList.add('animate-fade-out');
    setTimeout(() => {
        initialView.classList.add('hidden');
        resultsView.classList.remove('hidden');
        resultsView.classList.add('flex');
        globalStepper.classList.remove('hidden');
        
        document.getElementById('selected-label').innerText = mockDB[selectedValue].title;
        runStep1();
    }, 500);
}

function runStep1() {
    loader.classList.remove('hidden');
    loaderText.innerText = "Ingestando Convocatoria y Generando Evaluación...";
    updateStepper(1);

    setTimeout(() => {
        loader.classList.add('hidden');
        const data = mockDB[selectedValue];
        
        // Poblar datos Paso 1
        document.getElementById('res-title').innerText = data.title;
        document.getElementById('res-objective').innerText = data.objective;
        document.getElementById('res-funding').innerText = data.funding;
        document.getElementById('res-dates').innerText = data.dates;
        const tagsDiv = document.getElementById('res-keywords');
        tagsDiv.innerHTML = '';
        data.tags.forEach(t => tagsDiv.innerHTML += `<span class="bg-gray-100 px-2 py-1 rounded">#${t}</span>`);

        document.getElementById('step-1-ingest').classList.remove('hidden');
    }, 2000); 
}

// 2. Generar Ideas (Paso 2)
function goToStep2() {
    document.getElementById('step-1-ingest').classList.add('hidden');
    loader.classList.remove('hidden');
    loaderText.innerText = "Analizando oportunidades y generando ideas innovadoras...";
    updateStepper(2);

    setTimeout(() => {
        loader.classList.add('hidden');
        document.getElementById('step-2-ideas').classList.remove('hidden');
        renderIdeas();
    }, 2000);
}

function renderIdeas() {
    const container = document.getElementById('ideas-container');
    container.innerHTML = '';
    mockIdeas.forEach(idea => {
        const card = document.createElement('div');
        card.className = "bg-white p-5 rounded-xl border border-gray-200 hover:border-cotecmar-mid hover:shadow-lg transition-all cursor-pointer group relative";
        card.onclick = () => openEditIdea(idea);
        card.innerHTML = `
            <div class="flex justify-between items-start mb-2">
                <div class="font-bold text-gray-800 group-hover:text-cotecmar-mid transition-colors">${idea.title}</div>
                <i class="ph ph-pencil-simple text-gray-300 group-hover:text-cotecmar-mid"></i>
            </div>
            <p class="text-xs text-gray-500 line-clamp-2">${idea.desc}</p>
        `;
        container.appendChild(card);
    });
}

function openEditIdea(idea) {
    currentSelectedIdea = idea;
    // Ocultar grid, mostrar editor
    document.getElementById('ideas-container').classList.add('hidden');
    const editor = document.getElementById('idea-editor');
    editor.classList.remove('hidden');

    document.getElementById('edit-title').value = idea.title;
    document.getElementById('edit-desc').value = idea.desc;
    document.getElementById('edit-objectives').value = idea.objectives.join('\n');
}

function cancelEdit() {
    document.getElementById('idea-editor').classList.add('hidden');
    document.getElementById('ideas-container').classList.remove('hidden');
}

// 3. Confirmar Idea y Generar Esquema (Paso 3)
function confirmIdea() {
    // Guardar cambios (simulado)
    currentSelectedIdea.title = document.getElementById('edit-title').value;
    currentSelectedIdea.desc = document.getElementById('edit-desc').value;
    const objsRaw = document.getElementById('edit-objectives').value;
    currentSelectedIdea.objectives = objsRaw.split('\n');

    document.getElementById('step-2-ideas').classList.add('hidden');
    loader.classList.remove('hidden');
    loaderText.innerText = "Estructurando esquema inicial del proyecto...";
    updateStepper(3);

    setTimeout(() => {
        loader.classList.add('hidden');
        document.getElementById('step-3-schema').classList.remove('hidden');
        
        // Poblar Documento Mock
        document.getElementById('schema-title').innerText = currentSelectedIdea.title;
        document.getElementById('schema-desc').innerText = currentSelectedIdea.desc + " Este proyecto busca alinearse con los objetivos estratégicos de la convocatoria mediante la implementación de tecnología de vanguardia...";
        const ul = document.getElementById('schema-objs');
        ul.innerHTML = '';
        currentSelectedIdea.objectives.forEach(o => {
            if(o.trim()) ul.innerHTML += `<li>${o}</li>`;
        });
    }, 2000);
}

// 4. Generación Final (Paso 4)
function generateFinal() {
    document.getElementById('step-3-schema').classList.add('hidden');
    loader.classList.remove('hidden');
    loaderText.innerText = "Realizando investigación profunda y redactando documentos finales...";
    updateStepper(4);

    setTimeout(() => {
        loader.classList.add('hidden');
        document.getElementById('step-4-final').classList.remove('hidden');
    }, 3000); // Un poco más largo para simular trabajo pesado
}

// --- Utilidades ---
function updateStepper(step) {
    for(let i=1; i<=4; i++) {
        const el = document.getElementById(`step-dot-${i}`);
        if (i === step) el.className = "text-cotecmar-mid font-bold underline decoration-2 underline-offset-4";
        else if (i < step) el.className = "text-gray-800";
        else el.className = "text-gray-300";
    }
}

function resetInterface() {
    location.reload(); // Simple reset
}

function toggleSidebar() {
    const sb = document.getElementById('sidebar');
    sb.classList.toggle('w-64');
    sb.classList.toggle('w-0');
    sb.classList.toggle('p-0');
}