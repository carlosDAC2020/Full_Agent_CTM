from __future__ import annotations

import os 
import time
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from backend.agent.tech_surveillance.state import GraphState, ReportSchema, Justification
# Importamos los prompts (que también modificaremos)
from .prompts import JUSTIFICATION_PROMPT
from ...prompts import SHARED_CONTEXT_HEADER

# --- Inicialización del LLM (sin cambios) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

# --- Implementación de los Nodos del Subgrafo (MODIFICADOS) ---

def generate_justification(state: GraphState) -> dict:
    """
    Nodo 1: Genera el Planteamiento del Problema y Justificación usando Structured Output.
    """
    print("---SUBGRAPH: Generando Justificación (Structured)---")
    
    # Debug API Key (without printing it)
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ ERROR: GEMINI_API_KEY no encontrada en el entorno del worker.")
    
    
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
    if report_components.problem_statement_justification and "justification" not in sections_to_regen:
        print("⏭️ SKIP: Justificación ya existe y no fue seleccionada para regenerar.")
        return {
            "report_components": report_components,
            "messages": [AIMessage(content="Omitiendo generación de Justificación (contenido persistente).")]
        }

    # Safe access to nested Pydantic models
    project_title = "No especificado"
    project_description = "No especificado"
    
    if report_components.general_info:
        project_title = report_components.general_info.project_title or "No especificado"
        project_description = report_components.general_info.project_description or "No especificado"

    framework_body = "No se encontró marco teórico."
    if report_components.theoretical_framework:
        framework_body = report_components.theoretical_framework.body or "No se encontró marco teórico."

    # 2. Formatear el prompt con la información extraída
    initial_schema = state.get("initial_schema") or "No se encontró el esquema inicial."
    
    # Extract config values
    char_limit = getattr(config, "charLimit", 2500) if config else 2500
    section_limits = getattr(config, "section_char_limits", {}) or {}
    char_limit = section_limits.get("justification", char_limit)
    
    ref_style = getattr(config, "refStyle", "APA") if config else "APA"

    header_prompt = SHARED_CONTEXT_HEADER.format(
        initial_schema=initial_schema
    )
    prompt = JUSTIFICATION_PROMPT.format(
        project_title=project_title,
        project_description=project_description,
        theoretical_framework_body=framework_body,
        char_limit=char_limit,
        ref_style=ref_style
    )

    # 3. Configurar el LLM para salida estructurada
    structured_llm = llm.with_structured_output(Justification)

    # 4. Invocar al LLM con Reintentos
    full_prompt = header_prompt + "\n" + prompt
    
    justification_schema = None
    max_retries = 3
    for attempt in range(max_retries):
        try:
            justification_schema = structured_llm.invoke(full_prompt)
            if justification_schema: break
        except Exception as e:
            print(f"⚠️ Intento {attempt+1} fallido en Justificación: {e}")
            if attempt < max_retries - 1:
                time.sleep(2) # Breve espera antes de reintentar
            else:
                raise e

    # 5. Actualizar el esquema del reporte en el estado
    report_components.problem_statement_justification = justification_schema
    
    # 6. Mensaje de confirmación para el historial
    message = AIMessage(content="Justificación del proyecto generada (Estructurado). Procediendo a definir los objetivos.")
    
    print("--- Justificación generada y guardada en el estado. ---")

    # 7. Devolver el estado actualizado
    return {
        "report_components": report_components,
        "messages": [message]
    }