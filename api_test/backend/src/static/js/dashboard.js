let currentSessionId = null;
let currentTaskId = null;
let currentIdeas = []; // Para guardar las ideas temporalmente
let selectedIdeaObj = null;

// Función genérica para polling
async function pollTask(taskId, onComplete) {
    document.getElementById('global-spinner').style.display = 'inline-block';
    const statusText = document.getElementById('status-text');
    
    const interval = setInterval(async () => {
        try {
            const res = await fetch(`/api/tasks/${taskId}`);
            const data = await res.json();
            
            statusText.innerText = `Procesando... Estado: ${data.status}`;

            if (data.status === 'SUCCESS') {
                clearInterval(interval);
                document.getElementById('global-spinner').style.display = 'none';
                statusText.innerText = 'Completado';
                
                // data.result contiene lo que devuelve tu función de Celery task_process_agent_step
                // Recuerda que en Python devolvimos {"status": "completed", "data": "json_string..."}
                onComplete(data.result);
            } else if (data.status === 'FAILURE') {
                clearInterval(interval);
                alert("Error en el procesamiento del agente");
                document.getElementById('global-spinner').style.display = 'none';
            }
        } catch (e) {
            console.error(e);
        }
    }, 2000); // Consultar cada 2 segundos
}

// PASO 1: INGESTA
async function startIngest() {
    const text = document.getElementById('inputText').value;
    if(!text) return alert("Ingresa un texto");

    document.getElementById('status-bar').style.display = 'block';
    
    const res = await fetch('/api/agent/ingest', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text: text})
    });
    const data = await res.json();
    currentSessionId = data.session_id;

    pollTask(data.task_id, (result) => {
        // Parsear el estado devuelto (que viene como JSON string dentro de result.data)
        const agentState = JSON.parse(result.data); 
        const callInfo = agentState.call_info;

        let html = `<strong>Título:</strong> ${callInfo.title}<br>`;
        html += `<strong>Objetivo:</strong> ${callInfo.objective.substring(0, 150)}...`;
        document.getElementById('ingest-results').innerHTML = html;
        
        document.getElementById('step-2').classList.add('active-step');
    });
}

// PASO 2: GENERAR IDEAS
async function generateIdeas() {
    const res = await fetch('/api/agent/generate-ideas', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({session_id: currentSessionId})
    });
    const data = await res.json();

    pollTask(data.task_id, (result) => {
        const agentState = JSON.parse(result.data);
        const ideas = agentState.proposal_ideas.ideas;
        currentIdeas = ideas; // Guardar en memoria global JS

        const listDiv = document.getElementById('ideas-list');
        listDiv.innerHTML = '';
        
        ideas.forEach((idea, index) => {
            const item = document.createElement('button');
            item.className = 'list-group-item list-group-item-action';
            item.innerHTML = `
                <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">${idea.idea_title}</h5>
                </div>
                <p class="mb-1">${idea.idea_description}</p>
            `;
            item.onclick = () => {
                // Marcar visualmente
                document.querySelectorAll('.list-group-item').forEach(i => i.classList.remove('active'));
                item.classList.add('active');
                selectedIdeaObj = idea; // Guardar selección
            };
            listDiv.appendChild(item);
        });

        document.getElementById('step-3').classList.add('active-step');
    });
}

// PASO 3: SELECCIONAR IDEA
async function selectIdea() {
    if (!selectedIdeaObj) return alert("Selecciona una idea de la lista");

    const res = await fetch('/api/agent/select-idea', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            session_id: currentSessionId,
            selected_idea: selectedIdeaObj
        })
    });
    const data = await res.json();

    pollTask(data.task_id, (result) => {
        const agentState = JSON.parse(result.data);
        
        // Mostrar preview pequeño
        if(agentState.report_components && agentState.report_components.general_info) {
             document.getElementById('schema-preview').innerText = 
                "Proyecto: " + agentState.report_components.general_info.project_title;
        }
        
        document.getElementById('step-4').classList.add('active-step');
    });
}

// PASO 4: FINALIZAR
async function finalizeProject() {
    const res = await fetch('/api/agent/finalize', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({session_id: currentSessionId})
    });
    const data = await res.json();

    pollTask(data.task_id, (result) => {
        const agentState = JSON.parse(result.data);
        const docs = agentState.docs_paths;
        
        const list = document.getElementById('final-docs-list');
        // Aquí deberías poner links reales a un endpoint de descarga si usas MinIO o archivos locales
        // Por ahora mostramos las rutas
        if (docs) {
             list.innerHTML = `
                <li class="list-group-item">📄 PDF Propuesta: ${docs.proyect_proposal_pdf}</li>
                <li class="list-group-item">📊 PDF Presentación: ${docs.presentation_oath_pdf}</li>
                <li class="list-group-item">🖼️ Poster: ${docs.poster_image_path}</li>
             `;
        }
        document.getElementById('step-5').classList.add('active-step');
    });
}