import { store } from '../../data/store.js';
import { finalizeProject } from '../../api/agent.js';
import { pollTask } from '../../api/tasks.js';
import { getElements, updateStepper } from '../common.js';

// Paso 4: Resultados Finales
export async function generateFinal() {
    const { step3, loader, loaderText, step4 } = getElements();

    // UI Transition
    step3.classList.add('hidden');
    loader.classList.remove('hidden');
    loaderText.innerText = "Realizando investigación profunda, generando imágenes y redactando documentos finales...";
    updateStepper(4);

    try {
        // 1. Iniciar Tarea (API Real)
        const { task_id } = await finalizeProject(store.sessionId);

        // 2. Polling
        pollTask(
            task_id,
            (message) => {
                loaderText.innerText = message || "Procesando...";
            },
            (result) => {
                // Completado
                loader.classList.add('hidden');
                step4.classList.remove('hidden');

                // Renderizar datos reales
                if (result.data) {
                    const data = typeof result.data === 'string' ? JSON.parse(result.data) : result.data;
                    renderFinalResult(data);
                }
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

export function renderFinalResult(data) {
    console.log("Rendering final result:", data);
    const docs = data.docs_paths || {};
    const generalInfo = data.report_components?.general_info || {};
    const selectedIdea = data.selected_idea || {};
    const callInfo = data.call_info || {};

    // ----------------------------------------------------
    // COLUMNA IZQUIERDA: Poster + Botones
    // ----------------------------------------------------

    // 1. Configurar Poster
    const posterImg = document.getElementById('final-poster-img');
    const posterPlaceholder = document.getElementById('final-poster-placeholder');
    const posterOverlay = document.getElementById('poster-overlay');
    const viewPosterBtn = document.getElementById('btn-view-poster');

    if (docs.poster_image_path) {
        posterImg.src = docs.poster_image_path;
        posterImg.classList.remove('hidden');
        posterPlaceholder.classList.add('hidden');
        posterOverlay.classList.remove('hidden');

        // Botón ver en HD
        viewPosterBtn.onclick = () => window.open(docs.poster_image_path, '_blank');
    } else {
        posterImg.classList.add('hidden');
        posterPlaceholder.classList.remove('hidden');
        posterOverlay.classList.add('hidden');
    }

    // 2. Configurar Botón PDF
    const pdfBtn = document.getElementById('final-btn-pdf');
    if (docs.proyect_proposal_pdf) {
        pdfBtn.href = docs.proyect_proposal_pdf;
        pdfBtn.classList.remove('opacity-50', 'pointer-events-none');
        pdfBtn.classList.add('ring-2', 'ring-red-100', 'bg-red-50');
    } else {
        pdfBtn.classList.add('opacity-50', 'pointer-events-none');
        pdfBtn.href = '#';
    }

    // 3. Configurar Botón Markdown
    const mdBtn = document.getElementById('final-btn-md');
    if (docs.proyect_proposal_md) {
        mdBtn.href = docs.proyect_proposal_md;
        mdBtn.classList.remove('opacity-50', 'pointer-events-none');
        mdBtn.classList.add('ring-2', 'ring-gray-200', 'bg-gray-50');
    } else {
        mdBtn.classList.add('opacity-50', 'pointer-events-none');
        mdBtn.href = '#';
    }

    // ----------------------------------------------------
    // COLUMNA DERECHA: Información General
    // ----------------------------------------------------

    // Título
    const title = generalInfo.project_title || selectedIdea.idea_title || callInfo.title || "Proyecto Generado";
    document.getElementById('final-info-title').innerText = title;

    // Duración
    const duration = generalInfo.duration_months ? `${generalInfo.duration_months} meses` : "No especificada";
    document.getElementById('final-info-duration').innerText = duration;

    // Línea Temática
    const thematic = generalInfo.thematic_line || "General";
    document.getElementById('final-info-thematic').innerText = thematic;

    // Palabras Clave
    const keywordsContainer = document.getElementById('final-info-keywords');
    keywordsContainer.innerHTML = '';

    const keywords = generalInfo.keywords || callInfo.keywords || [];

    if (keywords.length > 0) {
        keywords.forEach(kw => {
            const badge = document.createElement('span');
            badge.className = "bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs border border-gray-200";
            badge.innerText = kw;
            keywordsContainer.appendChild(badge);
        });
    } else {
        keywordsContainer.innerHTML = '<span class="text-gray-400 text-sm italic">Sin palabras clave</span>';
    }
}
