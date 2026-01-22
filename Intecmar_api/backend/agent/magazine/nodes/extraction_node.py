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
        texto_limpio = ' '.join(raw_content.split())[:50000]
        print(f"DEBUG INPUT TEXT (First 500 chars): {texto_limpio[:500]}...")
        print(f"DEBUG INPUT LENGTH: {len(texto_limpio)} chars")

        # --- PROMPT MEJORADO Y CLASIFICACIÓN ---
        prompt = build_extraction_prompt(texto_limpio)

        # Llamar al LLM y obtener la respuesta de texto
        respuesta_llm = llm.invoke(prompt).content
        print(f"DEBUG LLM RAW: {respuesta_llm[:200]}...")

        # --- PARSEO DE JSON MÁS ROBUSTO ---
        # Limpieza de fences Markdown (```json ... ```)
        clean_resp = respuesta_llm.replace('```json', '').replace('```', '').strip()

        # Intentar primero extraer una LISTA JSON de objetos
        match = re.search(r'\[.*\]', clean_resp, re.DOTALL)
        parsed_list = []

        if match:
            json_str = match.group(0)
            try:
                parsed = json.loads(json_str)
                if isinstance(parsed, dict):
                    parsed_list = [parsed]
                elif isinstance(parsed, list):
                    parsed_list = parsed
            except json.JSONDecodeError:
                print(f"  -> Error: Se encontró una lista JSON, pero es inválida.")
        else:
            # Fallback: buscar un objeto único { ... }
            obj_match = re.search(r'\{.*\}', clean_resp, re.DOTALL)
            if obj_match:
                json_str = obj_match.group(0)
                try:
                    parsed = json.loads(json_str)
                    if isinstance(parsed, dict):
                        # Si el dict contiene alguna lista de convocatorias, intentar extraerla
                        # Primero, si parece ya una convocatoria individual
                        if any(k in parsed for k in ["titulo", "tipo", "fecha_cierre", "deadline"]):
                            parsed_list = [parsed]
                        else:
                            for v in parsed.values():
                                if isinstance(v, list):
                                    parsed_list = v
                                    break
                    elif isinstance(parsed, list):
                        parsed_list = parsed
                except json.JSONDecodeError:
                    print(f"  -> Error: Se encontró un objeto JSON, pero es inválido.")

        if parsed_list:
            for info_json in parsed_list:
                if isinstance(info_json, dict) and "error" not in info_json:
                    info_json['url_original'] = url
                    datos_extraidos.append(info_json)
                    print(f"  -> Éxito: '{info_json.get('titulo', 'Sin título')}'")
        else:
            print(f"  -> Error: No se pudo extraer ninguna convocatoria en formato JSON válido.")

    return {"datos_extraidos": datos_extraidos}
