from ..state import AgentState
from .common import _load_institutional_sources_db


def nodo_planificador(state: AgentState) -> AgentState:
    print("--- 🧠 PLANIFICANDO (FUENTES INSTITUCIONALES) ---")
    fuentes = _load_institutional_sources_db() or []
    urls = [str(f["url"]) for f in fuentes if f.get("url")]
    return {
        "plan": f"Búsqueda dirigida en {len(urls)} fuentes institucionales.",
        "consultas_busqueda": urls,
    }
