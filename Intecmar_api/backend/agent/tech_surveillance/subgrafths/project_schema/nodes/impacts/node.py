from __future__ import annotations

import os 
import time

from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from backend.agent.tech_surveillance.state import GraphState, ReportSchema, Impacts

# Importamos los prompts 
from .prompts import IMPACTS_PROMPT
from ...prompts import SHARED_CONTEXT_HEADER


# --- Inicialización del LLM (sin cambios) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

def generate_impacts(state: GraphState) -> dict:
    """
    Nodo 6: Genera los Resultados e Impactos Esperados usando Structured Output.
    """
    print("---SUBGRAPH: Generando Impactos (Structured)---")
    
    # Debug API Key
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ ERROR: GEMINI_API_KEY no encontrada.")
    # 1. Leer de forma segura el estado actual
    report_components = state.get("report_components") or ReportSchema()
    
    # --- LÓGICA DE REGENERACIÓN SELECTIVA ---
    config = state.get("generation_config")
    if isinstance(config, dict):
        try:
            from backend.agent.tech_surveillance.state import GenerationConfig
            config = GenerationConfig(**config)
        except:
            pass
    
    sections_to_regen = getattr(config, "sections_to_regenerate", []) or []
    
    # Si la sección ya existe y no está marcada para regenerar, saltar
    if report_components.results_and_impacts and "impacts" not in sections_to_regen:
        print("⏭️ SKIP: Impactos ya existe y no fue seleccionada para regenerar.")
        return {
            "report_components": report_components,
            "messages": [AIMessage(content="Omitiendo generación de Impactos (contenido persistente).")]
        }

    project_title = "No especificado"
    if report_components.general_info:
        project_title = report_components.general_info.project_title or "No especificado"
        
    general_objective = ""
    specific_objectives = ""
    if report_components.objectives:
        general_objective = report_components.objectives.general_objective or ""
        specific_objectives = report_components.objectives.specific_objectives_smart or ""

    # 2. Formatear el prompt
    initial_schema = state.get("initial_schema") or "No se encontró el esquema inicial."
    
    # Extract config values
    char_limit = getattr(config, "charLimit", 2500) if config else 2500
    section_limits = getattr(config, "section_char_limits", {}) or {}
    char_limit = section_limits.get("impacts", char_limit)
    
    ref_style = getattr(config, "refStyle", "APA") if config else "APA"
    
    header_prompt = SHARED_CONTEXT_HEADER.format(
        initial_schema=initial_schema
    )
    prompt = IMPACTS_PROMPT.format(
        project_title=project_title,
        general_objective=general_objective,
        specific_objectives_smart=specific_objectives,
        char_limit=char_limit,
        ref_style=ref_style
    )

    # 3. Configurar el LLM para salida estructurada
    structured_llm = llm.with_structured_output(Impacts)

    # 4. Invocar al LLM con Reintentos
    full_prompt = header_prompt + "\n" + prompt
    
    impacts_schema = None
    max_retries = 3
    for attempt in range(max_retries):
        try:
            impacts_schema = structured_llm.invoke(full_prompt)
            if impacts_schema: break
        except Exception as e:
            print(f"⚠️ Intento {attempt+1} fallido en Impactos: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise e

    # 5. Actualizar el esquema del reporte en el estado
    report_components.results_and_impacts = impacts_schema
    
    # 6. Mensaje de confirmación
    message = AIMessage(content="Sección de resultados e impactos generada (Estructurado). Procediendo a crear el resumen ejecutivo final.")
    
    print("--- Resultados e impactos generados y guardados en el estado. ---")

    # 7. Devolver el estado actualizado
    return {
        "report_components": report_components,
        "messages": [message]
    }