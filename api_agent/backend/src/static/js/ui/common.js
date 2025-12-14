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

        const circle = dot.querySelector('div');
        const label = dot.querySelector('span');

        // Reset click
        dot.onclick = null;

        if (i === currentStep) {
            // Active Step
            dot.className = "flex items-center gap-2 px-4 py-1.5 rounded-full bg-cotecmar-dark text-white shadow-md transform scale-105 transition-all duration-300 cursor-default";
            circle.className = "w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold border-2 border-white/20 bg-white/10";
            label.className = "text-xs font-bold whitespace-nowrap hidden md:block";
        } else if (i < currentStep || i <= store.maxReachedStep) {
            // Completed / Reached Step (Clickable)
            dot.className = "flex items-center gap-2 px-4 py-1.5 rounded-full hover:bg-gray-100 transition-all duration-300 cursor-pointer text-gray-600 group";
            circle.className = "w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold border-2 border-cotecmar-mid text-cotecmar-mid bg-white group-hover:bg-cotecmar-mid group-hover:text-white transition-colors";
            label.className = "text-xs font-bold whitespace-nowrap hidden md:block group-hover:text-cotecmar-mid";

            dot.onclick = () => navigateToStep(i);
        } else {
            // Future Step (Disabled)
            dot.className = "flex items-center gap-2 px-4 py-1.5 rounded-full transition-all duration-300 cursor-not-allowed text-gray-300 opacity-60";
            circle.className = "w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold border-2 border-gray-200 bg-gray-50";
            label.className = "text-xs font-bold whitespace-nowrap hidden md:block";
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
