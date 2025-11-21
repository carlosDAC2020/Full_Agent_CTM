from __future__ import annotations

import os 
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from agents.tech_surveillance.state import GraphState, ReportSchema, ExecutiveSummary
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
    Nodo 7 (Final): Genera el Resumen Ejecutivo usando Structured Output.
    """
    print("---SUBGRAPH: Generando Resumen Ejecutivo (Structured)---")

    # 1. Leer TODAS las secciones generadas hasta ahora
    report_components = state.get("report_components") or ReportSchema()
    
    project_title = "No especificado"
    if report_components.general_info:
        project_title = report_components.general_info.project_title or "No especificado"
        
    methodology = "N/A"
    if report_components.methodology:
        methodology = report_components.methodology.content or "N/A"
        
    justification = "N/A"
    if report_components.problem_statement_justification:
        justification = report_components.problem_statement_justification.content or "N/A"
        
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

    # 2. Formatear el prompt con el contexto completo
    prompt = EXECUTIVE_SUMMARY_PROMPT.format(
        project_title=project_title,
        problem_statement_justification=justification,
        objectives=objectives_text,
        methodology=methodology,
        results_and_impacts=impacts
    )

    # 3. Configurar el LLM para salida estructurada
    structured_llm = llm.with_structured_output(ExecutiveSummary)

    # 4. Invocar al LLM
    summary_schema = structured_llm.invoke(prompt)

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
