/**
 * ui.js
 * Manejo de renderizado de tarjetas de ideas y lógica del Modal de edición.
 */

// ==========================================
// RENDERIZADO DE IDEAS
// ==========================================

/**
 * Renderiza las tarjetas de ideas en el panel de Ideas (Paso 2)
 * @param {Array} ideas - Lista de ideas del agente
 */
function renderIdeas(ideas) {
    const container = document.getElementById('ideas-container');
    if (!container) return;

    container.innerHTML = '';

    if (!ideas || ideas.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="alert alert-info text-center">
                    <i class="bi bi-info-circle me-2"></i>
                    No se generaron ideas. Intenta con una convocatoria más detallada.
                </div>
            </div>`;
        return;
    }

    ideas.forEach((idea, index) => {
        const card = document.createElement('div');
        card.className = 'col-md-6 col-lg-4 mb-4';

        // Truncar descripción para preview
        const descPreview = idea.idea_description
            ? (idea.idea_description.length > 120
                ? idea.idea_description.substring(0, 120) + '...'
                : idea.idea_description)
            : 'Sin descripción disponible';

        card.innerHTML = `
            <div class="card h-100 idea-card border-0 shadow-sm">
                <div class="card-body d-flex flex-column p-4">
                    <div class="d-flex align-items-start mb-3">
                        <span class="badge bg-primary bg-opacity-10 text-primary me-2">#${index + 1}</span>
                    </div>
                    <h5 class="card-title text-cotecmar fw-bold mb-3">${idea.idea_title || 'Idea sin título'}</h5>
                    <p class="card-text text-muted small flex-grow-1">${descPreview}</p>
                    <button class="btn btn-outline-primary w-100 mt-3" onclick="openEditModal(${index})">
                        <i class="bi bi-pencil me-1"></i> Seleccionar y Editar
                    </button>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

// ==========================================
// MODAL DE EDICIÓN
// ==========================================

/**
 * Abre el modal de edición con los datos de la idea seleccionada
 * @param {number} index - Índice de la idea en appState.ideas
 */
function openEditModal(index) {
    // Verificar que existe la idea
    if (!appState.ideas || !appState.ideas[index]) {
        console.error('Idea no encontrada en el índice:', index);
        return;
    }

    const idea = appState.ideas[index];
    appState.selectedIdea = idea;

    // Llenar campos del formulario
    const titleInput = document.getElementById('modalIdeaTitle');
    const descInput = document.getElementById('modalIdeaDesc');

    if (titleInput) titleInput.value = idea.idea_title || '';
    if (descInput) descInput.value = idea.idea_description || '';

    // Renderizar objetivos
    const objContainer = document.getElementById('modalIdeaObjectives');
    if (objContainer) {
        objContainer.innerHTML = '';

        if (idea.idea_objectives && Array.isArray(idea.idea_objectives) && idea.idea_objectives.length > 0) {
            idea.idea_objectives.forEach(obj => {
                addObjectiveInput(obj);
            });
        } else {
            // Si no hay objetivos, agregar uno vacío
            addObjectiveInput('');
        }
    }

    // Mostrar modal
    const modalEl = document.getElementById('editIdeaModal');
    if (modalEl) {
        let modal = bootstrap.Modal.getInstance(modalEl);
        if (!modal) {
            modal = new bootstrap.Modal(modalEl);
        }
        modal.show();
    }
}

/**
 * Agrega un input de objetivo al modal
 * @param {string} value - Valor inicial del objetivo
 */
function addObjectiveInput(value = '') {
    const container = document.getElementById('modalIdeaObjectives');
    if (!container) return;

    const div = document.createElement('div');
    div.className = 'input-group mb-2';

    div.innerHTML = `
        <span class="input-group-text input-group-text-icon bg-white border-end-0">
            <i class="bi bi-check-circle text-success"></i>
        </span>
        <textarea class="form-control form-control-modern obj-input" 
                  rows="2" 
                  placeholder="Escriba un objetivo específico (SMART)...">${value}</textarea>
        <button class="btn btn-outline-danger border-start-0" type="button" 
                onclick="this.parentElement.remove()" title="Eliminar objetivo">
            <i class="bi bi-trash"></i>
        </button>
    `;

    container.appendChild(div);
}

/**
 * Recoge los datos del modal y confirma la selección
 */
async function confirmIdeaSelection() {
    // 1. Recolectar datos del formulario
    const titleInput = document.getElementById('modalIdeaTitle');
    const descInput = document.getElementById('modalIdeaDesc');

    const newTitle = titleInput ? titleInput.value.trim() : '';
    const newDesc = descInput ? descInput.value.trim() : '';

    // Validar campos requeridos
    if (!newTitle) {
        alert('El título del proyecto es requerido.');
        return;
    }

    // Recolectar objetivos
    const newObjs = [];
    document.querySelectorAll('.obj-input').forEach(input => {
        const val = input.value.trim();
        if (val) newObjs.push(val);
    });

    if (newObjs.length === 0) {
        alert('Debe agregar al menos un objetivo.');
        return;
    }

    // 2. Crear objeto de idea final
    const finalIdea = {
        idea_title: newTitle,
        idea_description: newDesc,
        idea_objectives: newObjs
    };

    // 3. Cerrar modal
    const modalEl = document.getElementById('editIdeaModal');
    if (modalEl) {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
    }

    // 3.1 Actualizar visualmente la tarjeta de la idea en el listado
    if (appState.selectedIdea && appState.ideas) {
        // Encontrar índice de la idea seleccionada
        const index = appState.ideas.indexOf(appState.selectedIdea);
        if (index !== -1) {
            appState.ideas[index] = finalIdea;
            // Renderizar de nuevo para reflejar cambios
            renderIdeas(appState.ideas);
        }
    }
    appState.selectedIdea = finalIdea;

    // 4. Enviar a API (función definida en main.js)
    if (typeof submitSelectedIdea === 'function') {
        await submitSelectedIdea(finalIdea);
    } else {
        console.error('Error: submitSelectedIdea no está definida en main.js');
    }
}

// ==========================================
// ESTILOS ADICIONALES PARA MODAL
// ==========================================

// Inyectar estilos CSS adicionales si no existen
(function () {
    if (document.getElementById('ui-js-styles')) return;

    const style = document.createElement('style');
    style.id = 'ui-js-styles';
    style.textContent = `
        /* Modal Header Cotecmar */
        .modal-header-cotecmar {
            background: linear-gradient(135deg, var(--cotecmar-navy, #002D62) 0%, var(--cotecmar-blue, #005691) 100%);
            color: white;
            border: none;
        }
        
        /* Form Controls Modernos */
        .form-control-modern {
            border-radius: 8px;
            border: 1px solid #e1e5eb;
            transition: all 0.2s;
        }
        
        .form-control-modern:focus {
            border-color: var(--cotecmar-blue, #005691);
            box-shadow: 0 0 0 3px rgba(0, 86, 145, 0.1);
        }
        
        /* Input Group Icon */
        .input-group-text-icon {
            background: white;
            border-right: none;
            color: var(--cotecmar-navy, #002D62);
        }
        
        /* SMART Badge */
        .smart-badge {
            font-size: 0.65rem;
            background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%);
            color: #333;
            padding: 2px 8px;
            border-radius: 12px;
            margin-left: 8px;
            font-weight: 600;
            cursor: help;
        }
        
        /* Objectives Container */
        .objectives-container {
            max-height: 300px;
            overflow-y: auto;
            padding-right: 5px;
        }
        
        .objectives-container::-webkit-scrollbar {
            width: 4px;
        }
        
        .objectives-container::-webkit-scrollbar-thumb {
            background: #ccc;
            border-radius: 2px;
        }
    `;
    document.head.appendChild(style);
})();
