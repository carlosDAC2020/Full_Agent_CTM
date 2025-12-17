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

    // Carga desde API: GET /convocatorias
    try {
      const url = `${API_URL}/convocatorias`;
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      const data = await res.json();
      const mapped = mapSavedToCards(data);
      if (typeof window.renderConvocatorias === 'function') {
        window.renderConvocatorias(mapped);
      }
    } catch (e) {
      const msg = e && e.message ? e.message : String(e);
      if (convocatoriasContainer) {
        convocatoriasContainer.innerHTML = `<p style="color:#b91c1c">No fue posible cargar las convocatorias guardadas desde la base de datos. Detalle: ${escapeHtml(msg)}</p>`;
      }
    }
  });

  function mapSavedToCards(items) {
    // items viene del endpoint /magazines/convocatorias (ConvocatoriaOut)
    return (Array.isArray(items) ? items : []).map((it) => ({
      id: it.id,
      tipo: it.type || 'general',
      titulo: it.title || 'Sin título',
      descripcion: it.description || '',
      objetivo: it.description || '',
      beneficios: it.beneficios || 'No especificado',
      dirigido_a: Array.isArray(it.keywords) ? it.keywords.join(', ') : '',
      fecha_inicio: it.fecha_inicio || '',
      fecha_cierre: it.fecha_cierre || it.deadline || 'No especificado',
      fecha: it.created_at || '',
      lugar: it.lugar || '',
      monto: it.monto || '',
      keywords: it.keywords || [],
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
