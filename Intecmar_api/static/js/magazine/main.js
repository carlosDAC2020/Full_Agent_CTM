// frontend/js/main.js
document.addEventListener('DOMContentLoaded', () => {
  const API_URL = document.body?.dataset?.api || window.location.origin;

  const generateBtn = document.getElementById('generateBtn');
  const loadingOverlay = document.getElementById('loading-overlay');
  const errorDiv = document.getElementById('error');
  const magazineContainer = document.getElementById('magazine-container');
  const successDiv = document.getElementById('successMessage');
  const statusEl = document.getElementById('status');
  const optionsBtn = document.getElementById('generateOptionsBtn');
  const optionsPanel = document.getElementById('optionsPanel');
  const closeOptions = document.getElementById('closeOptions');
  const saveOptions = document.getElementById('saveOptions');
  const otherTopic = document.getElementById('otherTopic');
  const pdfCartBtn = document.getElementById('pdfCartBtn');
  const pdfCartCount = document.getElementById('pdfCartCount');
  const pdfCartPanel = document.getElementById('pdfCartPanel');
  const closePdfCart = document.getElementById('closePdfCart');
  const pdfCartList = document.getElementById('pdfCartList');
  const generatePdfFromCartBtn = document.getElementById('generatePdfFromCart');
  const sourcesBtn = document.getElementById('sourcesBtn');
  const sourcesPanel = document.getElementById('sourcesPanel');
  const closeSources = document.getElementById('closeSources');
  const sourcesList = document.getElementById('sourcesList');
  const addSourceBtn = document.getElementById('addSourceBtn');
  const srcName = document.getElementById('srcName');
  const srcType = document.getElementById('srcType');
  const srcUrl = document.getElementById('srcUrl');
  const sourcesTabs = document.querySelectorAll('.sources-tabs .tab-btn');
  const sourcesViewTab = document.getElementById('sourcesViewTab');
  const sourcesAddTab = document.getElementById('sourcesAddTab');
  const magazineForm = document.getElementById('magazineForm');

  // Controles de oportunidades (filtros/paginación/selección)
  const btnActive = document.getElementById('btnActive');
  const btnClosed = document.getElementById('btnClosed');
  const btnRange = document.getElementById('btnRange');
  const startDateInput = document.getElementById('startDate');
  const endDateInput = document.getElementById('endDate');
  const applyRangeBtn = document.getElementById('applyRange');
  const selectAllVisibleCbx = document.getElementById('selectAllVisible');
  const pagePrevBtn = document.getElementById('pagePrev');
  const pageNextBtn = document.getElementById('pageNext');
  const pageInfoEl = document.getElementById('pageInfo');
  const categoryFiltersContainer = document.getElementById('category-filters');
  // Rediseñar botones de paginación con iconos (ya dentro del DOMContentLoaded)
  if (pagePrevBtn) {
    pagePrevBtn.innerHTML = '<i class="fa-solid fa-chevron-left"></i>';
    pagePrevBtn.setAttribute('aria-label', 'Anterior');
    pagePrevBtn.title = 'Anterior';
  }

  // =======================
  // Fuentes: Agregado desde pestaña IA
  // =======================
  async function addSelectedSources() {
    const aiResults = document.getElementById('sourcesAISearchResults');
    if (!aiResults) return;
    const checks = Array.from(aiResults.querySelectorAll('input.sr-cbx'));
    const toAdd = checks.filter(c => c.checked && c.getAttribute('data-exists') !== '1');
    if (!toAdd.length) return;
    showLoaderCustom(SOURCES_WORDS);
    try {
      for (const c of toAdd) {
        const name = c.getAttribute('data-title') || '';
        const url = c.getAttribute('data-url') || '';
        if (!url) continue;
        const res = await fetch(`${API_URL}/sources`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, url, type: '' })
        });
        if (!res.ok) {
          let msg = 'No se pudo agregar la fuente desde IA';
          try {
            const err = await res.json();
            if (err && err.detail) msg = String(err.detail);
          } catch { }
          throw new Error(msg);
        }
      }
      await refreshSources();
      // Aviso de cuántas se añadieron
      try { alert(`Se añadieron ${toAdd.length} fuente(s) al Dataset.`); } catch { }
      // Marcar en el estado local como agregadas y re-renderizar lista IA
      const addedSet = new Set(toAdd.map(c => c.getAttribute('data-url') || ''));
      if (Array.isArray(lastAISearchResults) && lastAISearchResults.length) {
        lastAISearchResults = lastAISearchResults.map(it => {
          if (addedSet.has(it.url || '')) {
            return { ...it, exists: true, added: true };
          }
          return it;
        });
        renderAISearchResults(lastAISearchResults);
      }
    } catch (e) {
      showError(e.message || String(e));
    } finally {
      hideLoaderRestore();
    }
  }
  // AI Search handlers
  const aiSearchBtn = document.getElementById('aiSearchBtn');
  const aiResults = document.getElementById('sourcesAISearchResults');
  const addSelectedSourcesAIBtn = document.getElementById('addSelectedSourcesAIBtn');
  let lastAISearchResults = [];
  function renderAISearchResults(items) {
    // reutiliza el renderer estándar
    // pero escribe en el contenedor AI
    if (!aiResults) return;
    // construimos HTML igual que renderSourcesSearchResults pero targeteando aiResults
    const list = Array.isArray(items) ? items : [];
    lastAISearchResults = list;
    const added = list.filter(x => x.added);
    const news = list.filter(x => !x.exists && !x.added);
    const olds = list.filter(x => x.exists && !x.added);
    const mkRow = (it, idx, disabled) => {
      const id = `srcai_${idx}_${Math.random().toString(36).slice(2)}`;
      return `
        <label class="source-result" style="display:flex;gap:10px;align-items:flex-start;margin:6px 0;">
          <input type="checkbox" class="sr-cbx" data-url="${escapeAttr(it.url || '')}" data-title="${escapeAttr(it.title || '')}" data-exists="${it.exists ? '1' : '0'}" id="${id}" ${(it.added || it.exists) ? 'checked' : ''} ${(it.added || disabled) ? 'disabled' : ''}>
          <div>
            <div><strong>${escapeHtml(it.title || it.url || '')}</strong></div>
            <small>${escapeHtml(it.url || '')}</small>
          </div>
        </label>`;
    };
    let html = '';
    if (added.length) {
      html += `<div class="sr-section"><div style="font-weight:600;margin:6px 0;color:#065f46;">Fuentes agregadas al Dataset</div>${added.map((it, i) => mkRow(it, i, true)).join('')}</div>`;
    }
    if (news.length) {
      html += `<div class="sr-section"><div style="font-weight:600;margin:6px 0;">Fuentes nuevas encontradas</div>${news.map((it, i) => mkRow(it, i, false)).join('')}</div>`;
    }
    if (olds.length) {
      html += `<div class="sr-section" style="margin-top:10px;">
        <div style="font-weight:600;margin:6px 0;color:#374151;">Ya se encuentran en el Dataset de Fuentes</div>
        ${olds.map((it, i) => mkRow(it, i + news.length + added.length, false)).join('')}
      </div>`;
    }
    if (!html) html = '<div style="color:#6b7280;">Sin resultados.</div>';
    aiResults.innerHTML = html;
  }
  if (aiSearchBtn) {
    aiSearchBtn.addEventListener('click', async () => {
      if (aiSearchBtn.disabled) return;
      aiSearchBtn.disabled = true;
      try {
        const tema = typeof buildTemaFromSavedOptions === 'function' ? buildTemaFromSavedOptions() : null;
        const taskId = await enqueueTask('fuentes', { tema });
        await new Promise((resolve, reject) => {
          taskWaiters.set(taskId, { resolve, reject });
          let stopped = false;
          const poll = async () => {
            if (stopped) return;
            try {
              const r = await fetch(`${API_URL}/api/tasks/id/${taskId}`);
              if (r.ok) {
                const js = await r.json();
                const st = (js.status || '').toLowerCase();
                if (st === 'succeeded') {
                  stopped = true;
                  if (taskWaiters.has(taskId)) taskWaiters.delete(taskId);
                  try { updateCard({ id: taskId, type: 'fuentes' }, 'succeeded', js.result); } catch { }
                  resolve(js);
                  return;
                }
                if (st === 'failed') {
                  stopped = true;
                  if (taskWaiters.has(taskId)) taskWaiters.delete(taskId);
                  try { updateCard({ id: taskId, type: 'fuentes' }, 'failed'); } catch { }
                  reject(new Error(js.error || 'Task failed'));
                  return;
                }
              }
            } catch { }
            setTimeout(poll, 2000);
          };
          setTimeout(poll, 2000);
          setTimeout(() => { if (taskWaiters.has(taskId)) { taskWaiters.delete(taskId); reject(new Error('Timeout AI search')); } }, 120000);
        });
        const res = await fetch(`${API_URL}/api/sources/ai_search`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ tema: tema || null }) });
        const data = res.ok ? await res.json() : { results: [] };
        renderAISearchResults(data.results || []);
      } catch (e) {
        try { const last = Array.from(taskCards.keys()).pop(); if (last) updateCard({ id: last, type: 'fuentes' }, 'failed'); } catch { }
        renderAISearchResults([]);
        showError(e.message || String(e));
      } finally {
        aiSearchBtn.disabled = false;
      }
    });
  }
  if (addSelectedSourcesAIBtn) {
    addSelectedSourcesAIBtn.addEventListener('click', async () => {
      if (addSelectedSourcesAIBtn.disabled) return;
      addSelectedSourcesAIBtn.disabled = true;
      try { await addSelectedSources(); }
      finally { addSelectedSourcesAIBtn.disabled = false; }
    });
  }
  if (pageNextBtn) {
    pageNextBtn.innerHTML = '<i class="fa-solid fa-chevron-right"></i>';
    pageNextBtn.setAttribute('aria-label', 'Siguiente');
    pageNextBtn.title = 'Siguiente';
  }
  const loaderOverlayEl = document.getElementById('loading-overlay');
  const loaderWordsContainer = document.querySelector('#loading-overlay .animated-words');
  let __currentUserId = null;
  async function getCurrentUserId() {
    if (typeof __currentUserId === 'number' && __currentUserId > 0) return __currentUserId;
    try {
      const r = await fetch(`${API_URL}/auth/me`);
      if (r.ok) {
        const me = await r.json();
        if (me && typeof me.id === 'number') { __currentUserId = me.id; return __currentUserId; }
      }
    } catch { }
    return null;
  }
  async function taskBelongsToMe(taskId) {
    try {
      const myId = await getCurrentUserId();
      if (!myId) return false;
      const r = await fetch(`${API_URL}/tasks/id/${taskId}`);
      if (!r.ok) return false;
      const js = await r.json();
      const uid = Number(js.user_id || 0);
      return uid === myId;
    } catch { return false; }
  }

  // =======================================================
  // Global defensive guards against unintended submits
  // =======================================================
  // 1) Block any submit event anywhere on the page (capturing)
  document.addEventListener('submit', (event) => {
    event.preventDefault();
    console.warn('Submit event prevented globally from target:', event.target);
  }, true);

  // 2) Block clicks on implicit submit buttons (type missing or type="submit")
  document.addEventListener('click', (event) => {
    const btn = event.target && event.target.closest && event.target.closest('button');
    if (!btn) return;
    const t = (btn.getAttribute('type') || '').toLowerCase();
    if (t === '' || t === 'submit') {
      event.preventDefault();
      console.warn('Implicit submit button click prevented:', btn.id || btn.className || btn.textContent);
    }
  }, true);

  // =======================
  // Ver Requisitos Flow
  // =======================
  const DEFAULT_WORDS = [
    'convocatorias', 'eventos', 'conferencias', 'summits', 'workshops', 'hackathons', 'convocatorias'
  ];
  const REQS_WORDS = [
    'requisitos', 'más info', 'requerimientos', 'normas', 'obligaciones', 'condiciones', 'requisitos'
  ];
  const SOURCES_WORDS = [
    'fuentes', 'bases de datos', 'organizaciones', 'sitios web', 'empresas', 'fuentes'
  ];

  function setLoaderWords(words) {
    if (!loaderWordsContainer) return;
    loaderWordsContainer.innerHTML = '';
    words.forEach(w => {
      const span = document.createElement('span');
      span.className = 'word';
      span.textContent = w;
      loaderWordsContainer.appendChild(span);
    });
  }
  function showLoaderCustom(words) {
    if (loaderOverlayEl) loaderOverlayEl.classList.remove('hidden');
    setLoaderWords(words || DEFAULT_WORDS);
  }
  function hideLoaderRestore() {
    if (loaderOverlayEl) loaderOverlayEl.classList.add('hidden');
    setLoaderWords(DEFAULT_WORDS);
  }

  async function handleVerRequisitos(itemId, cardEl) {
    try {
      // Encolar flujo en background
      let taskId;
      try {
        taskId = await enqueueTask('requisitos', { item_id: itemId });
      } catch (err) {
        if (err && err.code === 409) {
          // Ya existe un flujo de requisitos corriendo. Esperar por el próximo resultado que coincida con el itemId.
          const data = await new Promise((resolve, reject) => {
            requisitosWaitersByItem.set(itemId, { resolve, reject });
            // Polling de respaldo: leer outputs/convocatorias.json y detectar cuando se actualiza requisitos
            const pollReqs = async () => {
              try {
                const res = await fetch(`${API_URL}/outputs/convocatorias.json?t=${Date.now()}`);
                if (res.ok) {
                  const items = await res.json();
                  const it = Array.isArray(items) ? items.find(x => Number(x.id) === Number(itemId)) : null;
                  const reqs = it && Array.isArray(it.requisitos) ? it.requisitos : [];
                  if (reqs && reqs.length && !(reqs.length === 1 && String(reqs[0]).toLowerCase() === 'no especificado')) {
                    if (requisitosWaitersByItem.has(itemId)) {
                      requisitosWaitersByItem.delete(itemId);
                      resolve({ type: 'requisitos', result: { id: itemId, requirements: reqs } });
                      return;
                    }
                  }
                }
              } catch { }
              setTimeout(pollReqs, 2000);
            };
            setTimeout(pollReqs, 2000);
            setTimeout(() => {
              if (requisitosWaitersByItem.has(itemId)) {
                requisitosWaitersByItem.delete(itemId);
                reject(new Error('Timeout esperando requisitos (tarea existente)'));
              }
            }, 120000);
          });
          const res = data && data.result && Array.isArray(data.result.requirements) ? data.result.requirements : ['No especificado'];
          renderRequirementsIntoCard(cardEl, res);
          const btn = cardEl.querySelector('button[data-action="ver-requisitos"]');
          if (btn) btn.remove();
          // actualizar dataset en memoria
          try {
            if (Array.isArray(allItems)) {
              const idx = allItems.findIndex(x => Number(x.id) === Number(itemId));
              if (idx >= 0) allItems[idx] = { ...allItems[idx], requisitos: res };
            }
          } catch { }
          // Marcar mini-loader como completado si hay una tarjeta de requisitos pendiente (sin taskId conocido)
          try {
            for (const [tid, el] of taskCards.entries()) {
              const typeEl = el.querySelector('.flow-type');
              const statusEl = el.querySelector('.flow-status');
              if (typeEl && /requisitos/i.test(typeEl.textContent || '') && statusEl && /en progreso/i.test(statusEl.textContent || '')) {
                updateCard({ id: tid, type: 'requisitos' }, 'succeeded', { id: itemId, requirements: res });
                break;
              }
            }
          } catch { }
          if (!Number.isNaN(itemId)) localStorage.setItem(`reqLoaded:${itemId}`, '1');
          return; // listo
        }
        throw err;
      }
      // Esperar por SSE de éxito/fracaso con polling de respaldo por si SSE falla
      const data = await new Promise((resolve, reject) => {
        taskWaiters.set(taskId, { resolve, reject });
        let stopped = false;
        // Polling fallback cada 2s
        const poll = async () => {
          if (stopped) return;
          try {
            const r = await fetch(`${API_URL}/tasks/id/${taskId}`);
            if (r.ok) {
              const js = await r.json();
              const st = (js.status || '').toLowerCase();
              if (st === 'succeeded' || st === 'failed') {
                stopped = true;
                if (taskWaiters.has(taskId)) taskWaiters.delete(taskId);
                const payload = { type: js.type, id: js.id, result: js.result, error: js.error };
                if (st === 'succeeded') resolve(payload); else reject(new Error(js.error || 'Task failed'));
                return;
              }
            }
          } catch { }
          setTimeout(poll, 2000);
        };
        setTimeout(poll, 2000);
        setTimeout(() => {
          if (taskWaiters.has(taskId)) {
            taskWaiters.delete(taskId);
            reject(new Error('Timeout esperando requisitos'));
          }
        }, 120000);
      });
      const res = data && data.result && Array.isArray(data.result.requirements) ? data.result.requirements : ['No especificado'];
      renderRequirementsIntoCard(cardEl, res);
      // actualizar dataset en memoria
      try {
        if (Array.isArray(allItems)) {
          const idx = allItems.findIndex(x => Number(x.id) === Number(itemId));
          if (idx >= 0) allItems[idx] = { ...allItems[idx], requisitos: res };
        }
      } catch { }
      // Marcar mini-loader como completado con el taskId
      try { updateCard({ id: taskId, type: 'requisitos' }, 'succeeded', { id: itemId, requirements: res }); } catch { }
      const btn = cardEl.querySelector('button[data-action="ver-requisitos"]');
      if (btn) btn.remove();
      if (!Number.isNaN(itemId)) localStorage.setItem(`reqLoaded:${itemId}`, '1');
    } catch (err) {
      console.error('Ver Requisitos error:', err);
      // No sobreescribir con 'No especificado' si hay error de 409 o timeout
      if (!(err && (err.code === 409))) {
        renderRequirementsIntoCard(cardEl, ['No especificado']);
      }
    }
  }

  function renderRequirementsIntoCard(cardEl, requirements) {
    if (!cardEl) return;
    let reqBlock = cardEl.querySelector('.info-item.req-block');
    if (!reqBlock) {
      // Insertar después del bloque de BENEFICIOS si existe, si no, al final
      reqBlock = document.createElement('div');
      reqBlock.className = 'info-item req-block';
      reqBlock.innerHTML = `
        <div class="item-header">
          <span class="icon-wrapper"><i class="fa-solid fa-list-check"></i></span>
          <label>REQUISITOS</label>
        </div>
        <div class="requirements-list"><ul></ul></div>
      `;
      // Buscar específicamente el bloque con etiqueta BENEFICIOS
      const labels = cardEl.querySelectorAll('.info-item .item-header label');
      let benefitsItem = null;
      labels.forEach(lab => {
        if (!benefitsItem && String(lab.textContent || '').trim().toUpperCase() === 'BENEFICIOS') {
          const it = lab.closest('.info-item');
          if (it) benefitsItem = it;
        }
      });
      if (benefitsItem && benefitsItem.parentNode) {
        benefitsItem.parentNode.insertBefore(reqBlock, benefitsItem.nextSibling);
      } else {
        const grid = cardEl.querySelector('.card-body .details-grid');
        grid && grid.appendChild(reqBlock);
      }
    }
    const ul = reqBlock.querySelector('ul');
    if (ul) {
      ul.innerHTML = '';
      const reqList = Array.isArray(requirements) ? requirements : (typeof requirements === 'string' ? requirements.split(/\n|\r|;|\u2022|\•/).map(s => s.trim()).filter(Boolean) : []);
      reqList.forEach(r => {
        const li = document.createElement('li');
        li.textContent = String(r);
        ul.appendChild(li);
      });
    }
  }

  // Se elimina renderSourcesIntoCard; usamos la sección "Más Información" existente.

  // =======================================================
  // 1. SOLUCIÓN DEFINITIVA AL REFRESH DE PÁGINA
  // =======================================================
  // Evita que el formulario principal provoque recargas involuntarias
  if (magazineForm) {
    magazineForm.addEventListener('submit', (event) => {
      event.preventDefault();
      console.warn('Se ha prevenido el envío del formulario principal.');
    });
  }

  // Selected items Map: id -> title
  const selectedItems = new Map();

  // Estado de cards para filtros/paginación
  let allItems = [];
  let filteredItems = [];
  let currentPage = 1;
  const pageSize = 5;
  let currentTimeMode = 'active';
  let currentCategory = 'all';

  generateBtn.addEventListener('click', async (e) => {
    e.preventDefault();
    if (generateBtn.disabled) return;
    generateBtn.disabled = true;
    try {
      const tema = buildTemaFromSavedOptions();
      const taskId = await enqueueTask('magazine', tema ? { tema } : {});
      // Esperar resultado por SSE con fallback a polling y actualizar mini-card
      await new Promise((resolve, reject) => {
        taskWaiters.set(taskId, { resolve, reject });
        let stopped = false;
        const poll = async () => {
          if (stopped) return;
          try {
            const r = await fetch(`${API_URL}/tasks/id/${taskId}`);
            if (r.ok) {
              const js = await r.json();
              const st = (js.status || '').toLowerCase();
              if (st === 'succeeded') {
                stopped = true;
                if (taskWaiters.has(taskId)) taskWaiters.delete(taskId);
                try { updateCard({ id: taskId, type: 'magazine' }, 'succeeded', js.result); } catch { }
                // Abrir PDF si viene en result
                try {
                  const pdfUrl = js.result && js.result.pdf_url ? (js.result.pdf_url.startsWith('http') ? js.result.pdf_url : `${API_URL}${js.result.pdf_url}`) : null;
                  if (pdfUrl) window.open(pdfUrl, '_blank', 'noopener');
                } catch { }
                resolve(js);
                return;
              }
              if (st === 'failed') {
                stopped = true;
                if (taskWaiters.has(taskId)) taskWaiters.delete(taskId);
                try { updateCard({ id: taskId, type: 'magazine' }, 'failed'); } catch { }
                reject(new Error(js.error || 'Task failed'));
                return;
              }
            }
          } catch { }
          setTimeout(poll, 2000);
        };
        setTimeout(poll, 2000);
        setTimeout(() => { if (taskWaiters.has(taskId)) { taskWaiters.delete(taskId); reject(new Error('Timeout magazine')); } }, 120000);
      });
    } catch (err) {
      showError(err.message || String(err));
    } finally {
      generateBtn.disabled = false;
    }
  });

  // Options panel handlers
  if (optionsBtn) {
    optionsBtn.addEventListener('click', () => {
      loadSavedOptionsIntoUI();
      optionsPanel.classList.remove('hidden');
      optionsPanel.setAttribute('aria-hidden', 'false');
    });
  }
  if (closeOptions) {
    closeOptions.addEventListener('click', () => {
      optionsPanel.classList.add('hidden');
      optionsPanel.setAttribute('aria-hidden', 'true');
    });
  }
  if (saveOptions) {
    saveOptions.addEventListener('click', () => {
      const sel = getSelectedTopicFromUI();
      localStorage.setItem('topic_selection', JSON.stringify(sel));
      optionsPanel.classList.add('hidden');
      optionsPanel.setAttribute('aria-hidden', 'true');
    });
  }
  // enable/disable otherTopic
  document.querySelectorAll('input[name="topic"]').forEach(r => {
    r.addEventListener('change', () => {
      if (r.value === 'other' && r.checked) {
        otherTopic.disabled = false;
        otherTopic.focus();
      } else if (r.checked) {
        otherTopic.disabled = true;
        otherTopic.value = '';
      }
    });
  });

  // PDF Cart panel open/close and generate
  if (pdfCartBtn) {
    pdfCartBtn.addEventListener('click', () => {
      if (selectedItems.size > 0 && pdfCartPanel) {
        updatePdfCartList();
        pdfCartPanel.classList.remove('hidden');
        pdfCartPanel.setAttribute('aria-hidden', 'false');
      }
    });
  }
  if (closePdfCart) {
    closePdfCart.addEventListener('click', () => {
      pdfCartPanel.classList.add('hidden');
      pdfCartPanel.setAttribute('aria-hidden', 'true');
    });
  }
  if (generatePdfFromCartBtn) {
    generatePdfFromCartBtn.addEventListener('click', async (event) => {
      // Prevent default (submit/refresh) and bubbling that could close the panel
      if (event && typeof event.preventDefault === 'function') event.preventDefault();
      if (event && typeof event.stopPropagation === 'function') event.stopPropagation();
      if (selectedItems.size === 0) return;
      try {
        // Pre-abrir ventanas en el gesto del usuario para evitar bloqueadores de popups
        // Usa nombres de ventana fijos y evita 'noopener' para conservar el handle
        const pdfWin = window.open('about:blank', 'pdf_tab');
        const viewerWin = window.open('about:blank', 'viewer_tab');
        const prime = (win, title, targetUrl) => {
          try {
            if (!win || !win.document) return;
            const doc = win.document;
            doc.open();
            doc.write(`<!DOCTYPE html><html><head><meta charset="utf-8"><title>${title}</title><meta http-equiv="refresh" content="0;url='${targetUrl || ''}'"></head><body style="font-family:sans-serif;color:#111">
              <p>${title}</p>
              ${targetUrl ? `<p>Si no redirige automáticamente, <a href="${targetUrl}" target="_self">haz clic aquí</a>.</p>` : ''}
              <script>try{ if('${targetUrl || ''}') { setTimeout(function(){ location.href='${targetUrl}'; }, 150); } }catch(e){}</script>
            </body></html>`);
            doc.close();
          } catch { }
        };
        // Placeholders visibles mientras cargan
        try { if (pdfWin && pdfWin.document) { pdfWin.document.title = 'Abriendo PDF...'; pdfWin.document.body.innerHTML = '<p style="font-family:sans-serif">Abriendo PDF...</p>'; } } catch { }
        try { if (viewerWin && viewerWin.document) { viewerWin.document.title = 'Abriendo visor...'; viewerWin.document.body.innerHTML = '<p style="font-family:sans-serif">Abriendo visor...</p>'; } } catch { }
        const res = await fetch(`${API_URL}/api/generate_pdf_from_ids`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ ids: Array.from(selectedItems.keys()) })
        });
        if (!res.ok) throw new Error('No se pudo generar el PDF');
        const data = await res.json();
        // Calcular URLs absolutas
        const pdfAbs = data.pdf_url ? (data.pdf_url.startsWith('http') ? data.pdf_url : `${API_URL}${data.pdf_url}`) : '';
        let viewerAbs = '';
        if (data.viewer_url) {
          viewerAbs = data.viewer_url.startsWith('http') ? data.viewer_url : `${API_URL}${data.viewer_url}`;
        } else if (pdfAbs) {
          // Fallback: construir viewer usando el PDF absoluto como parámetro
          viewerAbs = `${API_URL}/viewer?file=${encodeURIComponent(pdfAbs)}`;
        }

        // Asignar URLs a las ventanas ya abiertas
        if (pdfAbs) {
          if (pdfWin) { try { prime(pdfWin, 'Abriendo PDF...', pdfAbs); pdfWin.location = pdfAbs; } catch { window.open(pdfAbs, 'pdf_tab'); } }
          else { window.open(pdfAbs, 'pdf_tab'); }
        } else if (pdfWin) {
          try { pdfWin.document.body.innerHTML = '<p style="font-family:sans-serif;color:#b91c1c">No se recibió PDF.</p>'; } catch { }
        }
        if (viewerAbs) {
          if (viewerWin) { try { prime(viewerWin, 'Abriendo visor...', viewerAbs); viewerWin.location = viewerAbs; } catch { window.open(viewerAbs, 'viewer_tab'); } }
          else { window.open(viewerAbs, 'viewer_tab'); }
        } else if (viewerWin) {
          try { viewerWin.document.body.innerHTML = '<p style=\"font-family:sans-serif;color:#b91c1c\">No se recibió visor.</p>'; } catch { }
        }
        // Cerrar panel del carrito tras abrir ventanas
        if (pdfCartPanel) {
          pdfCartPanel.classList.add('hidden');
          pdfCartPanel.setAttribute('aria-hidden', 'true');
        }
      } catch (e) {
        showError(e.message || String(e));
      }
    });
  }

  // Sources admin
  if (sourcesBtn) {
    sourcesBtn.addEventListener('click', async () => {
      sourcesPanel.classList.remove('hidden');
      sourcesPanel.setAttribute('aria-hidden', 'false');
      // activar pestaña "Ver" por defecto al abrir
      const viewTabBtn = document.querySelector('.sources-tabs .tab-btn[data-tab="view"]');
      if (viewTabBtn) viewTabBtn.click();
      await refreshSources();
    });
  }
  if (closeSources) {
    closeSources.addEventListener('click', () => {
      sourcesPanel.classList.add('hidden');
      sourcesPanel.setAttribute('aria-hidden', 'true');
    });
  }
  if (addSourceBtn) {
    addSourceBtn.addEventListener('click', async () => {
      const name = srcName.value.trim();
      const type = srcType.value.trim();
      const url = srcUrl.value.trim();
      if (!name || !url) return;
      try {
        const res = await fetch(`${API_URL}/sources`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, type, url })
        });
        if (!res.ok) {
          let msg = 'No se pudo agregar la fuente';
          try {
            const err = await res.json();
            if (err && err.detail) msg = String(err.detail);
          } catch { }
          throw new Error(msg);
        }
        srcName.value = ''; srcType.value = ''; srcUrl.value = '';
        const viewTabBtn = document.querySelector('.sources-tabs .tab-btn[data-tab="view"]');
        if (viewTabBtn) viewTabBtn.click();
        await refreshSources();
      } catch (e) {
        showError(e.message || String(e));
      }
    });
  }

  // Tabs de Sources (Ver / Agregar / AI)
  if (sourcesTabs && sourcesTabs.length) {
    sourcesTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        sourcesTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const aiTab = document.getElementById('sourcesAITab');
        if (tab.dataset.tab === 'view') {
          sourcesViewTab?.classList.remove('hidden');
          sourcesAddTab?.classList.add('hidden');
          aiTab?.classList.add('hidden');
        } else if (tab.dataset.tab === 'add') {
          sourcesViewTab?.classList.add('hidden');
          sourcesAddTab?.classList.remove('hidden');
          aiTab?.classList.add('hidden');
        } else if (tab.dataset.tab === 'ai') {
          sourcesViewTab?.classList.add('hidden');
          sourcesAddTab?.classList.add('hidden');
          aiTab?.classList.remove('hidden');
        }
      });
    });
  }

  async function generarMagazine() { /* deprecated: background tasks via /tasks */ }

  function showLoading() {
    if (loadingOverlay) loadingOverlay.classList.remove('hidden');
    if (generateBtn) generateBtn.disabled = true;
    updateStatus('Generando...');
  }
  function hideLoading() {
    if (loadingOverlay) loadingOverlay.classList.add('hidden');
    if (generateBtn) generateBtn.disabled = false;
  }
  function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
  }
  function hideError() {
    errorDiv.classList.add('hidden');
  }
  function showSuccess() {
    if (successDiv) successDiv.classList.remove('hidden');
  }
  function hideSuccess() {
    if (successDiv) successDiv.classList.add('hidden');
  }

  function updateStatus(text) {
    if (statusEl) {
      statusEl.dataset.text = text;
    }
  }

  // =======================
  // Mini Loader (tarjetas)
  // =======================
  const flowMiniLoader = document.getElementById('flow-mini-loader');
  const taskCards = new Map(); // taskId -> cardEl

  function ensureMiniLoader() {
    if (!flowMiniLoader) return;
    flowMiniLoader.classList.add('mini-flow-host');
  }

  function createCard(task) {
    ensureMiniLoader();
    const { id, type } = task || {};
    if (!id) return;
    if (taskCards.has(id)) return; // evitar duplicados cuando llega task_started tras enqueue
    const card = document.createElement('div');
    card.className = 'flow-card glass';
    card.dataset.id = id;
    card.innerHTML = `
      <div class="flow-card-header">
        <div class="spinner sm"></div>
        <div class="flow-title">Cargando flujo de IA...</div>
      </div>
      <div class="flow-meta">
        <span class="flow-type">${escapeHtml(type || '')}</span>
        <span class="flow-status badge blue">en progreso</span>
      </div>
    `;
    flowMiniLoader.appendChild(card);
    taskCards.set(id, card);
  }

  function updateCard(task, status, info) {
    const card = taskCards.get(task.id);
    if (!card) return;
    const statusEl = card.querySelector('.flow-status');
    const headerSpinner = card.querySelector('.spinner');
    if (!statusEl) return;
    if (status === 'succeeded') {
      statusEl.textContent = 'completado';
      statusEl.className = 'flow-status badge green';
      // Reemplazar spinner por icono de check
      if (headerSpinner) {
        const ok = document.createElement('i');
        ok.className = 'fa-solid fa-check';
        ok.style.color = '#10b981';
        ok.style.fontSize = '14px';
        headerSpinner.replaceWith(ok);
      }
      setTimeout(() => { card.remove(); taskCards.delete(task.id); }, 6000);
    } else if (status === 'failed') {
      statusEl.textContent = 'error';
      statusEl.className = 'flow-status badge red';
      // Reemplazar spinner por icono de x
      if (headerSpinner) {
        const x = document.createElement('i');
        x.className = 'fa-solid fa-xmark';
        x.style.color = '#ef4444';
        x.style.fontSize = '16px';
        headerSpinner.replaceWith(x);
      }
    } else if (status === 'running') {
      statusEl.textContent = 'en progreso';
      statusEl.className = 'flow-status badge blue';
    }
  }

  // Encolar tarea vía API
  async function enqueueTask(type, payload) {
    const res = await fetch(`${API_URL}/api/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type, payload: payload || {} })
    });
    if (res.status === 409) {
      const msg = await res.json().catch(() => ({ detail: 'Flujo ya en ejecución' }));
      const err = new Error(msg.detail || 'Flujo ya en ejecución');
      err.code = 409;
      throw err;
    }
    if (!res.ok) {
      const msg = await res.json().catch(() => ({ detail: 'Error creando tarea' }));
      throw new Error(msg.detail || 'Error creando tarea');
    }
    const data = await res.json();
    const task = { id: data.id, type };
    createCard(task);
    return task.id;
  }

  // Conectar SSE global y rehidratación
  // Mapa de promesas para esperar resultado por task id
  const taskWaiters = new Map();
  // Mapa de promesas para esperar resultado por itemId (para requisitos cuando hay 409)
  const requisitosWaitersByItem = new Map();

  function connectSSE() {
    try {
      const es = new EventSource(`${API_URL}/api/tasks/stream`);
      es.addEventListener('task_started', async (ev) => {
        try {
          const data = JSON.parse(ev.data || '{}');
          if (await taskBelongsToMe(data.id)) createCard({ id: data.id, type: data.type });
        } catch { }
      });
      es.addEventListener('task_progress', async (ev) => {
        try {
          const data = JSON.parse(ev.data || '{}');
          if (await taskBelongsToMe(data.id)) updateCard({ id: data.id, type: data.type }, 'running');
        } catch { }
      });
      es.addEventListener('task_succeeded', async (ev) => {
        try {
          const data = JSON.parse(ev.data || '{}');
          if (!(await taskBelongsToMe(data.id))) return;
          updateCard({ id: data.id, type: data.type }, 'succeeded', data.result);
          showToast(`Flujo ${data.type} terminado exitosamente!!`, 'success');
          // Resolver posibles esperas ligadas a esta tarea
          const waiter = taskWaiters.get(data.id);
          if (waiter && typeof waiter.resolve === 'function') {
            try { waiter.resolve(data); } catch { }
            taskWaiters.delete(data.id);
          }
          // Resolver esperas por itemId de requisitos
          if (data.type === 'requisitos' && data.result && typeof data.result.id === 'number') {
            // actualizar dataset en memoria para evitar que desaparezcan al re-renderizar
            try {
              if (Array.isArray(allItems)) {
                const idx = allItems.findIndex(x => Number(x.id) === Number(data.result.id));
                if (idx >= 0) {
                  const reqs = Array.isArray(data.result.requirements) ? data.result.requirements : [];
                  allItems[idx] = { ...allItems[idx], requisitos: reqs.length ? reqs : ['No especificado'] };
                }
              }
            } catch { }
            const w = requisitosWaitersByItem.get(data.result.id);
            if (w && typeof w.resolve === 'function') {
              try { w.resolve(data); } catch { }
              requisitosWaitersByItem.delete(data.result.id);
            }
          }
          if (data.type === 'magazine' && data.result && data.result.pdf_url) {
            const pdfUrl = data.result.pdf_url.startsWith('http') ? data.result.pdf_url : `${API_URL}${data.result.pdf_url}`;
            window.open(pdfUrl, '_blank', 'noopener');
          }
        } catch { }
      });
      es.addEventListener('task_failed', async (ev) => {
        try {
          const data = JSON.parse(ev.data || '{}');
          if (!(await taskBelongsToMe(data.id))) return;
          updateCard({ id: data.id, type: data.type }, 'failed');
          showToast(`Flujo ${data.type} falló`, 'error');
          const waiter = taskWaiters.get(data.id);
          if (waiter && typeof waiter.reject === 'function') {
            try { waiter.reject(new Error(data.error || 'Task failed')); } catch { }
            taskWaiters.delete(data.id);
          }
          if (data.type === 'requisitos' && data.result && typeof data.result.id === 'number') {
            const w = requisitosWaitersByItem.get(data.result.id);
            if (w && typeof w.reject === 'function') {
              try { w.reject(new Error(data.error || 'Task failed')); } catch { }
              requisitosWaitersByItem.delete(data.result.id);
            }
          }
        } catch { }
      });
      es.onerror = () => { /* el navegador reintenta solo */ };
    } catch { }
  }

  async function rehydrateActiveTasks() {
    try {
      const res = await fetch(`${API_URL}/api/tasks?status=active`);
      if (!res.ok) return;
      const data = await res.json();
      const tasks = Array.isArray(data.tasks) ? data.tasks : [];
      const myId = await getCurrentUserId();
      tasks.forEach(t => {
        const uid = Number((t && t.user_id) || 0);
        if (t && t.id && myId && uid === myId) createCard({ id: t.id, type: t.type });
      });
    } catch { }
  }

  function showToast(message, level) {
    try { alert(message); } catch { }
  }

  // Inicializar SSE y rehidratación
  connectSSE();
  rehydrateActiveTasks();

  function renderConvocatorias(items) {
    const container = document.getElementById('convocatorias-container');
    if (!container) return;
    allItems = Array.isArray(items) ? items : [];
    currentPage = 1;
    applyFiltersAndRender();
  }

  function applyFiltersAndRender() {
    const container = document.getElementById('convocatorias-container');
    if (!container) return;
    // Filtrado por tiempo
    const mode = getTimeFilterMode();
    const range = getRangeValues();
    filteredItems = allItems
      .filter((it) => matchesTimeFilter(it, mode, range))
      .filter((it) => matchesCategory(it, currentCategory));
    // Render de página actual
    const totalPages = Math.max(1, Math.ceil(filteredItems.length / pageSize));
    if (currentPage > totalPages) currentPage = totalPages;
    const start = (currentPage - 1) * pageSize;
    const pageSlice = filteredItems.slice(start, start + pageSize);
    renderCards(pageSlice);
    // Actualizar paginación
    if (pageInfoEl) pageInfoEl.textContent = `${totalPages === 0 ? 0 : currentPage} / ${totalPages}`;
    if (pagePrevBtn) pagePrevBtn.disabled = currentPage <= 1;
    if (pageNextBtn) pageNextBtn.disabled = currentPage >= totalPages;
    // Actualizar estado de "Seleccionar todas"
    updateSelectAllVisibleState();
  }

  function renderCards(items) {
    const container = document.getElementById('convocatorias-container');
    if (!container) return;
    container.innerHTML = '';

    const catTitle = (tipo) => {
      const t = (tipo || '').toLowerCase();
      if (t === 'convocatoria_nacional') return 'Convocatorias Nacionales';
      if (t === 'convocatoria_internacional') return 'Convocatorias Internacionales';
      if (t === 'evento') return 'Eventos';
      return 'Convocatorias';
    };
    const catKey = (tipo) => {
      const t = (tipo || '').toLowerCase();
      if (t === 'convocatoria_nacional') return 'nacional';
      if (t === 'convocatoria_internacional') return 'internacional';
      if (t === 'evento') return 'evento';
      return 'nacional';
    };

    const buckets = { nacional: [], internacional: [], evento: [] };
    items.forEach((it) => {
      // --- USAREMOS LAS CLAVES EN ESPAÑOL QUE LA API ENVÍA ---
      const tipoKey = catKey(it.tipo); // 'tipo' parece ser la clave correcta que envía la API
      const headerTitle = catTitle(it.tipo);
      const esEvento = tipoKey === 'evento';

      // Extracción de datos usando las claves en español
      const titulo = it.titulo || 'Sin Título';
      const dirigido = it.dirigido_a || 'No especificado';
      const fechaInicio = it.fecha_inicio || it.inicio || '';
      const cierre = it.fecha_cierre || it.fecha || it.deadline || 'No especificado';
      const objetivo = it.objetivo || it.objetivos || 'No especificado';
      const descripcion = it.descripcion || objetivo; // Usar objetivo como fallback para descripción

      // Manejo especial para 'beneficios' que puede ser un array
      const beneficios = Array.isArray(it.beneficios)
        ? it.beneficios.map(b => `• ${b}`).join('<br>') // Crea una lista con viñetas
        : (it.beneficios || 'No especificado');

      const lugar = it.lugar || 'No especificado';
      const monto = it.monto || it.monto_financiacion || it.financiacion || '';
      const keywordsVal = it.keywords || it.palabras_clave || it.tags || [];
      const keywords = Array.isArray(keywordsVal) ? keywordsVal.join(', ') : (keywordsVal || '');
      const url = it.url_original || it.url || it.source || ''; // Buscar en varios posibles nombres

      const card = document.createElement('div');
      card.className = 'call-card';
      card.dataset.category = tipoKey;
      const id = it.id != null ? Number(it.id) : NaN;
      if (it.created_at) card.dataset.createdAt = it.created_at;
      if (!Number.isNaN(id)) card.dataset.id = String(id);
      const requisitosVal = it.requisitos;
      const requisitosArr = Array.isArray(requisitosVal) ? requisitosVal : (typeof requisitosVal === 'string' && requisitosVal.trim() ? requisitosVal.split(/\n|\r|;|\u2022|\•/).map(s => s.trim()).filter(Boolean) : []);
      const requisitosValid = requisitosArr.length > 0 && !(requisitosArr.length === 1 && String(requisitosArr[0]).toLowerCase() === 'no especificado');
      const alreadyLoadedReqs = requisitosValid; // no ocultar por localStorage si no hay requisitos

      const cbxId = !Number.isNaN(id) ? `cbx-flip-${id}` : `cbx-flip-${Math.random().toString(36).slice(2)}`;
      const initiallyChecked = !Number.isNaN(id) && selectedItems.has(id);
      card.innerHTML = `
        <div class="card-checkbox-container">
          <input class="checkbox" id="${cbxId}" type="checkbox" ${initiallyChecked ? 'checked' : ''} />
          <label class="checkbox-label" for="${cbxId}">
            <div class="checkbox-flip">
              <div class="checkbox-front">
                <svg fill="white" height="24" width="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path d="M19 13H12V19H11V13H5V12H11V6H12V12H19V13Z"></path>
                </svg>
              </div>
              <div class="checkbox-back">
                <svg fill="white" height="24" width="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 19l-7-7 1.41-1.41L9 16.17l11.29-11.3L22 6l-13 13z"></path>
                </svg>
              </div>
            </div>
          </label>
        </div>
        <header class="card-header">
          <h2>${headerTitle}</h2>
        </header>
        <div class="card-body">
          <h1 class="card-title">${escapeHtml(titulo)}</h1>
          <div class="details-grid">
            ${esEvento ? `
              <div class="info-item">
                <div class="item-header">
                  <span class="icon-wrapper"><i class="fa-solid fa-file-lines"></i></span>
                  <label>DESCRIPCIÓN</label>
                </div>
                <p>${escapeHtml(descripcion)}</p>
              </div>
              <div class="info-item">
                <div class="item-header">
                  <span class="icon-wrapper"><i class="fa-solid fa-bullseye"></i></span>
                  <label>OBJETIVOS</label>
                </div>
                <p>${escapeHtml(objetivo)}</p>
              </div>
              <div class="info-item">
                <div class="item-header">
                  <span class="icon-wrapper"><i class="fa-solid fa-clock"></i></span>
                  <label>FECHA</label>
                </div>
                <p>${escapeHtml(cierre)}</p>
              </div>
              <div class="info-item">
                <div class="item-header">
                  <span class="icon-wrapper"><i class="fa-solid fa-location-dot"></i></span>
                  <label>LUGAR</label>
                </div>
                <p>${escapeHtml(lugar)}</p>
              </div>
              ${monto ? `
              <div class="info-item">
                <div class="item-header">
                  <span class="icon-wrapper"><i class="fa-solid fa-money-bill-wave"></i></span>
                  <label>MONTO</label>
                </div>
                <p>${escapeHtml(monto)}</p>
              </div>` : ''}
              ${keywords ? `
              <div class="info-item">
                <div class="item-header">
                  <span class="icon-wrapper"><i class="fa-solid fa-tags"></i></span>
                  <label>KEYWORDS</label>
                </div>
                <p>${escapeHtml(keywords)}</p>
              </div>` : ''}
            ` : `
              <div class="info-item">
                <div class="item-header">
                  <span class="icon-wrapper"><i class="fa-solid fa-user"></i></span>
                  <label>DIRIGIDO A</label>
                </div>
                <p>${escapeHtml(dirigido)}</p>
              </div>
              <div class="info-item">
                <div class="item-header">
                  <span class="icon-wrapper"><i class="fa-solid fa-calendar"></i></span>
                  <label>FECHAS IMPORTANTES</label>
                </div>
                <p>
                  <strong>Fecha de Inicio:</strong> ${escapeHtml(fechaInicio || 'No especificado')}<br>
                  <strong>Fecha de Cierre:</strong> ${escapeHtml(cierre)}
                </p>
              </div>
              <div class="info-item">
                <div class="item-header">
                  <span class="icon-wrapper"><i class="fa-solid fa-bullseye"></i></span>
                  <label>OBJETIVO</label>
                </div>
                <p>${escapeHtml(objetivo)}</p>
              </div>
              <div class="info-item">
                <div class="item-header">
                  <span class="icon-wrapper"><i class="fa-solid fa-check"></i></span>
                  <label>BENEFICIOS</label>
                </div>
                <p>${beneficios}</p>
              </div>
              ${monto ? `
              <div class="info-item">
                <div class="item-header">
                  <span class="icon-wrapper"><i class="fa-solid fa-money-bill-wave"></i></span>
                  <label>MONTO</label>
                </div>
                <p>${escapeHtml(monto)}</p>
              </div>` : ''}
              ${keywords ? `
              <div class="info-item">
                <div class="item-header">
                  <span class="icon-wrapper"><i class="fa-solid fa-tags"></i></span>
                  <label>KEYWORDS</label>
                </div>
                <p>${escapeHtml(keywords)}</p>
              </div>` : ''}
            `}
            <div class="info-item">
              <div class="item-header">
                <span class="icon-wrapper"><i class="fa-solid fa-link"></i></span>
                <label>MÁS INFORMACIÓN</label>
              </div>
              <p>${url ? `<a href="${escapeAttr(url)}" target="_blank" rel="noopener">${escapeHtml(url)}</a>` : 'No especificado'}</p>
            </div>
            <div class="card-actions" style="margin-top:16px;display:flex;gap:12px;flex-wrap:wrap;">
              ${alreadyLoadedReqs ? '' : `
              <button type="button" class="btn-animated-icon" data-action="ver-requisitos">
                <div class="svg-wrapper-1"><div class="svg-wrapper">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20"><path fill="none" d="M0 0h24v24H0z"/><path d="M4 4h16v2H4zM4 11h16v2H4zM4 18h16v2H4z"/></svg>
                </div></div>
                <span>Ver Requisitos</span>
              </button>`}
            </div>
          </div>
        </div>
      `;
      const inputEl = card.querySelector(`#${cbxId}`);
      if (inputEl && !Number.isNaN(id)) {
        inputEl.addEventListener('change', () => {
          if (inputEl.checked) {
            selectedItems.set(id, titulo);
          } else {
            selectedItems.delete(id);
          }
          updateCartCount();
        });
      }
      buckets[tipoKey].push(card);
    });

    ['nacional', 'internacional', 'evento'].forEach((key) => {
      buckets[key].forEach((card) => container.appendChild(card));
    });
    // Listeners de checkboxes para sincronizar "Seleccionar todas"
    updateSelectAllVisibleState();

    // Renderizar requisitos preexistentes
    container.querySelectorAll('.call-card').forEach((cardEl) => {
      const idStr = cardEl.dataset.id;
      if (!idStr) return;
      const it = items.find(x => String(x.id) === idStr);
      if (!it) return;
      const reqs = Array.isArray(it.requisitos) ? it.requisitos : (typeof it.requisitos === 'string' ? it.requisitos.split(/\n|\r|;|\u2022|\•/).map(s => s.trim()).filter(Boolean) : []);
      if (reqs.length && !(reqs.length === 1 && String(reqs[0]).toLowerCase() === 'no especificado')) {
        renderRequirementsIntoCard(cardEl, reqs);
      }
    });

    // Delegación: botón Ver Requisitos
    container.addEventListener('click', async (ev) => {
      const btn = ev.target.closest('button[data-action="ver-requisitos"]');
      if (!btn) return;
      if (btn.disabled) return;
      const cardEl = btn.closest('.call-card');
      const idStr = cardEl && cardEl.dataset.id;
      if (!idStr) return;
      const itemId = Number(idStr);
      btn.disabled = true;
      try {
        await handleVerRequisitos(itemId, cardEl);
      } catch (e) {
        // En caso de error, permitir reintentar
        if (document.body.contains(btn)) btn.disabled = false;
      }
    });
  }

  // Exponer globalmente para reutilización desde otros módulos (p. ej., savedMagazines.js)
  window.renderConvocatorias = renderConvocatorias;

  // =======================
  // Filtros y paginación UI
  // =======================
  // Mostrar/ocultar controles de rango solo en modo "Periodo"
  function updateRangeControlsVisibility(show) {
    const disp = show ? '' : 'none';
    if (startDateInput) startDateInput.style.display = disp;
    if (endDateInput) endDateInput.style.display = disp;
    if (applyRangeBtn) applyRangeBtn.style.display = disp;
    if (startDateInput) startDateInput.disabled = !show;
    if (endDateInput) endDateInput.disabled = !show;
    if (applyRangeBtn) applyRangeBtn.disabled = !show;
  }

  // Filtro Estado (Activas por defecto)
  if (btnActive && btnClosed && btnRange) {
    const timeButtons = [btnActive, btnClosed, btnRange];
    // Estado inicial: Activas
    currentTimeMode = 'active';
    timeButtons.forEach(x => x.classList.remove('active'));
    btnActive.classList.add('active');
    updateRangeControlsVisibility(false);
    applyFiltersAndRender();

    timeButtons.forEach(b => {
      b.addEventListener('click', () => {
        timeButtons.forEach(x => x.classList.remove('active'));
        b.classList.add('active');
        const mode = b.dataset.time || 'active';
        if (mode === 'range') {
          // Entrar a Periodo: mostrar inputs pero NO aplicar aún
          currentTimeMode = 'range';
          updateRangeControlsVisibility(true);
          // mantener la vista actual hasta que se presione Aplicar
        } else {
          // Activas o Cerradas: ocultar inputs y aplicar de una vez
          currentTimeMode = mode;
          updateRangeControlsVisibility(false);
          currentPage = 1;
          applyFiltersAndRender();
        }
      });
    });

    if (applyRangeBtn) {
      applyRangeBtn.addEventListener('click', () => {
        if (currentTimeMode === 'range') {
          currentPage = 1;
          applyFiltersAndRender();
        }
      });
    }
  }

  if (pagePrevBtn) {
    pagePrevBtn.innerHTML = '<i class="fa-solid fa-chevron-left"></i>';
    pagePrevBtn.addEventListener('click', () => {
      if (currentPage > 1) { currentPage--; applyFiltersAndRender(); }
    });
  }
  if (pageNextBtn) {
    pageNextBtn.innerHTML = '<i class="fa-solid fa-chevron-right"></i>';
    pageNextBtn.addEventListener('click', () => {
      const totalPages = Math.max(1, Math.ceil(filteredItems.length / pageSize));
      if (currentPage < totalPages) { currentPage++; applyFiltersAndRender(); }
    });
  }
  // Categorías: Todos/Nacionales/Internacionales/Eventos
  if (categoryFiltersContainer) {
    const catButtons = Array.from(categoryFiltersContainer.querySelectorAll('button'));
    if (catButtons.length) {
      // Estado inicial: Todos
      catButtons.forEach(b => b.classList.remove('active'));
      const allBtn = catButtons.find(b => (b.dataset.filter || '') === 'all') || catButtons[0];
      if (allBtn) allBtn.classList.add('active');
      currentCategory = (allBtn && allBtn.dataset.filter) ? allBtn.dataset.filter : 'all';
      catButtons.forEach(btn => {
        btn.addEventListener('click', () => {
          catButtons.forEach(x => x.classList.remove('active'));
          btn.classList.add('active');
          currentCategory = btn.dataset.filter || 'all';
          currentPage = 1;
          applyFiltersAndRender();
        });
      });
    }
  }
  if (selectAllVisibleCbx) {
    selectAllVisibleCbx.addEventListener('change', () => {
      const container = document.getElementById('convocatorias-container');
      if (!container) return;
      const checkboxes = container.querySelectorAll('.card-checkbox-container input.checkbox');
      checkboxes.forEach((cbx) => {
        const inputEl = cbx;
        const idMatch = inputEl.id.match(/cbx-flip-(.+)$/);
        const card = inputEl.closest('.call-card');
        const visible = card && card.style.display !== 'none';
        if (!visible) return;
        const shouldCheck = !!selectAllVisibleCbx.checked;
        if (inputEl.checked !== shouldCheck) {
          inputEl.checked = shouldCheck;
          // disparar el handler manualmente
          inputEl.dispatchEvent(new Event('change'));
        }
      });
    });
  }

  function updateSelectAllVisibleState() {
    if (!selectAllVisibleCbx) return;
    const container = document.getElementById('convocatorias-container');
    if (!container) return;
    const visibleCheckboxes = Array.from(container.querySelectorAll('.call-card'))
      .filter(c => c.style.display !== 'none')
      .map(c => c.querySelector('.card-checkbox-container input.checkbox'))
      .filter(Boolean);
    if (visibleCheckboxes.length === 0) { selectAllVisibleCbx.checked = false; return; }
    const allChecked = visibleCheckboxes.every((el) => el.checked);
    selectAllVisibleCbx.checked = allChecked;
  }

  function getTimeFilterMode() {
    return currentTimeMode;
  }
  function getRangeValues() {
    const start = startDateInput && startDateInput.value ? new Date(startDateInput.value) : null;
    const end = endDateInput && endDateInput.value ? new Date(endDateInput.value) : null;
    if (start) start.setHours(0, 0, 0, 0);
    if (end) end.setHours(23, 59, 59, 999);
    return { start, end };
  }
  function parseDateMaybe(str) {
    if (!str) return null;
    // intentar ISO o formatos comunes dd/mm/yyyy, yyyy-mm-dd
    const s = String(str).trim();
    const iso = new Date(s);
    if (!isNaN(iso)) return iso;
    const m = s.match(/^(\d{2})[\/\-](\d{2})[\/\-](\d{4})$/);
    if (m) {
      const d = new Date(Number(m[3]), Number(m[2]) - 1, Number(m[1]));
      if (!isNaN(d)) return d;
    }
    return null;
  }
  function matchesTimeFilter(it, mode, range) {
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const end = parseDateMaybe(it.fecha_cierre || it.fecha || it.deadline) || null;
    const start = parseDateMaybe(it.fecha_inicio || it.inicio) || null;
    const pivot = end || start; // fecha a usar para clasificar activa/cerrada

    if (mode === 'active') {
      if (!pivot) return true; // sin fechas: considerarlas activas
      const d = new Date(pivot); d.setHours(0, 0, 0, 0);
      return d.getTime() >= today.getTime();
    }
    if (mode === 'closed') {
      if (!pivot) return false; // sin fechas no se puede clasificar
      const d = new Date(pivot); d.setHours(0, 0, 0, 0);
      return d.getTime() < today.getTime();
    }
    // range
    const startD = start || end; // si no hay inicio, usar fin
    const endD = end || start;   // si no hay fin, usar inicio
    if (!range.start && !range.end) return true;
    const startOk = !range.start || (startD && startD <= range.end);
    const endOk = !range.end || (endD && endD >= range.start);
    return !!(startOk && endOk);
  }
  function normalizeCategory(it) {
    const t = String(it && it.tipo || '').toLowerCase();
    if (t === 'convocatoria_internacional') return 'internacional';
    if (t === 'evento') return 'evento';
    if (t === 'convocatoria_nacional') return 'nacional';
    return 'nacional';
  }
  function matchesCategory(it, cat) {
    if (!cat || cat === 'all') return true;
    return normalizeCategory(it) === cat;
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
  function escapeAttr(str) {
    // For URL attributes; basic escaping
    return String(str).replace(/"/g, '&quot;');
  }

  // Preload helper
  async function preloadImages(urls) {
    await Promise.all(
      urls.map(
        (u) =>
          new Promise((resolve) => {
            const img = new Image();
            img.onload = () => resolve(true);
            img.onerror = () => resolve(true);
            img.src = u;
          })
      )
    );
  }

  function buildTemaFromSavedOptions() {
    try {
      const raw = localStorage.getItem('topic_selection');
      if (!raw) return null;
      const sel = JSON.parse(raw);
      if (!sel || !sel.value) return null;
      if (sel.value === 'all') return null;
      if (sel.value === 'other') {
        if (sel.other && sel.other.trim()) return sel.other.trim();
        return null;
      }
      // map to human string
      const map = {
        ciencia: 'ciencia',
        tecnologia: 'tecnología',
        ia: 'inteligencia artificial',
        naval: 'naval'
      };
      return map[sel.value] || sel.value;
    } catch { return null; }
  }

  function loadSavedOptionsIntoUI() {
    try {
      const raw = localStorage.getItem('topic_selection');
      if (!raw) return;
      const sel = JSON.parse(raw);
      if (!sel) return;
      const radios = Array.from(document.querySelectorAll('input[name="topic"]'));
      const r = radios.find(x => x.value === sel.value) || radios[0];
      if (r) r.checked = true;
      if (sel.value === 'other') {
        otherTopic.disabled = false;
        otherTopic.value = sel.other || '';
      } else {
        otherTopic.disabled = true;
        otherTopic.value = '';
      }
    } catch { }
  }
  function getSelectedTopicFromUI() {
    const r = document.querySelector('input[name="topic"]:checked');
    const value = r ? r.value : 'all';
    const other = value === 'other' ? (otherTopic.value || '') : '';
    return { value, other };
  }

  function updateCartCount() {
    if (pdfCartCount) {
      pdfCartCount.textContent = String(selectedItems.size);
      pdfCartCount.classList.remove('pop');
      void pdfCartCount.offsetWidth; // reflow to restart animation
      pdfCartCount.classList.add('pop');
    }
  }

  function updatePdfCartList() {
    if (!pdfCartList) return;
    pdfCartList.innerHTML = '';
    if (selectedItems.size === 0) {
      const li = document.createElement('li');
      li.className = 'pdf-cart-list-item';
      li.style.listStyle = 'none';
      li.textContent = 'No hay convocatorias seleccionadas.';
      pdfCartList.appendChild(li);
      return;
    }
    selectedItems.forEach((title) => {
      const li = document.createElement('li');
      li.className = 'pdf-cart-list-item';
      li.textContent = title;
      pdfCartList.appendChild(li);
    });
  }

  async function refreshSources() {
    try {
      const res = await fetch(`${API_URL}/api/sources`);
      const data = res.ok ? await res.json() : [];
      buildSourcesList(data);
      const badge = document.getElementById('sourcesCount');
      if (badge) {
        badge.textContent = String(data.length);
        badge.classList.remove('pop');
        // trigger reflow to restart animation
        void badge.offsetWidth;
        badge.classList.add('pop');
      }
    } catch {
      buildSourcesList([]);
    }
  }
  function buildSourcesList(items) {
    if (!sourcesList) return;
    sourcesList.innerHTML = '';
    items.forEach((s) => {
      const row = document.createElement('div');
      row.className = 'source-item';
      row.innerHTML = `
        <div>
          <div><strong>${escapeHtml(s.name || '')}</strong> <small>(${s.hidden ? 'Oculta' : 'Visible'})</small></div>
          <small>${escapeHtml(s.type || '')}</small><br/>
          <small>${escapeHtml(s.url || '')}</small>
        </div>
        <div>
          <button class="icon-btn toggle-btn" title="${s.hidden ? 'Mostrar' : 'Ocultar'}"><i class="fa-solid ${s.hidden ? 'fa-eye-slash' : 'fa-eye'}"></i></button>
          <button class="icon-btn edit-btn" title="Editar"><i class="fa-solid fa-pencil"></i></button>
          <button class="icon-btn delete-btn" title="Eliminar"><i class="fa-solid fa-trash"></i></button>
        </div>
      `;
      const toggleBtn = row.querySelector('.toggle-btn');
      toggleBtn.addEventListener('click', async () => {
        await fetch(`${API_URL}/api/sources/${s.id}/toggle`, { method: 'PATCH' });
        await refreshSources();
      });
      const editBtn = row.querySelector('.edit-btn');
      editBtn.addEventListener('click', async () => {
        const name = prompt('Nombre', s.name || '') || s.name;
        const type = prompt('Tipo', s.type || '') || s.type;
        const url = prompt('URL', s.url || '') || s.url;
        await fetch(`${API_URL}/api/sources/${s.id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, type, url }) });
        await refreshSources();
      });
      const deleteBtn = row.querySelector('.delete-btn');
      deleteBtn.addEventListener('click', async () => {
        if (confirm(`¿Seguro que quieres eliminar la fuente "${s.name}"?`)) {
          await fetch(`${API_URL}/api/sources/${s.id}`, { method: 'DELETE' });
          await refreshSources();
        }
      });
      sourcesList.appendChild(row);
    });
  }
});
