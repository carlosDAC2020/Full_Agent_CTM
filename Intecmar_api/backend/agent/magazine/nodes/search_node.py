from ..state import AgentState
import requests
from bs4 import BeautifulSoup
import urllib3


# Deshabilitar warnings de certificados inseguros (sitios gubernamentales con SSL viejo)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def nodo_busqueda(state: AgentState) -> AgentState:
    print("--- 🔍 BUSCANDO EN FUENTES INSTITUCIONALES ---")
    resultados = []

    urls = state.get("consultas_busqueda", []) or []
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    for i, url in enumerate(urls):
        print(f"Visitando fuente institucional ({i+1}/{len(urls)}): {url}")
        try:
            resp = requests.get(url, timeout=20, headers=headers, verify=False)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, "html.parser")

            body = soup.body or soup
            texto = body.get_text(separator=" ") if body else soup.get_text(separator=" ")
            texto_limpio = " ".join(texto.split())

            resultados.append({
                "url": url,
                "title": soup.title.string.strip() if soup.title and soup.title.string else url,
                "content": texto_limpio,
            })
        except Exception as e:
            print(f"  -> Error accediendo a {url}: {e}")

    return {"resultados_busqueda": resultados}
