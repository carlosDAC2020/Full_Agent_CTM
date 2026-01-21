from ..state import AgentState
from .common import _load_institutional_sources_db, INSTITUTIONAL_SOURCES
from ..tools import search_all


def nodo_busqueda(state: AgentState) -> AgentState:
    print("--- 🔍 BUSCANDO EN LA WEB ---")
    resultados = []
    for query in state['consultas_busqueda']:
        print(f"Buscando: {query}")
        # Combinar Tavily + Brave, deduplicado
        combinados = search_all(query, tavily_max=1, brave_max=1)
        resultados.extend(combinados)
    # Añadir fuentes institucionales como semillas (dinámicas desde BD)
    dynamic_sources = _load_institutional_sources_db() or INSTITUTIONAL_SOURCES
    for src in dynamic_sources:
        resultados.append({
            "url": src["url"],
            "title": src["name"],
            "content": ""
        })
    return {"resultados_busqueda": resultados}
