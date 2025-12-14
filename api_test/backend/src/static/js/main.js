// Main Entry Point
import { loadHistory, toggleSidebar } from './ui/sidebar.js';
import { openDropdown, filterOptions, selectOption } from './ui/search.js';
import {
    startAnalysis,
    updateFileStatus,
    goToStep2,
    cancelEdit,
    confirmIdea,
    generateFinal,
    confirmIdea,
    generateFinal,
    restoreSession,
    resetInterface
} from './ui/wizard.js';

document.addEventListener('DOMContentLoaded', () => {
    // Inicializar componentes
    loadHistory();

    // Exponer funciones globales necesarias para onclicks en el HTML
    window.toggleSidebar = toggleSidebar;
    window.resetInterface = resetInterface;

    window.openDropdown = openDropdown;
    window.filterOptions = filterOptions;
    window.selectOption = selectOption;

    window.startAnalysis = startAnalysis;
    window.updateFileStatus = updateFileStatus;
    window.goToStep2 = goToStep2;
    window.cancelEdit = cancelEdit;
    window.confirmIdea = confirmIdea;
    window.generateFinal = generateFinal;
    window.restoreSession = restoreSession; // Exponer para debug o usos globales
});
