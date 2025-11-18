
from __future__ import annotations

import os 
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from agents.tech_surveillance.state import GraphState, ReportSchema

# Importamos los prompts 
from .prompts import IMPACTS_PROMPT


# --- Inicialización del LLM (sin cambios) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

def generate_impacts(state: GraphState) -> dict:
    """
    Nodo 6: Genera los Resultados e Impactos Esperados.
    """
    print("---SUBGRAPH: Generando Impactos---")

    # 1. Leer de forma segura el estado actual
    report_components = state.get("report_components", ReportSchema())
    general_info = report_components.get("general_info", {})
    objectives = report_components.get("objectives", {})

    project_title = general_info.get("project_title", "No especificado")
    general_objective = objectives.get("general_objective", "")
    specific_objectives = objectives.get("specific_objectives_smart", "")

    # 2. Formatear el prompt
    prompt = IMPACTS_PROMPT.format(
        project_title=project_title,
        general_objective=general_objective,
        specific_objectives_smart=specific_objectives
    )

    # 3. Invocar al LLM
    response = llm.invoke(prompt)
    generated_text = response.content

    # 4. Actualizar el esquema del reporte en el estado
    current_report_schema = state.get("report_components", ReportSchema())
    current_report_schema['results_and_impacts'] = generated_text
    
    # 5. Mensaje de confirmación
    message = AIMessage(content="Sección de resultados e impactos generada. Procediendo a crear el resumen ejecutivo final.")
    
    print("--- Resultados e impactos generados y guardados en el estado. ---")

    # 6. Devolver el estado actualizado
    return {
        "report_components": current_report_schema,
        "messages": [message]
    }