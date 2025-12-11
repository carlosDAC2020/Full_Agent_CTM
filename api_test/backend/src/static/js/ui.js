/**
 * ui.js
 * Manejo de renderizado de tarjetas y lógica del Modal.
 */

// Renderiza las tarjetas de ideas en el Paso 2
function renderIdeas(ideas) {
    const container = document.getElementById('ideas-container');
    if (!container) return; // Protección por si no existe el elemento
    
    container.innerHTML = '';
    
    ideas.forEach((idea, index) => {
        const card = document.createElement('div');
        card.className = 'col-md-6 mb-4';
        
        // CORRECCIÓN: Quitamos el onclick del div padre para evitar conflictos 
        // y lo dejamos solo en el botón, o manejamos mejor el evento.
        // Aquí lo dejamos en el botón para ser más explícitos.
        card.innerHTML = `
            <div class="card h-100 card-cotecmar idea-card border-0 shadow-sm">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title text-cotecmar fw-bold mb-3">${idea.idea_title}</h5>
                    <p class="card-text text-muted small flex-grow-1">
                        ${idea.idea_description ? idea.idea_description.substring(0, 120) + '...' : 'Sin descripción'}
                    </p>
                    <button class="btn btn-outline-primary w-100 mt-3" onclick="openEditModal(${index})">
                        Seleccionar y Editar
                    </button>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

// Abrir Modal con datos pre-cargados
function openEditModal(index) {
    // CORRECCIÓN 1: Usar 'appState' en lugar de 'state'
    if (!appState.ideas || !appState.ideas[index]) return;

    const idea = appState.ideas[index];
    appState.selectedIdea = idea; // Guardar referencia en el estado global
    
    document.getElementById('modalIdeaTitle').value = idea.idea_title || "";
    document.getElementById('modalIdeaDesc').value = idea.idea_description || "";
    
    // Renderizar objetivos
    const objContainer = document.getElementById('modalIdeaObjectives');
    objContainer.innerHTML = '';
    
    // CORRECCIÓN 3: Validar que existan objetivos
    if (idea.idea_objectives && Array.isArray(idea.idea_objectives)) {
        idea.idea_objectives.forEach(obj => {
            addObjectiveInput(obj); // Usamos la función auxiliar
        });
    } else {
        // Si no hay, agregamos uno vacío por defecto
        addObjectiveInput("");
    }
    
    // CORRECCIÓN 4: Manejo seguro de la instancia de Bootstrap
    const modalEl = document.getElementById('editIdeaModal');
    let modal = bootstrap.Modal.getInstance(modalEl);
    if (!modal) {
        modal = new bootstrap.Modal(modalEl);
    }
    modal.show();
}

// CORRECCIÓN 2: AGREGAR ESTA FUNCIÓN FALTANTE
// Función auxiliar para agregar inputs de objetivos al modal
function addObjectiveInput(value = "") {
    const container = document.getElementById('modalIdeaObjectives');
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

// Capturar datos del modal y confirmar
async function confirmIdeaSelection() {
    // 1. Recolectar datos del formulario
    const newTitle = document.getElementById('modalIdeaTitle').value;
    const newDesc = document.getElementById('modalIdeaDesc').value;
    
    const newObjs = [];
    document.querySelectorAll('.obj-input').forEach(input => {
        if(input.value.trim()) newObjs.push(input.value.trim());
    });
    
    // 2. Crear objeto limpio
    const finalIdea = {
        idea_title: newTitle,
        idea_description: newDesc,
        idea_objectives: newObjs
    };
    
    // 3. Cerrar modal
    const modalEl = document.getElementById('editIdeaModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) modal.hide();
    
    // 4. Enviar a API (Llama a la función definida en main.js)
    if (typeof submitSelectedIdea === 'function') {
        await submitSelectedIdea(finalIdea);
    } else {
        console.error("Error: submitSelectedIdea no está definido en main.js");
    }
}