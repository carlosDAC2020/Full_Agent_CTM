import { store } from '../data/store.js';
import { getSessionHistory } from '../api/agent.js';
import { getElements, updateStepper } from './common.js';
import { renderStep1Result } from './steps/step1.js';
import { renderIdeas } from './steps/step2.js';
import { renderSchema } from './steps/step3.js';
import { renderFinalResult } from './steps/step4.js';
import { loadHistory } from './sidebar.js';
import { resetInterface } from './wizard.js'; // Import reset to clean state first

// RESTORE SESSION LOGIC
export async function restoreSession(sessionId) {
    const { initialView, resultsView, globalStepper, loader, loaderText, step1, step2, step3, step4 } = getElements();

    // 0. Clean old state before loading new one avoids mixing data
    resetInterface();

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

    // Ensure all steps hidden initially
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

        // ---------------------------------------------------------
        // 2. SYSTEMATIC RENDER OF ALL AVAILABLE HISTORY
        // Use latestState for shared collections like call_info or docs if available
        const latestState = historyData.latest_data;

        // A. Render Step 1 (Ingest) - Always expected
        if (stepsMap['ingest'] || latestState) {
            renderStep1Result(latestState || stepsMap['ingest']);
        }

        // B. Render Step 2 (Ideas)
        if (stepsMap['proposal_ideas'] || latestState) {
            let data = stepsMap['proposal_ideas'] || latestState;
            // Handle potential double-serialization or string format
            if (typeof data === 'string') {
                try { data = JSON.parse(data); } catch (e) { }
            }
            if (data && data.proposal_ideas) { // Check if ideas exist in the state
                renderIdeas(data);
            }
        }

        // C. Render Step 3 (Schema)
        if (stepsMap['project_idea'] || latestState) {
            let data = stepsMap['project_idea'] || latestState;
            if (typeof data === 'string') {
                try { data = JSON.parse(data); } catch (e) { }
            }

            if (data && data.selected_idea) {
                const ideaData = data.selected_idea;
                store.currentSelectedIdea = {
                    title: ideaData.idea_title || ideaData.title,
                    desc: ideaData.idea_description || ideaData.desc,
                    objectives: ideaData.idea_objectives || ideaData.objectives || []
                };
            }
            if (data && data.initial_schema) { // Corrected key: initial_schema
                renderSchema(data);
            }
        }

        // D. Render Step 4 (Final)
        const finalData = stepsMap['generate_project'] || stepsMap['generate_proyect'] || stepsMap['report'] || latestState;
        if (finalData) {
            let data = finalData;
            if (typeof data === 'string') {
                try { data = JSON.parse(data); } catch (e) { }
            }
            // Corrected check: look into docs_paths for the PDF
            if (data && data.docs_paths && data.docs_paths.proyect_proposal_pdf) {
                renderFinalResult(data);
            }
        }

        // ---------------------------------------------------------
        // 3. DETERMINE VISIBLE STEP BASED ON LAST ACTIVITY
        // ---------------------------------------------------------

        let targetStep = 1;

        if (!lastStep || lastStep === 'ingest') {
            targetStep = 1;
        }
        else if (lastStep === 'proposal_ideas') {
            targetStep = 2;
        }
        else if (lastStep === 'project_idea') {
            targetStep = 3;
        }
        else if (lastStep === 'generate_project' || lastStep === 'generate_proyect' || lastStep === 'final' || lastStep === 'report') {
            targetStep = 4;
        }

        // Activate the determined step
        const stepElements = [null, step1, step2, step3, step4]; // 1-indexed
        if (stepElements[targetStep]) {
            stepElements[targetStep].classList.remove('hidden');
        }

        updateStepper(targetStep);

        // --- NEW: Restore Modal if Researching ---
        if (historyData.status === 'researching' && historyData.current_task_id) {
            console.log("🔄 Reanudando monitoreo de investigación...");
            const researchModal = document.getElementById('research-loading-modal');
            const statusText = document.getElementById('research-status-text');
            const { pollTask } = await import('../api/tasks.js');

            researchModal.classList.remove('hidden');
            statusText.innerText = "Reconectando con el agente...";

            pollTask(
                historyData.current_task_id,
                (msg) => { statusText.innerText = msg || "Analizando..."; },
                (result) => {
                    renderStep1Result(result.data);
                    researchModal.classList.add('hidden');
                },
                (err) => {
                    statusText.innerText = "Error recuperado: " + err;
                    setTimeout(() => researchModal.classList.add('hidden'), 3000);
                }
            );
        }

    } catch (err) {
        console.error(err);
        loader.classList.add('hidden');
        alert("Error restaurando sesión: " + err.message);
        // location.reload(); // Optional: might be too aggressive if it's just a minor glitch
    }
}
