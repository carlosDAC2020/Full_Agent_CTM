import os
import asyncio
from typing import Dict, Any, List

# Importar el agente (preferir ruta absoluta del paquete backend)
try:
    from Intecmar_api.backend.agent.magazine.graph import app as agent_app
    from Intecmar_api.backend.agent.magazine.nodes import llm as agent_llm
except Exception:
    try:
        from Intecmar_api.backend.agent.magazine.graph import workflow
        agent_app = workflow.compile()
        from Intecmar_api.backend.agent.magazine.nodes import llm as agent_llm
    except Exception:
        # Fallback para entornos donde `backend` no está como paquete
        try:
            from Intecmar_api.backend.agent.magazine.graph import workflow  # type: ignore
            agent_app = workflow.compile()  # type: ignore
            from Intecmar_api.backend.agent.magazine.nodes import llm as agent_llm
        except Exception:
            agent_app = None
            agent_llm = None

# Utilidades de búsqueda web para fuentes
try:
    from Intecmar_api.backend.agent.magazine.tools import search_all as web_search_all  # type: ignore
except Exception:
    try:
        from Intecmar_api.backend.agent.magazine.tools import search_all as web_search_all  # type: ignore
    except Exception:
        web_search_all = None

async def run_magazine_generation_stream(tema: str):
    """Ejecuta el agente y devuelve el resultado final (PDF path y contenido)."""
    if not agent_app:
        raise RuntimeError("El agente no está disponible")
    
    inputs = {"tema": tema}
    result = {}
    
    # El agente es síncrono o asíncrono? LangGraph .stream suele ser sync iterator o async iterator depending on config.
    # main_api.py usage: for output in agent_app.stream(inputs):
    # This implies sync iterator.
    
    for output in agent_app.stream(inputs):
        for key, value in output.items():
            if key in ['contenido_curado', 'pdf_path']:
                result[key] = value
    return result

def llm_invoke(prompt: str) -> str:
    if agent_llm:
        return agent_llm.invoke(prompt).content
    return ""

def search_web(query: str, tavily_max=2, brave_max=1) -> List[Dict[str, Any]]:
    if web_search_all:
        try:
            return web_search_all(query, tavily_max=tavily_max, brave_max=brave_max) or []
        except Exception:
            return []
    return []
