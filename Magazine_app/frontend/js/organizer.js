// frontend/js/organizer.js
// Ordena las tarjetas .call-card dentro de #convocatorias-container
// en el orden: nacional -> internacional -> evento

document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector("#convocatorias-container");
  if (!container) return;

  const cards = Array.from(container.querySelectorAll(".call-card"));
  if (cards.length === 0) return;

  const categorias = {
    nacional: [],
    internacional: [],
    evento: []
  };

  cards.forEach((card) => {
    const tipo = card.getAttribute("data-tipo") || "";
    if (tipo === "convocatoria_nacional") categorias.nacional.push(card);
    else if (tipo === "convocatoria_internacional") categorias.internacional.push(card);
    else if (tipo === "evento") categorias.evento.push(card);
  });

  container.innerHTML = "";
  ["nacional", "internacional", "evento"].forEach((cat) => {
    categorias[cat].forEach((c) => container.appendChild(c));
  });
});
