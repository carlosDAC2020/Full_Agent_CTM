# backend/agent/tools.py
import os
import requests
from langchain_community.tools.tavily_search import TavilySearchResults

# Por ahora, solo usaremos Tavily. Es muy potente.
# max_results=2 significa que por cada consulta, obtendremos 2 resultado.
tavily_tool = TavilySearchResults(max_results=2)

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

def brave_search(query: str, count: int = 2):
    """
    Realiza una búsqueda web usando Brave Search API y devuelve una lista de resultados
    con el formato: [{"url": str, "title": str, "content": str}]
    """
    if not BRAVE_API_KEY:
        return []
    try:
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {"X-Subscription-Token": BRAVE_API_KEY}
        params = {"q": query, "count": count, "source": "web"}
        resp = requests.get(url, headers=headers, params=params, timeout=12)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("web", {}).get("results", [])[:count]:
            results.append({
                "url": item.get("url"),
                "title": item.get("title") or item.get("url"),
                "content": item.get("description") or ""
            })
        return [r for r in results if r.get("url")]
    except Exception:
        return []

def search_all(query: str, tavily_max: int = 2, brave_max: int = 2):
    """Combina resultados de Tavily y Brave, deduplicando por URL."""
    out = []
    # Tavily
    try:
        tavily = TavilySearchResults(max_results=tavily_max)
        out.extend(tavily.invoke(query))
    except Exception:
        out.extend([])
    # Brave
    out.extend(brave_search(query, count=brave_max))

    # Dedupe por URL
    seen = set()
    deduped = []
    for r in out:
        url = r.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        deduped.append(r)
    return deduped

# Lista de herramientas que nuestro agente conocerá (se mantiene por compatibilidad).
tools = [tavily_tool]
