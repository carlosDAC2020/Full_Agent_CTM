import { mockDB, mockIdeas } from '../data/mocks.js';
import { store } from '../data/store.js';

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
export function startAnalysis() {
    const { initialView, resultsView, globalStepper } = getElements();
    if (!store.selectedValue) return;

    initialView.classList.add('animate-fade-out');
    setTimeout(() => {
        initialView.classList.add('hidden');
        resultsView.classList.remove('hidden');
        resultsView.classList.add('flex');
        globalStepper.classList.remove('hidden');

        document.getElementById('selected-label').innerText = mockDB[store.selectedValue].title;
        runStep1();
    }, 500);
}

function runStep1() {
    const { loader, loaderText, step1 } = getElements();
    loader.classList.remove('hidden');
    loaderText.innerText = "Ingestando Convocatoria y Generando Evaluación...";
    updateStepper(1);

    setTimeout(() => {
        loader.classList.add('hidden');
        const data = mockDB[store.selectedValue];

        document.getElementById('res-title').innerText = data.title;
        document.getElementById('res-objective').innerText = data.objective;
        document.getElementById('res-funding').innerText = data.funding;
        document.getElementById('res-dates').innerText = data.dates;
        const tagsDiv = document.getElementById('res-keywords');
        tagsDiv.innerHTML = '';
        data.tags.forEach(t => tagsDiv.innerHTML += `<span class="bg-gray-100 px-2 py-1 rounded">#${t}</span>`);

        step1.classList.remove('hidden');
    }, 2000);
}

// Paso 2
export function goToStep2() {
    const { step1, loader, loaderText, step2 } = getElements();
    step1.classList.add('hidden');
    loader.classList.remove('hidden');
    loaderText.innerText = "Analizando oportunidades y generando ideas innovadoras...";
    updateStepper(2);

    setTimeout(() => {
        loader.classList.add('hidden');
        step2.classList.remove('hidden');
        renderIdeas();
    }, 2000);
}

function renderIdeas() {
    const { ideasContainer } = getElements();
    ideasContainer.innerHTML = '';
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
        ideasContainer.appendChild(card);
    });
}

function openEditIdea(idea) {
    const { ideasContainer, ideaEditor } = getElements();
    store.currentSelectedIdea = idea;
    ideasContainer.classList.add('hidden');
    ideaEditor.classList.remove('hidden');

    document.getElementById('edit-title').value = idea.title;
    document.getElementById('edit-desc').value = idea.desc;
    document.getElementById('edit-objectives').value = idea.objectives.join('\n');
}

export function cancelEdit() {
    const { ideasContainer, ideaEditor } = getElements();
    ideaEditor.classList.add('hidden');
    ideasContainer.classList.remove('hidden');
}

// Paso 3
export function confirmIdea() {
    const { step2, loader, loaderText, step3 } = getElements();

    // Guardar cambios mock
    if (store.currentSelectedIdea) {
        store.currentSelectedIdea.title = document.getElementById('edit-title').value;
        store.currentSelectedIdea.desc = document.getElementById('edit-desc').value;
        const objsRaw = document.getElementById('edit-objectives').value;
        store.currentSelectedIdea.objectives = objsRaw.split('\n');
    }

    step2.classList.add('hidden');
    loader.classList.remove('hidden');
    loaderText.innerText = "Estructurando esquema inicial del proyecto...";
    updateStepper(3);

    setTimeout(() => {
        loader.classList.add('hidden');
        step3.classList.remove('hidden');

        document.getElementById('schema-title').innerText = store.currentSelectedIdea.title;
        document.getElementById('schema-desc').innerText = store.currentSelectedIdea.desc + " Este proyecto busca alinearse con los objetivos estratégicos...";
        const ul = document.getElementById('schema-objs');
        ul.innerHTML = '';
        store.currentSelectedIdea.objectives.forEach(o => {
            if (o.trim()) ul.innerHTML += `<li>${o}</li>`;
        });
    }, 2000);
}

// Paso 4
export function generateFinal() {
    const { step3, loader, loaderText, step4 } = getElements();
    step3.classList.add('hidden');
    loader.classList.remove('hidden');
    loaderText.innerText = "Realizando investigación profunda y redactando documentos finales...";
    updateStepper(4);

    setTimeout(() => {
        loader.classList.add('hidden');
        step4.classList.remove('hidden');
    }, 3000);
}
