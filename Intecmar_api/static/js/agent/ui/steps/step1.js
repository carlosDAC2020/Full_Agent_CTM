import { mockDB } from '../../data/mocks.js';
import { store } from '../../data/store.js';
import { ingestCall, researchCall, appendDocsCall } from '../../api/agent.js';
import { pollTask } from '../../api/tasks.js';
import { getElements, updateStepper, getAssetUrl } from '../common.js';
import { loadHistory } from '../sidebar.js';

// Paso 1: Iniciar Análisis (Ingesta)
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
    loaderText.innerText = "Iniciando ingesta de convocatoria y extracción básica...";
    updateStepper(1);

    try {
        const fileInput = document.getElementById('file-upload');
        const files = fileInput ? fileInput.files : [];

        const { task_id, session_id } = await ingestCall(store.selectedCallText, files);
        store.sessionId = session_id;
        loadHistory(session_id);

        pollTask(
            task_id,
            (message) => { loaderText.innerText = message || "Procesando..."; },
            (result) => {
                renderStep1Result(result.data);
                getElements().step1.classList.remove('hidden');
            },
            (error) => {
                loaderText.innerText = "Error: " + error;
                loaderText.classList.add('text-red-500');
            }
        );

    } catch (err) {
        loaderText.innerText = "Error: " + err.message;
        loaderText.classList.add('text-red-500');
    }
}

// Fase 1.5: Iniciar Investigación Profunda
export async function startResearch() {
    if (!store.sessionId) return;

    const researchModal = document.getElementById('research-loading-modal');
    const statusText = document.getElementById('research-status-text');

    researchModal.classList.remove('hidden');
    statusText.innerText = "Conectando con agente de investigación...";

    try {
        const { task_id } = await researchCall(store.sessionId);

        pollTask(
            task_id,
            (message) => { statusText.innerText = message || "Analizando..."; },
            (result) => {
                renderStep1Result(result.data); // Refresca UI con presentación generada
                researchModal.classList.add('hidden');
            },
            (error) => {
                statusText.innerText = "Error crítico: " + error;
                statusText.classList.add('text-red-500');
                setTimeout(() => researchModal.classList.add('hidden'), 5000);
            }
        );
    } catch (err) {
        console.error(err);
        researchModal.classList.add('hidden');
        alert("Error iniciando investigación: " + err.message);
    }
}

// Fase 1.x: Añadir más documentos
export async function appendDocs(inputElement) {
    if (!store.sessionId || !inputElement.files.length) return;

    const files = inputElement.files;
    // UI Feedack simple (se podría mejorar)
    const btn = inputElement.previousElementSibling;
    const originalText = btn.innerHTML;
    btn.innerHTML = `<i class="ph ph-spinner animate-spin"></i> Subiendo...`;
    btn.disabled = true;

    try {
        const { task_id } = await appendDocsCall(store.sessionId, files);

        // Polling rápido para la vectorización
        pollTask(
            task_id,
            (msg) => { /* opcional status */ },
            (result) => {
                // Éxito: refrescar lista de docs
                renderStep1Result(result.data);
                btn.innerHTML = originalText;
                btn.disabled = false;
                inputElement.value = ''; // Reset input
            },
            (err) => {
                console.error(err);
                btn.innerHTML = `<i class="ph-bold ph-warning"></i> Error`;
                btn.classList.add('text-red-500');
            }
        );
    } catch (err) {
        console.error(err);
        btn.innerHTML = originalText;
        btn.disabled = false;
        alert("Error subiendo documentos: " + err.message);
    }
}

export function renderStep1Result(dataJson) {
    const { loader, step1 } = getElements();
    let data;
    try { data = typeof dataJson === 'string' ? JSON.parse(dataJson) : dataJson; }
    catch (e) { console.error("Error parsing JSON", e); return; }

    const callInfo = data.call_info || {};
    const docs = data.docs_paths || {};

    loader.classList.add('hidden');

    // Basic Info
    document.getElementById('res-title').innerText = callInfo.title || "Sin Título";
    document.getElementById('res-objective').innerText = callInfo.objective || "Sin objetivos detectados";
    document.getElementById('res-funding').innerText = callInfo.funding || "No especificado";
    document.getElementById('res-dates').innerText = callInfo.important_dates || callInfo.dates || "Fechas no detectadas";

    // Keywords (Visual Refresh)
    const tagsDiv = document.getElementById('res-keywords');
    tagsDiv.innerHTML = '';
    if (callInfo.keywords && Array.isArray(callInfo.keywords)) {
        callInfo.keywords.forEach(t => tagsDiv.innerHTML += `
            <span class="bg-gray-100 hover:bg-blue-50 text-gray-600 hover:text-blue-600 border border-gray-200 hover:border-blue-200 px-3 py-1.5 rounded-full text-xs font-semibold transition-all cursor-default select-none">
                #${t}
            </span>
        `);
    }

    // --- LOGICA DE ESTADO: ¿Investigación hecha? ---
    const presBtn = document.getElementById('btn-presentation-link');
    const researchContainer = document.getElementById('research-action-container');
    const historyContainer = document.getElementById('res-history-container');
    const historyList = document.getElementById('res-history-list');

    // 1. Botón Principal (Ver Presentación AND Iniciar/Regenerar Investigación)
    if (presBtn) {
        if (docs.presentation_oath_pdf) {
            presBtn.href = getAssetUrl(docs.presentation_oath_pdf);
            presBtn.target = "_blank";
            presBtn.classList.remove('hidden', 'opacity-50', 'pointer-events-none');
            presBtn.innerHTML = `
                <div class="w-8 h-8 rounded-full bg-red-500 text-white flex items-center justify-center shadow-sm group-hover:scale-110 transition-transform">
                    <i class="ph ph-presentation text-lg"></i>
                </div>
                <div class="text-left">
                    <div class="text-[10px] text-red-400 font-bold uppercase">Evaluación</div>
                    <div class="text-sm font-bold text-red-700">Ver Presentación</div>
                </div>
            `;
        } else {
            presBtn.classList.add('hidden');
        }
    }

    if (researchContainer) {
        researchContainer.classList.remove('hidden'); // Siempre visible si estamos aquí
        const researchBtnTitle = researchContainer.querySelector('h3');
        const researchBtnSubtitle = researchContainer.querySelector('p');
        const researchBtnIcon = researchContainer.querySelector('.ph-rocket-launch');

        if (docs.presentation_oath_pdf) {
            if (researchBtnTitle) researchBtnTitle.innerText = "Regenerar Análisis Técnico";
            if (researchBtnSubtitle) researchBtnSubtitle.innerText = "Actualiza el reporte con nuevos documentos o datos";
            if (researchBtnIcon) researchBtnIcon.className = "ph-fill ph-arrows-clockwise text-2xl"; // Cambio icono a recarga
        } else {
            if (researchBtnTitle) researchBtnTitle.innerText = "Iniciar Análisis Técnico Profundo";
            if (researchBtnSubtitle) researchBtnSubtitle.innerText = "Genera reporte técnico y presentación ejecutiva";
            if (researchBtnIcon) researchBtnIcon.className = "ph-fill ph-rocket-launch text-2xl";
        }
    }

    // 2. Historial de Versiones
    if (callInfo.presentation_history && Array.isArray(callInfo.presentation_history) && callInfo.presentation_history.length > 0) {
        historyContainer.classList.remove('hidden');
        historyList.innerHTML = '';

        // El actual es el que coincide con docs.presentation_oath_pdf
        const currentPdf = docs.presentation_oath_pdf;

        callInfo.presentation_history.forEach(ver => {
            const isLatest = ver.url === currentPdf;
            const absoluteUrl = getAssetUrl(ver.url);
            historyList.innerHTML += `
                <a href="${absoluteUrl}" target="_blank" 
                   class="flex items-center justify-between p-3 rounded-xl transition-all group mb-2
                          ${isLatest ? 'bg-blue-50 border-2 border-blue-200 shadow-sm' : 'bg-gray-50 hover:bg-white border border-transparent hover:border-gray-200'}"
                >
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-lg flex items-center justify-center ${isLatest ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-500'} group-hover:scale-110 transition-transform">
                            <i class="ph-fill ph-presentation"></i>
                        </div>
                        <div class="flex flex-col">
                            <span class="text-xs font-bold ${isLatest ? 'text-blue-900' : 'text-gray-700'}">${ver.name || 'Versión Anterior'}</span>
                            <span class="text-[9px] text-gray-400 font-medium">${ver.date || 'S/F'}</span>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        ${isLatest ? '<span class="text-[9px] font-black text-blue-500 bg-blue-100 px-2 py-0.5 rounded-md tracking-tighter">ACTUAL</span>' : ''}
                        <i class="ph-bold ph-download-simple ${isLatest ? 'text-blue-500' : 'text-gray-300 group-hover:text-blue-400'}"></i>
                    </div>
                </a>
             `;
        });
    } else {
        historyContainer.classList.add('hidden');
    }

    // 3. Documentos de Contexto
    const contextDocsContainer = document.getElementById('res-context-docs-container');
    const contextDocsDiv = document.getElementById('res-context-docs');

    if (contextDocsContainer && contextDocsDiv) {
        contextDocsDiv.innerHTML = '';
        if (callInfo.context_docs && Array.isArray(callInfo.context_docs) && callInfo.context_docs.length > 0) {
            contextDocsContainer.classList.remove('hidden');
            callInfo.context_docs.forEach(doc => {
                let docName = typeof doc === 'object' ? doc.name : doc;
                let docUrl = typeof doc === 'object' ? doc.url : doc;
                if (docName && docName.includes('/')) docName = docName.split('/').pop();

                const absoluteUrl = getAssetUrl(docUrl);

                contextDocsDiv.innerHTML += `
                    <a href="${absoluteUrl || '#'}" target="_blank" class="flex items-center p-3 bg-white border border-gray-100 rounded-xl hover:border-blue-200 hover:bg-blue-50/50 transition-all group shadow-sm">
                        <div class="w-10 h-10 bg-blue-50 text-blue-500 rounded-lg flex items-center justify-center group-hover:bg-blue-100 transition-colors">
                            <i class="ph ph-file-text text-xl"></i>
                        </div>
                        <div class="ml-3 overflow-hidden">
                            <div class="text-[11px] font-bold text-gray-800 truncate">${docName}</div>
                            <div class="text-[9px] text-gray-400 font-medium uppercase tracking-wider">Documento de Apoyo</div>
                        </div>
                        <i class="ph ph-arrow-square-out ml-auto text-gray-300 group-hover:text-blue-400"></i>
                    </a>
                `;
            });
        }
        // Nota: No ocultamos el container si está vacío porque ahora contiene el botón de subir más docs
        if (!callInfo.context_docs || callInfo.context_docs.length === 0) {
            // Solo si queremos ocultar la lista pero dejar el botón...
            // Dejamos el container visible para ver el botón "Añadir más"
            contextDocsContainer.classList.remove('hidden');
        }
    }
}
