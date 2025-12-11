from __future__ import annotations

import os 
import time
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from src.agents.tech_surveillance.state import GraphState, ReportSchema, Justification
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
    time.sleep(10) 
    
    # 1. Leer de forma segura el estado actual
    report_components = state.get("report_components") or ReportSchema()
    
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
    header_prompt = SHARED_CONTEXT_HEADER.format(
        initial_schema=initial_schema
    )
    prompt = JUSTIFICATION_PROMPT.format(
        project_title=project_title,
        project_description=project_description,
        theoretical_framework_body=framework_body
    )

    # 3. Configurar el LLM para salida estructurada
    structured_llm = llm.with_structured_output(Justification)

    # 4. Invocar al LLM
    full_prompt = header_prompt + "\n" + prompt
    justification_schema = structured_llm.invoke(full_prompt)

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