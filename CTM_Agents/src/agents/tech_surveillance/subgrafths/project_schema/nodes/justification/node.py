from __future__ import annotations

import os 
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from agents.tech_surveillance.state import GraphState, ReportSchema
# Importamos los prompts (que también modificaremos)
from .prompts import JUSTIFICATION_PROMPT

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
    Nodo 1: Genera el Planteamiento del Problema y Justificación.
    """
    print("---SUBGRAPH: Generando Justificación---")

    # 1. Leer de forma segura el estado actual
    report_components = state.get("report_components", ReportSchema())
    general_info = report_components.get("general_info", {})
    theoretical_framework = report_components.get("theoretical_framework", {})

    project_title = general_info.get("project_title", "No especificado")
    project_description = general_info.get("project_description", "No especificado")
    framework_body = theoretical_framework.get("body", "No se encontró marco teórico.")

    # 2. Formatear el prompt con la información extraída
    prompt = JUSTIFICATION_PROMPT.format(
        project_title=project_title,
        project_description=project_description,
        theoretical_framework_body=framework_body
    )

    # 3. Invocar al LLM para generar el contenido
    response = llm.invoke(prompt)
    generated_text = response.content

    # 4. Actualizar el esquema del reporte en el estado
    # Obtenemos el objeto actual y lo modificamos, no creamos uno nuevo
    current_report_schema = state.get("report_components", ReportSchema())
    current_report_schema['problem_statement_justification'] = generated_text
    
    # 5. Mensaje de confirmación para el historial
    message = AIMessage(content="Justificación del proyecto generada. Procediendo a definir los objetivos.")
    
    print("--- Justificación generada y guardada en el estado. ---")

    # 6. Devolver el estado actualizado
    return {
        "report_components": current_report_schema,
        "messages": [message]
    }