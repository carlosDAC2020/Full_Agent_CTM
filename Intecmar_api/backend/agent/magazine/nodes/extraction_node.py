import json
import re

from ..state import AgentState
from .common import llm
from ..prompts.extraction_prompts import build_extraction_prompt


def nodo_extraccion(state: AgentState) -> AgentState:
    print("--- 🔬 EXtrayendo Y CLASIFICANDO ---")

    resultados = state.get("resultados_busqueda", []) or []
    datos_extraidos = []

    for i, item in enumerate(resultados):
        url = item.get('url')
        print(f"Procesando resultado ({i+1}/{len(resultados)}): {url}")

        raw_content = (item.get('content') or '').strip()
        if not raw_content:
            print("  -> Aviso: contenido vacío desde Jina, se omite este resultado.")
            continue

        # El contenido ya viene en texto/Markdown desde Jina; solo normalizamos tamaño
        texto_limpio = ' '.join(raw_content.split())[:10000]

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
