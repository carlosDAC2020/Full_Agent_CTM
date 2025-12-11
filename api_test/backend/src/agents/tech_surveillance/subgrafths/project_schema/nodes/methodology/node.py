from __future__ import annotations

import os 
import time

from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from src.agents.tech_surveillance.state import GraphState, ReportSchema, Methodology

# Importamos los prompts 
from .prompts import METHODOLOGY_PROMPT
from ...prompts import SHARED_CONTEXT_HEADER


# --- Inicialización del LLM (sin cambios) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

def generate_methodology(state: GraphState) -> dict:
    """
    Nodo 3: Genera la Metodología Propuesta usando Structured Output.
    """
    print("---SUBGRAPH: Generando Metodología (Structured)---")
    time.sleep(10) 
    
    # 1. Leer de forma segura el estado actual
    report_components = state.get("report_components") or ReportSchema()
    
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
    header_prompt = SHARED_CONTEXT_HEADER.format(
        initial_schema=initial_schema
    )
    prompt = METHODOLOGY_PROMPT.format(
        project_title=project_title,
        general_objective=general_objective,
        specific_objectives_smart=specific_objectives
    )

    # 3. Configurar el LLM para salida estructurada
    structured_llm = llm.with_structured_output(Methodology)

    # 4. Invocar al LLM
    full_prompt = header_prompt + "\n" + prompt
    methodology_schema = structured_llm.invoke(full_prompt)

    # 5. Actualizar el esquema del reporte en el estado
    report_components.methodology = methodology_schema
    
    # 6. Mensaje de confirmación
    message = AIMessage(content="Metodología del proyecto definida (Estructurado). Procediendo a crear el cronograma de actividades.")
    
    print("--- Metodología generada y guardada en el estado. ---")

    # 7. Devolver el estado actualizado
    return {
        "report_components": report_components,
        "messages": [message]
    }