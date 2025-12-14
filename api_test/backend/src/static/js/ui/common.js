// DOM Elements
export function getElements() {
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

import { store } from '../data/store.js';

export function updateFileStatus() {
    const input = document.getElementById('file-upload');
    const dropZone = document.getElementById('drop-zone');
    if (input && input.files.length > 0) {
        dropZone.classList.add('border-green-400', 'bg-green-50/50');
        document.getElementById('upload-text-main').innerText = input.files.length + " Archivo(s)";
    }
}

export function updateStepper(currentStep) {
    if (currentStep > store.maxReachedStep) {
        store.maxReachedStep = currentStep;
    }

    for (let i = 1; i <= 4; i++) {
        const dot = document.getElementById(`step-dot-${i}`);
        if (!dot) continue;

        // Reset classes
        dot.className = "cursor-default text-gray-300 transition-colors duration-200 select-none"; // Base style
        dot.onclick = null;

        if (i === currentStep) {
            // Active Step
            dot.className = "text-cotecmar-mid font-bold underline decoration-2 underline-offset-4 cursor-default";
        } else if (i < currentStep || i <= store.maxReachedStep) {
            // Completed / Reached Step (Clickable)
            dot.className = "text-gray-800 hover:text-cotecmar-mid cursor-pointer font-medium";
            dot.onclick = () => navigateToStep(i);
        } else {
            // Future Step (Disabled)
            dot.className = "text-gray-300 cursor-not-allowed";
        }
    }
}

export function navigateToStep(stepNumber) {
    if (stepNumber > store.maxReachedStep) return;

    const { step1, step2, step3, step4 } = getElements();

    // Hide all steps
    step1.classList.add('hidden');
    step2.classList.add('hidden');
    step3.classList.add('hidden');
    step4.classList.add('hidden');

    // Show target step
    switch (stepNumber) {
        case 1: step1.classList.remove('hidden'); break;
        case 2: step2.classList.remove('hidden'); break;
        case 3: step3.classList.remove('hidden'); break;
        case 4: step4.classList.remove('hidden'); break;
    }

    updateStepper(stepNumber);
}
