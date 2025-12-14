// frontend/js/savedMagazines.js
// Panel de filtros para Magazines Guardados (periodo de tiempo + categoría)

document.addEventListener("DOMContentLoaded", () => {
  const showBtn = document.getElementById("showSavedBtn");
  const savedSection = document.getElementById("savedMagazines");
  const convocatoriasContainer = document.getElementById('convocatorias-container');
  const API_URL = document.body?.dataset?.api || window.location.origin;

  // Botones del nuevo panel de filtros
  // (Delegado a main.js: se encarga de time filters y category filters)

  if (!showBtn || !savedSection || !convocatoriasContainer) return;

  // Función para actualizar el texto del botón
  function updateButtonText() {
    const isHidden = savedSection.classList.contains("hidden");
    showBtn.textContent = isHidden ? 'Ver Convocatorias Guardadas' : 'Ocultar Convocatorias Guardadas';
  }

  // Inicializar el texto del botón
  updateButtonText();

  showBtn.addEventListener("click", async () => {
    // Toggle de panel
    if (!savedSection.classList.contains("hidden")) {
      savedSection.classList.add("hidden");
      convocatoriasContainer.innerHTML = '';
      updateButtonText();
      return;
    }

    savedSection.classList.remove("hidden");
    updateButtonText();
    try { savedSection.scrollIntoView({ behavior: 'smooth', block: 'start' }); } catch {}

    // Carga de JSON (con fallback)
    let lastAttemptUrl = '';
    let lastStatus = '';
    try {
      const urlPrimary = `${API_URL}/outputs/convocatorias.json?t=${Date.now()}`;
      lastAttemptUrl = urlPrimary;
      let res = await fetch(urlPrimary);
      if (!res.ok) {
        lastStatus = `HTTP ${res.status}`;
        const urlFallback = `${window.location.origin}/outputs/convocatorias.json?t=${Date.now()}`;
        lastAttemptUrl = urlFallback;
        const res2 = window.location.origin.startsWith('http') ? await fetch(urlFallback) : { ok: false, status: 'origen no http' };
        if (res2.ok) res = res2; else {
          const urlRelative = `outputs/convocatorias.json?t=${Date.now()}`;
          lastAttemptUrl = urlRelative;
          const res3 = await fetch(urlRelative);
          if (res3.ok) res = res3; else {
            lastStatus = `${lastStatus} / ${res2.status} / HTTP ${res3.status}`;
            throw new Error('Fallo al cargar JSON con primario, fallback y relativo');
          }
        }
      }
      const data = await res.json();
      const mapped = mapSavedToCards(data);
      if (typeof window.renderConvocatorias === 'function') {
        window.renderConvocatorias(mapped);
      }
    } catch (e) {
      const baseMsg = e && e.message ? e.message : String(e);
      const msg = `${lastStatus || 'Error de red'} en ${lastAttemptUrl} :: ${baseMsg}`;
      if (convocatoriasContainer) convocatoriasContainer.innerHTML = `<p style="color:#b91c1c">No fue posible cargar las convocatorias guardadas. Detalle: ${escapeHtml(msg)}</p>`;
    }
  });

  function mapSavedToCards(items) {
    return (Array.isArray(items) ? items : []).map((it) => ({
      id: it.id,
      tipo: it.type || 'general',
      titulo: it.title || 'Sin título',
      descripcion: it.description || '',
      objetivo: it.description || '',
      beneficios: it.beneficios || 'No especificado',
      dirigido_a: (it.keywords || []).join(', '),
      fecha_inicio: it.fecha_inicio || it.inicio || '',
      fecha_cierre: it.fecha_cierre || it.deadline || 'No especificado',
      fecha: it.fecha || '',
      lugar: it.lugar || '',
      monto: it.monto || it.monto_financiacion || it.financiacion || '',
      keywords: it.keywords || it.palabras_clave || it.tags || [],
      url_original: it.url || it.source || '',
      created_at: it.created_at || new Date().toISOString(),
    }));
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
});
