
from __future__ import annotations

import os 
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from agents.tech_surveillance.state import GraphState, ReportSchema, ExecutionPlan
# Importamos los prompts 
from .prompts import EXECUTIVE_SUMMARY_PROMPT

# --- Inicialización del LLM (sin cambios) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

def generate_executive_summary(state: GraphState) -> dict:
    """
    Nodo 7 (Final): Genera el Resumen Ejecutivo.
    """
    print("---SUBGRAPH: Generando Resumen Ejecutivo---")

    # 1. Leer TODAS las secciones generadas hasta ahora
    report_components = state.get("report_components", ReportSchema())
    general_info = report_components.get("general_info", {})
    objectives = report_components.get("objectives", {})
    methodology = report_components.get("methodology", "N/A")
    justification = report_components.get("problem_statement_justification", "N/A")
    impacts = report_components.get("results_and_impacts", "N/A")

    project_title = general_info.get("project_title", "No especificado")
    
    # Concatenar objetivos para pasarlos como un solo bloque de texto
    objectives_text = f"General: {objectives.get('general_objective', 'N/A')}\n\nSpecifics:\n{objectives.get('specific_objectives_smart', 'N/A')}"

    # 2. Formatear el prompt con el contexto completo
    prompt = EXECUTIVE_SUMMARY_PROMPT.format(
        project_title=project_title,
        problem_statement_justification=justification,
        objectives=objectives_text,
        methodology=methodology,
        results_and_impacts=impacts
    )

    # 3. Invocar al LLM
    response = llm.invoke(prompt)
    generated_summary = response.content

    # 4. Actualizar el esquema del reporte en el estado
    current_report_schema = state.get("report_components", ReportSchema())
    current_report_schema['executive_summary'] = generated_summary
    
    # 5. Mensaje de confirmación
    message = AIMessage(content="Resumen ejecutivo generado. El contenido del reporte está completo.")
    
    print("--- Resumen ejecutivo generado. Subgrafo de contenido completado. ---")

    # 6. Devolver el estado actualizado
    return {
        "report_components": current_report_schema,
        "messages": [message]
    }

