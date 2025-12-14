import { store } from '../data/store.js';
import { getSessionHistory } from '../api/agent.js';
import { getElements, updateStepper } from './common.js';
import { renderStep1Result } from './steps/step1.js';
import { renderIdeas } from './steps/step2.js';
import { renderSchema } from './steps/step3.js';
import { renderFinalResult } from './steps/step4.js';
import { loadHistory } from './sidebar.js'; // Helper for sidebar updates

// RESTORE SESSION LOGIC
export async function restoreSession(sessionId) {
    const { initialView, resultsView, globalStepper, loader, loaderText, step1, step2, step3, step4 } = getElements();
    store.sessionId = sessionId;

    // Highlight active session
    loadHistory(sessionId);

    // Switch Views
    initialView.classList.add('hidden');
    resultsView.classList.remove('hidden');
    resultsView.classList.add('flex');
    globalStepper.classList.remove('hidden');

    loader.classList.remove('hidden');
    loaderText.innerText = "Restaurando sesión...";

    // Reset Steps
    step1.classList.add('hidden');
    step2.classList.add('hidden');
    step3.classList.add('hidden');
    step4.classList.add('hidden');

    try {
        const historyData = await getSessionHistory(sessionId); // returns { steps_data: {...}, status, last_step }
        const stepsMap = historyData.steps_data || {};
        const lastStep = historyData.last_step;

        loader.classList.add('hidden');

        // 1. Calculate and update Max Reached Step
        const STEP_MAPPING = {
            'ingest': 1,
            'proposal_ideas': 2,
            'project_idea': 3,
            'generate_project': 4,
            'generate_proyect': 4,
            'final': 4,
            'report': 4
        };
        const maxStep = STEP_MAPPING[lastStep] || 1;
        store.maxReachedStep = maxStep;

        // 2. Restore Ingest Data (Always expected if session exists)
        if (stepsMap['ingest']) {
            renderStep1Result(stepsMap['ingest']);

            // Extract title for the header label
            let ingestData = typeof stepsMap['ingest'] === 'string' ? JSON.parse(stepsMap['ingest']) : stepsMap['ingest'];
            if (ingestData.call_info && ingestData.call_info.title) {
                document.getElementById('selected-label').innerText = ingestData.call_info.title;
            }
        }

        // 2. Logic based on last executed step
        if (!lastStep || lastStep === 'ingest') {
            // Stay on Step 1
            step1.classList.remove('hidden');
        }
        else if (lastStep === 'proposal_ideas') {
            // Step 1 done, move to Step 2
            step1.classList.add('hidden');
            step2.classList.remove('hidden');
            updateStepper(2);
            // Verify if we have ideas data to render
            if (stepsMap['proposal_ideas']) {
                let data = stepsMap['proposal_ideas'];
                if (typeof data === 'string') data = JSON.parse(data);
                renderIdeas(data);
            }
        }
        else if (lastStep === 'project_idea') {
            // Step 2 done, move to Step 3 (Schema)
            step1.classList.add('hidden');
            step2.classList.add('hidden');
            step3.classList.remove('hidden');
            updateStepper(3);

            // Restore selected idea to store (needed for renderSchema)
            if (stepsMap['project_idea']) {
                let data = stepsMap['project_idea'];
                if (typeof data === 'string') data = JSON.parse(data);

                if (data.selected_idea) {
                    const ideaData = data.selected_idea;
                    store.currentSelectedIdea = {
                        title: ideaData.idea_title,
                        desc: ideaData.idea_description,
                        objectives: ideaData.idea_objectives || []
                    };
                }

                renderSchema(data);
            }
        }
        else if (lastStep === 'generate_project' || lastStep === 'generate_proyect' || lastStep === 'final') {
            // Step 3 done, move to Step 4
            step1.classList.add('hidden');
            step2.classList.add('hidden');
            step3.classList.add('hidden');
            step4.classList.remove('hidden');
            updateStepper(4);

            // Renderizar resultados finales
            const finalData = stepsMap['generate_project'] || stepsMap['generate_proyect'] || stepsMap['report'];

            if (finalData) {
                const data = typeof finalData === 'string' ? JSON.parse(finalData) : finalData;
                renderFinalResult(data);
            }
        }

    } catch (err) {
        loader.classList.add('hidden');
        alert("Error restaurando sesión: " + err.message);
        location.reload();
    }
}
