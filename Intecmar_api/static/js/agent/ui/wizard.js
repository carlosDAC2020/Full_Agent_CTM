// Wizard Orchestrator
// Centralizes imports/exports for the application

import { store } from '../data/store.js';
import { getElements, updateFileStatus } from './common.js';
import { loadHistory } from './sidebar.js';

// Common Utilities
export { updateFileStatus, navigateToStep } from './common.js';

// Step Logic
// Step Logic
export { startAnalysis, startResearch, appendDocs, openIdeaConfigModal, closeIdeaConfigModal, confirmIdeaGeneration } from './steps/step1.js';
export { goToStep2, cancelEdit } from './steps/step2.js';
export { confirmIdea, openConfigModal, closeConfigModal, saveConfigAndGenerate, resetStep3State } from './steps/step3.js';
export { generateFinal } from './steps/step4.js';

// Session Management
export { restoreSession } from './session_manager.js';

// --- Global Reset Logic ---
export function resetInterface() {
    const { initialView, resultsView, globalStepper, step1, step2, step3, step4 } = getElements();

    // 1. Reset Store
    store.sessionId = null;
    store.maxReachedStep = 1;
    store.selectedValue = null;
    store.selectedCallText = null;
    store.currentSelectedIdea = null;
    store.finalResult = null;
    store.callInfo = null;
    store.selectedThematicLine = null;
    store.selectedMethodology = null;
    store.generationConfig = null;
    store.allianceLogos = {};

    // 2. Reset UI Views
    resultsView.classList.add('hidden');
    resultsView.classList.remove('flex');
    globalStepper.classList.add('hidden');

    // Show Initial View
    initialView.classList.remove('hidden');
    initialView.classList.remove('animate-fade-out'); // Ensure it's visible

    // 3. Reset Steps Visibility
    step1.classList.add('hidden');
    step2.classList.add('hidden');
    step3.classList.add('hidden');
    step4.classList.add('hidden');

    // 4. Clear Inputs
    const searchInput = document.getElementById('search-input');
    if (searchInput) searchInput.value = '';

    const fileInput = document.getElementById('file-upload');
    if (fileInput) fileInput.value = '';
    updateFileStatus(); // Update file text to 0

    // Clear Step 4 Fields (Avoid stale data if switching between step 4 sessions)
    const fTitle = document.getElementById('final-info-title');
    if (fTitle) fTitle.innerText = 'Cargando título...';

    const fDuration = document.getElementById('final-info-duration');
    if (fDuration) fDuration.innerText = '--';

    const fThematic = document.getElementById('final-info-thematic');
    if (fThematic) fThematic.innerText = '--';

    const fKeywords = document.getElementById('final-info-keywords');
    if (fKeywords) fKeywords.innerHTML = '';

    const fExecutor = document.getElementById('final-executor-name');
    if (fExecutor) fExecutor.innerText = '';
    const fExecutorImg = document.getElementById('final-executor-img');
    if (fExecutorImg) fExecutorImg.src = '';

    const fCoexecList = document.getElementById('final-coexecutors-list');
    if (fCoexecList) fCoexecList.innerHTML = '';
    const fCollabList = document.getElementById('final-collaborators-list');
    if (fCollabList) fCollabList.innerHTML = '';
    const fNoAlliances = document.getElementById('final-no-alliances');
    if (fNoAlliances) fNoAlliances.classList.remove('hidden');

    // Clear Step 3 (Schema) Fields
    const sTitle = document.getElementById('general-title');
    if (sTitle) sTitle.innerText = 'Cargando título...';

    const sDuration = document.getElementById('general-duration');
    if (sDuration) sDuration.innerText = '--';

    const sThematic = document.getElementById('general-thematic');
    if (sThematic) sThematic.innerText = '--';

    const sKeywords = document.getElementById('general-keywords');
    if (sKeywords) sKeywords.innerHTML = '';

    const sContent = document.getElementById('schema-content');
    if (sContent) sContent.innerHTML = '';

    // 5. Reset Selection UI
    const { noSelectionState, selectionDetails, convocatoriasList } = getElements();
    if (noSelectionState) noSelectionState.classList.remove('hidden');
    if (selectionDetails) selectionDetails.classList.add('hidden');

    // 6. Hide Modals (if open) and clear modal-specific state
    const researchModal = document.getElementById('research-loading-modal');
    if (researchModal) researchModal.classList.add('hidden');

    const baseHistoryGrid = document.getElementById('base-history-grid');
    if (baseHistoryGrid) baseHistoryGrid.innerHTML = '';

    // Reset Step 3/Modal internal state
    import('./steps/step3.js').then(({ resetStep3State }) => {
        resetStep3State();
    });

    // 7. Restore Poster Container Structure (if it was wiped by the history slider)
    const posterCard = document.getElementById('final-poster-card');
    if (posterCard) {
        // ALWAYS restore to avoid stale slider from previous session if it wasn't caught
        console.log("🛠️ Forcefully restoring Poster Card DOM structure...");

        // Restore classes
        posterCard.className = "bg-gray-100 rounded-[2rem] border-2 border-dashed border-gray-200 flex items-center justify-center relative group overflow-hidden shadow-inner transition-all duration-500 min-h-[500px]";

        // Restore inner HTML
        posterCard.innerHTML = `
            <!-- Imagen del Poster -->
            <img id="final-poster-img"
                class="hidden w-full h-full object-contain rounded-lg shadow-2xl transition-transform duration-500 hover:scale-[1.02]"
                alt="Poster Científico">

            <!-- Placeholder por defecto -->
            <div id="final-poster-placeholder" class="text-center text-gray-400 p-8">
                <div class="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i class="ph ph-image text-4xl"></i>
                </div>
                <p class="font-medium">El poster se visualizará aquí una vez generado</p>
            </div>

            <!-- Botón de ampliar (overlay) -->
            <div id="poster-overlay"
                class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center hidden">
                <button id="btn-view-poster"
                    class="bg-white text-gray-900 px-6 py-3 rounded-full font-bold shadow-lg transform hover:scale-105 transition flex items-center gap-2">
                    <i class="ph-fill ph-arrows-out-simple"></i>
                    Ver en Alta Resolución
                </button>
            </div>
        `;
    }

    // 8. Refresh History and List
    loadHistory();
    import('./search.js').then(search => search.filterOptions());
}
