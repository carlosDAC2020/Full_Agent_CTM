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
export { confirmIdea, openConfigModal, closeConfigModal, saveConfigAndGenerate } from './steps/step3.js';
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

    // 5. Reset Selection UI
    const { noSelectionState, selectionDetails, convocatoriasList } = getElements();
    if (noSelectionState) noSelectionState.classList.remove('hidden');
    if (selectionDetails) selectionDetails.classList.add('hidden');

    // 6. Hide Modals (if open)
    const researchModal = document.getElementById('research-loading-modal');
    if (researchModal) researchModal.classList.add('hidden');

    // 7. Restore Poster Container Structure (if it was wiped by the history slider)
    const posterImg = document.getElementById('final-poster-img');
    if (!posterImg) {
        // Find the container (it had classes bg-gray-100, border-dashed, etc.)
        // We can find it by looking for the one that usually contains the placeholder if it was there, 
        // but since it's wiped, we look for the one inside #step-4-final that's a sibling of the info card.
        const step4 = document.getElementById('step-4-final');
        if (step4) {
            const posterCard = step4.querySelector('.border-dashed');
            if (posterCard) {
                console.log("🛠️ Restoring Poster Card DOM structure...");
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
        }
    }

    // 8. Refresh History and List
    loadHistory();
    import('./search.js').then(search => search.filterOptions());
}
