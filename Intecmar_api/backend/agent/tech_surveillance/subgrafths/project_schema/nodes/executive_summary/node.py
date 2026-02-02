from __future__ import annotations

import os 
import time
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from backend.agent.tech_surveillance.state import GraphState, ReportSchema, ExecutiveSummary
# Importamos los prompts 
from .prompts import EXECUTIVE_SUMMARY_PROMPT
from ...prompts import SHARED_CONTEXT_HEADER

# --- Inicialización del LLM (sin cambios) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

def generate_executive_summary(state: GraphState) -> dict:
    """
    Nodo 7 (Final): Genera el Resumen Ejecutivo usando Structured Output.
    """
    print("---SUBGRAPH: Generando Resumen Ejecutivo (Structured)---")
    
    # Debug API Key
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ ERROR: GEMINI_API_KEY no encontrada.")
    
    # 1. Leer TODAS las secciones generadas hasta ahora
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
    if report_components.executive_summary and "executive_summary" not in sections_to_regen:
        print("⏭️ SKIP: Resumen Ejecutivo ya existe y no fue seleccionado para regenerar.")
        return {
            "report_components": report_components,
            "messages": [AIMessage(content="Omitiendo generación de Resumen Ejecutivo (contenido persistente).")]
        }

    project_title = "No especificado"
    if report_components.general_info:
        project_title = report_components.general_info.project_title or "No especificado"
        
    methodology = "N/A"
    if report_components.methodology:
        methodology = report_components.methodology.content or "N/A"
        
    justification = "N/A"
    if report_components.problem_statement_justification:
        ps = report_components.problem_statement_justification.problem_statement or ""
        j = report_components.problem_statement_justification.justification or ""
        justification = f"Planteamiento: {ps}\nJustificación: {j}"
        
    impacts = "N/A"
    if report_components.results_and_impacts:
        impacts = report_components.results_and_impacts.content or "N/A"
    
    general_obj = "N/A"
    specific_objs = "N/A"
    if report_components.objectives:
        general_obj = report_components.objectives.general_objective or "N/A"
        specific_objs = report_components.objectives.specific_objectives_smart or "N/A"
        
    # Concatenar objetivos para pasarlos como un solo bloque de texto
    objectives_text = f"General: {general_obj}\n\nSpecifics:\n{specific_objs}"

    initial_schema = state.get("initial_schema") or "No se encontró el esquema inicial."
    
    # Extract config values
    char_limit = getattr(config, "charLimit", 2500) if config else 2500
    section_limits = getattr(config, "section_char_limits", {}) or {}
    char_limit = section_limits.get("executive_summary", char_limit)
    
    header_prompt = SHARED_CONTEXT_HEADER.format(
        initial_schema=initial_schema
    )
    # 2. Formatear el prompt con el contexto completo
    prompt = EXECUTIVE_SUMMARY_PROMPT.format(
        project_title=project_title,
        problem_statement_justification=justification,
        objectives=objectives_text,
        methodology=methodology,
        results_and_impacts=impacts,
        char_limit=char_limit
    )

    # 3. Configurar el LLM para salida estructurada
    structured_llm = llm.with_structured_output(ExecutiveSummary)

    # 4. Invocar al LLM con Reintentos
    full_prompt = header_prompt + "\n" + prompt
    
    summary_schema = None
    max_retries = 3
    for attempt in range(max_retries):
        try:
            summary_schema = structured_llm.invoke(full_prompt)
            if summary_schema: break
        except Exception as e:
            print(f"⚠️ Intento {attempt+1} fallido en Resumen: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise e

    # 5. Actualizar el esquema del reporte en el estado
    report_components.executive_summary = summary_schema
    
    # 6. Mensaje de confirmación
    message = AIMessage(content="Resumen ejecutivo generado (Estructurado). El contenido del reporte está completo.")
    
    print("--- Resumen ejecutivo generado. Subgrafo de contenido completado. ---")

    # 7. Devolver el estado actualizado
    return {
        "report_components": report_components,
        "messages": [message]
    }
