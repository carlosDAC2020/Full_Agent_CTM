from __future__ import annotations

import os 
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from src.agents.tech_surveillance.state import GraphState, ReportSchema, ProjectObjectives
# Importamos los prompts 
from .prompts import SMART_OBJECTIVES_PROMPT
from ...prompts import SHARED_CONTEXT_HEADER

# --- Inicialización del LLM (sin cambios) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

def generate_objectives(state: GraphState) -> dict:
    """
    Nodo 2: Genera los Objetivos del Proyecto usando Structured Output.
    """
    print("---SUBGRAPH: Generando Objetivos (Structured)---")

    # 1. Leer de forma segura el estado actual
    report_components = state.get("report_components") or ReportSchema()
    
    project_title = "No especificado"
    if report_components.general_info:
        project_title = report_components.general_info.project_title or "No especificado"
    
    # La entrada clave: la justificación del nodo anterior
    justification = report_components.problem_statement_justification or "No hay justificación disponible."

    # 2. Formatear el prompt
    initial_schema = state.get("initial_schema") or "No se encontró el esquema inicial."
    header_prompt = SHARED_CONTEXT_HEADER.format(
        initial_schema=initial_schema
    )
    prompt = SMART_OBJECTIVES_PROMPT.format(
        project_title=project_title,
        problem_statement_justification=justification
    )

    # 3. Configurar el LLM para salida estructurada
    structured_llm = llm.with_structured_output(ProjectObjectives)

    # 4. Invocar al LLM
    # El resultado ya será una instancia de ProjectObjectives
    full_prompt = header_prompt + "\n" + prompt
    objectives_schema = structured_llm.invoke(full_prompt)

    # 5. Actualizar el esquema del reporte en el estado
    report_components.objectives = objectives_schema
    
    # 6. Mensaje de confirmación
    message = AIMessage(content="Objetivos del proyecto generados (Estructurado). Procediendo a definir la metodología.")
    
    print("--- Objetivos generados y guardados en el estado. ---")

    # 7. Devolver el estado actualizado
    return {
        "report_components": report_components,
        "messages": [message]
    }