// Main Entry Point
import { loadHistory, toggleSidebar } from './ui/sidebar.js';
import { initInitialView, filterOptions, selectOption, setStatusFilter, setCategoryFilter } from './ui/search.js';
import {
    startAnalysis,
    updateFileStatus,
    goToStep2,
    cancelEdit,
    confirmIdea,
    generateFinal,
    restoreSession,
    resetInterface
} from './ui/wizard.js';

// ===== NEW: Load User Info from /api/me =====
async function loadUserInfo() {
    // Helper to get login URL dynamically (Codespaces vs Localhost)
    const getLoginUrl = () => {
        const currentHost = window.location.hostname;
        const protocol = window.location.protocol;
        if (currentHost.includes('github.dev') || currentHost.includes('csb.app')) {
            // Codespaces: replace 8001 with 8000
            return protocol + '//' + currentHost.replace('-8001', '-8000') + '/frontend/login.html';
        } else {
            // Localhost
            return 'http://' + currentHost + ':8000/frontend/login.html';
        }
    };

    const token = localStorage.getItem('auth_token');
    if (!token) {
        window.location.href = getLoginUrl();
        return;
    }

    try {
        const res = await fetch('/api/me', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!res.ok) {
            throw new Error('Auth failed');
        }

        const user = await res.json();

        // Update sidebar user info
        const userNameEl = document.getElementById('user-name');
        const userRoleEl = document.getElementById('user-role');
        const userAvatarEl = document.getElementById('user-avatar');

        if (userNameEl) userNameEl.textContent = user.name || 'Usuario';
        if (userRoleEl) userRoleEl.textContent = user.role || 'Usuario';

        // Update avatar with initials
        if (userAvatarEl) {
            const initials = (user.name || 'U').split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
            userAvatarEl.textContent = initials;
        }

    } catch (err) {
        console.error('Failed to load user:', err);
        localStorage.removeItem('auth_token');
        window.location.href = getLoginUrl();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Load user info first
    loadUserInfo();

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
    window.updateFileStatus = updateFileStatus;
    window.goToStep2 = goToStep2;
    window.cancelEdit = cancelEdit;
    window.confirmIdea = confirmIdea;
    window.generateFinal = generateFinal;
    window.restoreSession = restoreSession; // Exponer para debug o usos globales

    // Navigation function to Magazine app
    window.navigateToMagazineHome = function () {
        const currentHost = window.location.hostname;
        const protocol = window.location.protocol;
        let targetUrl = '';
        const token = localStorage.getItem('auth_token');

        if (currentHost.includes('github.dev') || currentHost.includes('csb.app')) {
            // Codespaces/Cloud environment: replace port in subdomain
            targetUrl = protocol + '//' + currentHost.replace('-8001', '-8000') + '/frontend/index.html';
        } else {
            // Localhost environment
            targetUrl = 'http://' + currentHost + ':8000/frontend/index.html';
        }

        if (token) {
            targetUrl += `?token=${encodeURIComponent(token)}`;
        }

        window.location.href = targetUrl;
    };
});
