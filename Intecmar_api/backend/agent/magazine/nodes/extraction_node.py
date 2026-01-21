import json
import re

import requests
from bs4 import BeautifulSoup

from ..state import AgentState
from .common import llm
from ..prompts.extraction_prompts import build_extraction_prompt


def nodo_extraccion(state: AgentState) -> AgentState:
    print("--- 🔬 EXtrayendo Y CLASIFICANDO ---")

    resultados = state.get("resultados_busqueda", []) or []
    datos_extraidos = []

    # Añadimos headers para parecer un navegador real y evitar bloqueos
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
    for i, item in enumerate(resultados):
        url = item.get('url')
        print(f"Procesando resultado ({i+1}/{len(resultados)}): {url}")

        # Intentar usar el contenido ya descargado del nodo de búsqueda
        texto_limpio = ''
        raw_content = (item.get('content') or '').strip()
        if raw_content:
            texto_limpio = ' '.join(raw_content.split())[:10000]
        else:
            # Fallback: si no hay contenido, hacemos una petición HTTP
            try:
                resp = requests.get(url, timeout=15, headers=headers, verify=False)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.content, 'html.parser')
                texto_web = soup.get_text(separator=' ')
                texto_limpio = ' '.join(texto_web.split())[:10000]
            except requests.RequestException as e:
                print(f"  -> Error: No se pudo acceder a la URL. {e}")
                continue

        # Si aún así no tenemos texto, pasamos al siguiente
        if not texto_limpio:
            print("  -> Aviso: contenido vacío, se omite este resultado.")
            continue

        # --- PROMPT MEJORADO Y CLASIFICACIÓN ---
        prompt = build_extraction_prompt(texto_limpio)

        # Llamar al LLM y obtener la respuesta de texto
        respuesta_llm = llm.invoke(prompt).content

        # --- PARSEO DE JSON MÁS ROBUSTO ---
        # A veces el LLM envuelve el JSON con texto. Intentamos extraerlo.
        match = re.search(r'\{.*\}', respuesta_llm, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                info_json = json.loads(json_str)
                if isinstance(info_json, dict) and "error" not in info_json:
                    info_json['url_original'] = url
                    datos_extraidos.append(info_json)
                    print(f"  -> Éxito: '{info_json.get('titulo', 'Sin título')}'")
            except json.JSONDecodeError:
                print(f"  -> Error: Se encontró un JSON, pero es inválido.")
        else:
            print(f"  -> Error: No se encontró ningún objeto JSON en la respuesta del LLM.")

    return {"datos_extraidos": datos_extraidos}
