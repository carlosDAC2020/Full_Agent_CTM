import { mockDB } from '../../data/mocks.js';
import { store } from '../../data/store.js';
import { ingestCall } from '../../api/agent.js';
import { pollTask } from '../../api/tasks.js';
import { getElements, updateStepper } from '../common.js';
import { loadHistory } from '../sidebar.js'; // Helper for sidebar updates

// Paso 1: Iniciar Análisis
export async function startAnalysis() {
    const { initialView, resultsView, globalStepper, loader, loaderText } = getElements();
    if (!store.selectedValue) return;

    // UI Transitions
    initialView.classList.add('animate-fade-out');
    setTimeout(() => {
        initialView.classList.add('hidden');
        resultsView.classList.remove('hidden');
        resultsView.classList.add('flex');
        globalStepper.classList.remove('hidden');
    }, 500);

    // Call API
    loader.classList.remove('hidden');
    loaderText.innerText = "Iniciando ingesta de convocatoria...";
    updateStepper(1);

    try {
        // 1. Start Ingestion Task
        const fileInput = document.getElementById('file-upload');
        const files = fileInput ? fileInput.files : [];

        const { task_id, session_id } = await ingestCall(store.selectedCallText, files);
        store.sessionId = session_id;
        loadHistory(session_id); // Refresh history with new session

        // 2. Poll Task Progress
        pollTask(
            task_id,
            (message) => {
                // Update loader text with progress message from backend
                loaderText.innerText = message || "Procesando...";
            },
            (result) => {
                // On Complete
                renderStep1Result(result.data);
                // Fix: Explicitly show step 1 ONLY here, when user initiates analysis
                getElements().step1.classList.remove('hidden');
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

export function renderStep1Result(dataJson) {
    const { loader, step1 } = getElements();

    // Parse backend data (which is a JSON string inside the result wrapper)
    let data;
    try {
        data = typeof dataJson === 'string' ? JSON.parse(dataJson) : dataJson;
    } catch (e) { console.error("Error parsing JSON", e); return; }

    const callInfo = data.call_info || {};
    const docs = data.docs_paths || {}; // URLs of generated docs

    // Hide Loader
    loader.classList.add('hidden');

    // Populate UI
    document.getElementById('res-title').innerText = callInfo.title || "Sin Título";
    document.getElementById('res-objective').innerText = callInfo.objective || "Sin objetivos detectados";
    document.getElementById('res-funding').innerText = callInfo.funding || "No especificado";

    // Keywords
    const tagsDiv = document.getElementById('res-keywords');
    tagsDiv.className = "flex flex-wrap gap-2 mt-2"; // Better container styling
    tagsDiv.innerHTML = '';
    if (callInfo.keywords && Array.isArray(callInfo.keywords)) {
        callInfo.keywords.forEach(t => tagsDiv.innerHTML += `
            <span class="bg-blue-50 text-blue-700 border border-blue-100 px-2 py-1 rounded-md shadow-sm text-xs font-medium whitespace-nowrap">#${t}</span>
        `);
    }

    // Dates 
    document.getElementById('res-dates').innerText = callInfo.dates || "Fechas no detectadas";

    // Update Presentation Link: Use correct key 'presentation_oath_pdf' from state.py
    const presBtn = document.getElementById('btn-presentation-link');
    if (presBtn && docs.presentation_oath_pdf) {
        presBtn.href = docs.presentation_oath_pdf;
        presBtn.target = "_blank";
        presBtn.classList.remove('opacity-50', 'pointer-events-none');

        // Visual indicator that it is ready
        presBtn.classList.add('animate-pulse-slow');
        setTimeout(() => presBtn.classList.remove('animate-pulse-slow'), 3000);
    } else if (presBtn) {
        presBtn.classList.add('opacity-50', 'pointer-events-none');
    }

    // Fix: Do NOT unhide step1 here. This function is shared with restoreSession.
    // step1.classList.remove('hidden'); 
}
