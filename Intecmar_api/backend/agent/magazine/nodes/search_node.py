from ..state import AgentState
import requests
from backend.app.core.config import settings


def nodo_busqueda(state: AgentState) -> AgentState:
    print("--- 🔍 BUSCANDO EN FUENTES INSTITUCIONALES (Jina Reader) ---")
    resultados = []

    urls = state.get("consultas_busqueda", []) or []
    if not settings.JINA_API_KEY:
        print("⚠️ JINA_API_KEY no está configurada; no se puede usar Jina Reader.")
        return {"resultados_busqueda": resultados}

    for i, url in enumerate(urls):
        print(f"Consultando Jina Reader para fuente ({i+1}/{len(urls)}): {url}")
        try:
            jina_url = f"https://r.jina.ai/{url}"
            headers = {
                "Authorization": f"Bearer {settings.JINA_API_KEY}",
                "X-Retain-Images": "none",
                "Accept": "text/plain",
            }
            resp = requests.get(jina_url, timeout=30, headers=headers)
            resp.raise_for_status()

            resultados.append({
                "url": url,
                "title": "Extraído vía Jina",
                "content": resp.text,
            })
        except Exception as e:
            print(f"  -> Error accediendo a {url} vía Jina: {e}")

    return {"resultados_busqueda": resultados}
