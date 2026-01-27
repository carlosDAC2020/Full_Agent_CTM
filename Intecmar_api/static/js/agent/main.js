// Main Entry Point
import { loadHistory, toggleSidebar } from './ui/sidebar.js';
import { initInitialView, filterOptions, selectOption, setStatusFilter, setCategoryFilter } from './ui/search.js';
import {
    startAnalysis,
    startResearch,
    appendDocs,
    updateFileStatus,
    goToStep2,
    cancelEdit,
    confirmIdea,
    generateFinal,
    restoreSession,
    resetInterface,
    openIdeaConfigModal,
    closeIdeaConfigModal,
    confirmIdeaGeneration
} from './ui/wizard.js';

document.addEventListener('DOMContentLoaded', () => {
    // Componentes ya cargados por auth.js (si existe en el layout)

    // Inicializar componentes
    loadHistory();
    initInitialView();

    // Exponer funciones globales necesarias para onclicks en el HTML
    window.toggleSidebar = toggleSidebar;
    window.resetInterface = resetInterface;

    window.filterOptions = filterOptions;
    window.selectOption = selectOption;
    window.setStatusFilter = setStatusFilter;
    window.setCategoryFilter = setCategoryFilter;

    window.startAnalysis = startAnalysis;
    window.startResearch = startResearch;
    window.appendDocs = appendDocs;
    window.updateFileStatus = updateFileStatus;
    window.goToStep2 = goToStep2;
    window.cancelEdit = cancelEdit;
    window.confirmIdea = confirmIdea;
    window.generateFinal = generateFinal;
    window.restoreSession = restoreSession; // Exponer para debug o usos globales

    window.openIdeaConfigModal = openIdeaConfigModal;
    window.closeIdeaConfigModal = closeIdeaConfigModal;
    window.confirmIdeaGeneration = confirmIdeaGeneration;

    // Navigation function to Magazine app
    window.navigateToMagazineHome = function () {
        window.location.href = '/magazine';
    };
});
