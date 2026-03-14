import { store } from '../../data/store.js';
import { finalizeProject, regenerateReport, regeneratePoster as apiRegeneratePoster } from '../../api/agent.js';
import { getElements, updateStepper, getAssetUrl } from '../common.js';
import { renderFinalResult } from './steps/step4.js';

// ==========================================
// EDITOR MODAL LOGIC (New Feature)
// ==========================================

let currentSection = 'executive_summary';

export function openEditModal() {
    const modal = document.getElementById('edit-report-modal');
    // Pre-cargar datos del store
    // Suponemos que store.finalData contiene el JSON del resultado
    if (store.finalData) {
        // Cargar sección por defecto
        loadSectionContent();
    }
    modal.classList.remove('hidden');
}

export function closeEditModal() {
    const modal = document.getElementById('edit-report-modal');
    modal.classList.add('hidden');
}

export function switchEditTab(tab) {
    const tabContent = document.getElementById('tab-content');
    const tabVisuals = document.getElementById('tab-visuals');
    const btnContent = document.getElementById('tab-btn-content');
    const btnVisuals = document.getElementById('tab-btn-visuals');

    if (tab === 'content') {
        tabContent.classList.remove('hidden');
        tabVisuals.classList.add('hidden');
        btnContent.classList.add('border-blue-500', 'text-blue-600', 'border-b-2');
        btnContent.classList.remove('border-transparent', 'text-gray-500', 'hover:border-gray-300');
        btnVisuals.classList.remove('border-blue-500', 'text-blue-600', 'border-b-2');
        btnVisuals.classList.add('border-transparent', 'text-gray-500', 'hover:border-gray-300');
    } else {
        tabContent.classList.add('hidden');
        tabVisuals.classList.remove('hidden');
        btnVisuals.classList.add('border-blue-500', 'text-blue-600', 'border-b-2');
        btnVisuals.classList.remove('border-transparent', 'text-gray-500', 'hover:border-gray-300');
        btnContent.classList.remove('border-blue-500', 'text-blue-600', 'border-b-2');
        btnContent.classList.add('border-transparent', 'text-gray-500', 'hover:border-gray-300');
    }
}

export function loadSectionContent() {
    const selector = document.getElementById('section-selector');
    const editor = document.getElementById('markdown-editor');
    const preview = document.getElementById('markdown-preview');

    currentSection = selector.value;

    // Obtener contenido actual del store
    // Estructura esperada: store.finalData.report_components[section]

    let content = "";
    if (store.finalData && store.finalData.report_components) {
        content = store.finalData.report_components[currentSection] || "";
    }

    editor.value = content;

    // Render simple preview (for now just text, later markdown parser)
    // Usamos marked si está disponible, o texto plano
    if (window.marked) {
        preview.innerHTML = window.marked.parse(content);
    } else {
        preview.innerText = content;
    }

    // Auto-update preview on type
    editor.oninput = () => {
        if (store.finalData && store.finalData.report_components) {
            store.finalData.report_components[currentSection] = editor.value;
        }
        if (window.marked) {
            preview.innerHTML = window.marked.parse(editor.value);
        } else {
            preview.innerText = editor.value;
        }
    };
}

export async function saveAndRegenerateReport() {
    const btn = document.getElementById('btn-save-changes');
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="ph ph-spinner animate-spin"></i> Regenerando...';

    try {
        // Enviar datos actualizados al backend
        // Endpoint: POST /api/agent/regenerate_report
        // Payload: { session_id, report_components: ... }

        const payload = {
            session_id: store.sessionId,
            report_components: store.finalData.report_components
        };

        const result = await regenerateReport(payload);

        // Actualizar UI con nuevos paths
        if (result && result.docs_paths) {
            // Merge docs_paths
            store.finalData.docs_paths = { ...store.finalData.docs_paths, ...result.docs_paths };
            renderFinalResult(store.finalData);
            closeEditModal();
            // Show success toast or similar?
        }

    } catch (error) {
        console.error("Error regenerating report:", error);
        alert("Error al regenerar el reporte: " + error.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

export async function regeneratePoster() {
    const promptInput = document.getElementById('poster-style-prompt');
    const prompt = promptInput.value;

    if (!prompt) {
        alert("Por favor ingresa un prompt de estilo visual.");
        return;
    }

    const loader = document.getElementById('poster-loader');
    loader.classList.remove('hidden');

    try {
        // Enviar prompt al backend
        const result = await apiRegeneratePoster(store.sessionId, prompt);

        if (result && result.poster_path) {
            const absoluteUrl = getAssetUrl(result.poster_path);
            document.getElementById('edit-poster-preview').src = absoluteUrl;
            // Update final view too
            const finalPoster = document.getElementById('final-poster-img');
            finalPoster.src = absoluteUrl;
            store.finalData.docs_paths.poster_image_path = result.poster_path;
        }
    } catch (error) {
        console.error("Error generating poster:", error);
        alert("Error generando poster: " + error.message);
    } finally {
        loader.classList.add('hidden');
    }
}
