from ..state import AgentState
from .common import llm
from ..prompts.curation_prompts import build_curation_prompt


def nodo_curacion(state: AgentState) -> AgentState:
    print("--- ✍️ CURANDO Y REDACTANDO ---")
    convocatorias_curadas = []
    for datos in state.get('datos_extraidos', []):
        prompt = build_curation_prompt(datos)

        try:
            resumen = llm.invoke(prompt).content
        except Exception:
            resumen = "Resumen no disponible."

        datos_enriquecidos = dict(datos)
        datos_enriquecidos['resumen_magazine'] = resumen
        convocatorias_curadas.append(datos_enriquecidos)

    return {"contenido_curado": convocatorias_curadas}
