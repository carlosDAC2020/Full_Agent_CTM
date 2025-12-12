/* src/static/js/dashboard.js */

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
    }
];

let selectedValue = "";
let currentSelectedIdea = null;

// Referencias DOM se inicializan cuando carga la página
document.addEventListener('DOMContentLoaded', () => {
    // Inicializaciones si fueran necesarias
});

function openDropdown() { document.getElementById('dropdown-options').classList.remove('hidden'); }

function filterOptions() {
    // Lógica simplificada para el ejemplo
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
    
    document.getElementById('prev-title').innerText = mockDB[val].title;
    document.getElementById('prev-desc').innerText = mockDB[val].objective;
    document.getElementById('preview-panel').classList.remove('hidden');
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
function startAnalysis() {
    if (!selectedValue) return;
    const initialView = document.getElementById('initial-view');
    const resultsView = document.getElementById('results-view');
    const globalStepper = document.getElementById('global-stepper');
    
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
    const loader = document.getElementById('generic-loader');
    loader.classList.remove('hidden');
    document.getElementById('loader-text').innerText = "Ingestando Convocatoria y Generando Evaluación...";
    updateStepper(1);

    setTimeout(() => {
        loader.classList.add('hidden');
        const data = mockDB[selectedValue];
        
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

function goToStep2() {
    document.getElementById('step-1-ingest').classList.add('hidden');
    const loader = document.getElementById('generic-loader');
    loader.classList.remove('hidden');
    document.getElementById('loader-text').innerText = "Analizando oportunidades y generando ideas innovadoras...";
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
    document.getElementById('ideas-container').classList.add('hidden');
    document.getElementById('idea-editor').classList.remove('hidden');

    document.getElementById('edit-title').value = idea.title;
    document.getElementById('edit-desc').value = idea.desc;
    document.getElementById('edit-objectives').value = idea.objectives.join('\n');
}

function cancelEdit() {
    document.getElementById('idea-editor').classList.add('hidden');
    document.getElementById('ideas-container').classList.remove('hidden');
}

function confirmIdea() {
    currentSelectedIdea.title = document.getElementById('edit-title').value;
    currentSelectedIdea.desc = document.getElementById('edit-desc').value;
    const objsRaw = document.getElementById('edit-objectives').value;
    currentSelectedIdea.objectives = objsRaw.split('\n');

    document.getElementById('step-2-ideas').classList.add('hidden');
    const loader = document.getElementById('generic-loader');
    loader.classList.remove('hidden');
    document.getElementById('loader-text').innerText = "Estructurando esquema inicial del proyecto...";
    updateStepper(3);

    setTimeout(() => {
        loader.classList.add('hidden');
        document.getElementById('step-3-schema').classList.remove('hidden');
        
        document.getElementById('schema-title').innerText = currentSelectedIdea.title;
        document.getElementById('schema-desc').innerText = currentSelectedIdea.desc;
        const ul = document.getElementById('schema-objs');
        ul.innerHTML = '';
        currentSelectedIdea.objectives.forEach(o => {
            if(o.trim()) ul.innerHTML += `<li>${o}</li>`;
        });
    }, 2000);
}

function generateFinal() {
    document.getElementById('step-3-schema').classList.add('hidden');
    const loader = document.getElementById('generic-loader');
    loader.classList.remove('hidden');
    document.getElementById('loader-text').innerText = "Realizando investigación profunda...";
    updateStepper(4);

    setTimeout(() => {
        loader.classList.add('hidden');
        document.getElementById('step-4-final').classList.remove('hidden');
    }, 3000);
}

function updateStepper(step) {
    for(let i=1; i<=4; i++) {
        const el = document.getElementById(`step-dot-${i}`);
        if (i === step) el.className = "text-cotecmar-mid font-bold underline decoration-2 underline-offset-4";
        else if (i < step) el.className = "text-gray-800";
        else el.className = "text-gray-300";
    }
}

function resetInterface() {
    location.reload();
}

function toggleSidebar() {
    const sb = document.getElementById('sidebar');
    sb.classList.toggle('w-64');
    sb.classList.toggle('w-0');
    sb.classList.toggle('p-0');
}