import json
import re

import requests
from bs4 import BeautifulSoup

from ..state import AgentState
from .common import llm
from ..prompts.extraction_prompts import build_extraction_prompt


def nodo_extraccion(state: AgentState) -> AgentState:
    print("--- 🔬 EXtrayendo Y CLASIFICANDO ---")

    urls_a_visitar = [res['url'] for res in state['resultados_busqueda']]
    datos_extraidos = []

    # Añadimos un User-Agent para parecer un navegador real y evitar bloqueos
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    for i, url in enumerate(urls_a_visitar):
        print(f"Procesando URL ({i+1}/{len(urls_a_visitar)}): {url}")
        try:
            resp = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'html.parser')
            texto_web = soup.get_text(separator=' ')
            texto_limpio = ' '.join(texto_web.split())[:10000]

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

        except requests.RequestException as e:
            print(f"  -> Error: No se pudo acceder a la URL. {e}")
    return {"datos_extraidos": datos_extraidos}
