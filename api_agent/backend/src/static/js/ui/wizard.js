// Wizard Orchestrator
// Centralizes imports/exports for the application

import { store } from '../data/store.js';
import { getElements, updateFileStatus } from './common.js';
import { loadHistory } from './sidebar.js';

// Common Utilities
export { updateFileStatus, navigateToStep } from './common.js';

// Step Logic
export { startAnalysis } from './steps/step1.js';
export { goToStep2, cancelEdit } from './steps/step2.js';
export { confirmIdea } from './steps/step3.js';
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

    // 5. Refresh History (removes active highlight)
    loadHistory();
}
