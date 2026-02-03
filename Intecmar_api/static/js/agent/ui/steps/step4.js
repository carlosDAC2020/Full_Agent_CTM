import { store } from '../../data/store.js';
import { finalizeProject } from '../../api/agent.js';
import { pollTask } from '../../api/tasks.js';
import { getElements, updateStepper, getAssetUrl } from '../common.js';
import { loadHistory } from '../sidebar.js';
import '../modals/allianceModal.js'; // Importante para registrar funciones globales del modal

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
        const config = store.generationConfig || {};
        console.log("📤 Sending Generation Config:", config);
        const { task_id } = await finalizeProject(store.sessionId, config);

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
                loadHistory(store.sessionId);

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
    // Persist to store so modals can access it
    store.finalResult = data;

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

    if (docs.poster_image_path && posterImg) {
        // Cache-busting: add timestamp to ensure refresh
        const timestamp = new Date().getTime();
        const absoluteUrl = getAssetUrl(docs.poster_image_path) + `?t=${timestamp}`;

        posterImg.src = absoluteUrl;
        posterImg.classList.remove('hidden');
        if (posterPlaceholder) posterPlaceholder.classList.add('hidden');
        if (posterOverlay) posterOverlay.classList.remove('hidden');

        // Botón ver en HD
        if (viewPosterBtn) {
            viewPosterBtn.onclick = () => window.open(absoluteUrl, '_blank');
        }
    } else if (posterImg) {
        posterImg.classList.add('hidden');
        if (posterPlaceholder) posterPlaceholder.classList.remove('hidden');
        if (posterOverlay) posterOverlay.classList.add('hidden');
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

    // ----------------------------------------------------
    // ALIANZAS (NUEVO)
    // ----------------------------------------------------
    renderFinalAlliances(generalInfo);

    // ----------------------------------------------------
    // HISTORIAL DE VERSIONES (SLIDER)
    // ----------------------------------------------------
    const history = data.generation_history || [];
    const posterCard = document.getElementById('final-poster-img')?.parentElement;

    if (history.length > 0 && posterCard) {
        setupHistorySlider(posterCard, history, docs);
    }
}

// Listen for updates from Alliance Modal (Breaking circular dependency)
window.addEventListener('poster-updated', (e) => {
    console.log("📢 Poster Update Event received in step4.js");
    console.log("   General Info:", e.detail?.report_components?.general_info);

    // For alliance updates, we only need to refresh the alliance display
    // The poster/slider may have replaced the original elements
    const generalInfo = e.detail?.report_components?.general_info || {};
    renderFinalAlliances(generalInfo);

    // Also update the history slider if it exists
    const history = e.detail?.generation_history || [];
    const posterCard = document.getElementById('final-poster-img')?.parentElement;
    if (history.length > 0 && posterCard) {
        setupHistorySlider(posterCard, history, e.detail?.docs_paths || {});
    }
});

function renderFinalAlliances(info) {
    const executorName = info.executor_entity;
    const executorLogo = info.executor_entity_logo;
    const coexecutors = info.coejecutors_entities || [];
    const coexecutorsLogos = info.coejecutors_entities_logos || [];
    const collaborators = info.collaborators_entities || [];
    const collaboratorsLogos = info.collaborators_entities_logos || [];

    const hasAny = executorName || coexecutors.length > 0 || collaborators.length > 0;

    // Toggle main container vs placeholder
    document.getElementById('final-no-alliances').classList.toggle('hidden', hasAny);

    // 1. Executor
    const execContainer = document.getElementById('final-executor-display');
    if (executorName && execContainer) {
        execContainer.classList.remove('hidden');
        const nameEl = document.getElementById('final-executor-name');
        if (nameEl) nameEl.innerText = executorName;

        const img = document.getElementById('final-executor-img');
        if (img) {
            if (executorLogo) {
                img.src = getAssetUrl(executorLogo);
                img.classList.remove('hidden');
            } else {
                img.classList.add('hidden');
            }
        }
    } else if (execContainer) {
        execContainer.classList.add('hidden');
    }

    // 2. Coexecutors
    const coexecList = document.getElementById('final-coexecutors-list');
    if (coexecList) {
        coexecList.innerHTML = '';
        coexecutors.forEach((name, i) => {
            const logo = coexecutorsLogos[i];
            coexecList.appendChild(createAllianceChip(name, logo, 'blue'));
        });
    }

    // 3. Collaborators
    const collabList = document.getElementById('final-collaborators-list');
    if (collabList) {
        collabList.innerHTML = '';
        collaborators.forEach((name, i) => {
            const logo = collaboratorsLogos[i];
            collabList.appendChild(createAllianceChip(name, logo, 'purple'));
        });
    }
}

function createAllianceChip(name, logo, color) {
    const div = document.createElement('div');
    // Using simple chip style
    div.className = `flex items-center gap-2 bg-${color}-50 px-2 py-1 rounded-lg border border-${color}-100`;

    if (logo) {
        const img = document.createElement('img');
        img.src = getAssetUrl(logo);
        img.className = "w-5 h-5 object-contain bg-white rounded border border-gray-100";
        div.appendChild(img);
    }

    const span = document.createElement('span');
    span.className = `text-xs font-bold text-${color}-800`;
    span.innerText = name;
    div.appendChild(span);

    return div;
}

function setupHistorySlider(container, history, currentDocs) {
    // 1. Limpiar contenedor para el slider
    container.innerHTML = '';
    // Usamos un fondo oscuro inmersivo
    container.className = "relative w-full min-h-[600px] bg-slate-950 rounded-[2rem] overflow-hidden shadow-2xl group border border-white/5";

    let currentIndex = history.length - 1;

    // 2. Render inicial
    renderSlide(currentIndex, null);

    function renderSlide(idx, direction) {
        const item = history[idx];
        const isLatest = idx === history.length - 1;
        const timestamp = new Date(item.timestamp);
        const dateStr = timestamp.toLocaleDateString() + " " + timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        // Crear diapositiva
        const slide = document.createElement('div');
        slide.className = "absolute inset-0 w-full h-full transition-all duration-500 ease-in-out transform";

        if (direction === 'next') {
            slide.classList.add('translate-x-full', 'opacity-0');
        } else if (direction === 'prev') {
            slide.classList.add('-translate-x-full', 'opacity-0');
        } else {
            slide.classList.add('opacity-100');
        }

        // --- Contenido del Slide ---

        // 1. Fondo difuminado (Inmersivo)
        const bgBlur = document.createElement('div');
        const imgUrl = getAssetUrl(item.poster_path);
        const fullImgUrl = imgUrl.startsWith('blob:') ? imgUrl : imgUrl + `?t=${new Date().getTime()}`;
        bgBlur.className = "absolute inset-0 bg-cover bg-center opacity-40 scale-110 blur-2xl brightness-50 pointer-events-none transition-all duration-700";
        bgBlur.style.backgroundImage = `url("${fullImgUrl}")`;
        slide.appendChild(bgBlur);

        // 2. Imagen Principal
        const img = document.createElement('img');
        img.src = fullImgUrl;
        img.className = "relative w-full h-full object-contain drop-shadow-[0_20px_60px_rgba(0,0,0,0.8)] z-10 select-none";
        slide.appendChild(img);

        // 3. Info de Versión (ESTILO "VERSION 4" IMAGE)
        const infoOverlay = document.createElement('div');
        infoOverlay.className = "absolute top-6 left-6 flex flex-col gap-2 z-30 pointer-events-none";
        infoOverlay.innerHTML = `
            <div class="bg-blue-600 text-white text-[10px] px-4 py-1.5 rounded-lg font-black uppercase tracking-[0.1em] shadow-lg w-fit">
                VERSIÓN ${idx + 1} ${isLatest ? ' (ACTUAL)' : ''}
            </div>
            <div class="flex items-center gap-2 bg-black/70 backdrop-blur-md px-3 py-1.5 rounded-lg w-fit border border-white/10 text-white shadow-xl">
                <i class="ph-bold ph-calendar text-white opacity-80"></i>
                <p class="text-[11px] font-bold uppercase tracking-wider">${dateStr}</p>
            </div>
        `;
        slide.appendChild(infoOverlay);

        // 4. Icono Superior Derecho (Giroscopio/Mundo)
        const topIcon = document.createElement('div');
        topIcon.className = "absolute top-6 right-6 w-10 h-10 bg-black/40 backdrop-blur-md rounded-full flex items-center justify-center text-white z-30 border border-white/10 shadow-lg";
        topIcon.innerHTML = `<i class="ph-fill ph-globe text-xl"></i>`;
        slide.appendChild(topIcon);

        // 5. Botones de Acción (Overlay al final)
        const actionOverlay = document.createElement('div');
        actionOverlay.className = "absolute bottom-10 left-0 right-0 flex justify-center gap-4 px-6 z-40 transition-all duration-400 transform translate-y-6 opacity-0 group-hover:translate-y-0 group-hover:opacity-100";

        if (item.pdf_path) {
            const pdfA = document.createElement('a');
            pdfA.href = getAssetUrl(item.pdf_path);
            pdfA.target = "_blank";
            pdfA.className = "flex items-center gap-2 bg-white/95 text-red-600 px-6 py-4 rounded-2xl font-black shadow-2xl hover:bg-red-600 hover:text-white transition-all transform hover:-translate-y-1 text-xs uppercase tracking-widest";
            pdfA.innerHTML = `<i class="ph-fill ph-file-pdf text-xl"></i> <span>DESCARGAR PDF</span>`;
            actionOverlay.appendChild(pdfA);
        }

        if (item.md_path) {
            const mdA = document.createElement('a');
            mdA.href = getAssetUrl(item.md_path);
            mdA.target = "_blank";
            mdA.className = "flex items-center gap-2 bg-white/95 text-slate-800 px-6 py-4 rounded-2xl font-black shadow-2xl hover:bg-slate-800 hover:text-white transition-all transform hover:-translate-y-1 text-xs uppercase tracking-widest";
            mdA.innerHTML = `<i class="ph-fill ph-markdown-logo text-xl"></i> <span>FUENTES MD</span>`;
            actionOverlay.appendChild(mdA);
        }
        slide.appendChild(actionOverlay);

        container.appendChild(slide);

        // --- Animación ---
        if (direction) {
            requestAnimationFrame(() => {
                slide.classList.remove('translate-x-full', '-translate-x-full', 'opacity-0');
                slide.classList.add('translate-x-0', 'opacity-100');
            });

            // Limpieza
            const oldSlides = Array.from(container.children).filter(child => child !== slide && !child.classList.contains('nav-arrow') && !child.classList.contains('progress-bar'));
            oldSlides.forEach(oldSlide => {
                oldSlide.classList.add('opacity-0');
                if (direction === 'next') oldSlide.classList.add('-translate-x-full');
                else oldSlide.classList.add('translate-x-full');
                setTimeout(() => {
                    if (oldSlide.parentNode === container) container.removeChild(oldSlide);
                }, 500);
            });
        }
    }

    // --- Controles de Navegación (Estilo Círculo Blanco) ---
    if (history.length > 1) {
        const prevBtn = document.createElement('button');
        prevBtn.className = "nav-arrow absolute left-6 top-1/2 -translate-y-1/2 w-14 h-14 bg-white/10 hover:bg-white/30 backdrop-blur-2xl rounded-full flex items-center justify-center text-white transition-all z-50 hover:scale-110 active:scale-95 shadow-2xl group-hover:opacity-100 opacity-0 border border-white/20";
        prevBtn.innerHTML = `<i class="ph ph-caret-left text-2xl font-bold"></i>`;
        prevBtn.onclick = (e) => {
            e.stopPropagation();
            if (currentIndex > 0) {
                currentIndex--;
                renderSlide(currentIndex, 'prev');
                updateArrows();
            }
        };
        container.appendChild(prevBtn);

        const nextBtn = document.createElement('button');
        nextBtn.className = "nav-arrow absolute right-6 top-1/2 -translate-y-1/2 w-14 h-14 bg-white/10 hover:bg-white/30 backdrop-blur-2xl rounded-full flex items-center justify-center text-white transition-all z-50 hover:scale-110 active:scale-95 shadow-2xl group-hover:opacity-100 opacity-0 border border-white/20";
        nextBtn.innerHTML = `<i class="ph ph-caret-right text-2xl font-bold"></i>`;
        nextBtn.onclick = (e) => {
            e.stopPropagation();
            if (currentIndex < history.length - 1) {
                currentIndex++;
                renderSlide(currentIndex, 'next');
                updateArrows();
            }
        };
        container.appendChild(nextBtn);

        function updateArrows() {
            prevBtn.style.visibility = currentIndex === 0 ? 'hidden' : 'visible';
            nextBtn.style.visibility = currentIndex === history.length - 1 ? 'hidden' : 'visible';
        }
        updateArrows();
    }

    // Progress Bar
    const progress = document.createElement('div');
    progress.className = "progress-bar absolute bottom-0 left-0 h-1.5 bg-blue-500 shadow-[0_0_20px_rgba(59,130,246,0.8)] transition-all duration-700 z-[60]";
    progress.style.width = `${((currentIndex + 1) / history.length) * 100}%`;
    container.appendChild(progress);
}
