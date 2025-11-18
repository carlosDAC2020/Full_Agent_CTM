from __future__ import annotations

import os 
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from agents.tech_surveillance.state import GraphState, ReportSchema, ExecutionPlan
# Importamos los prompts 
from .prompts import ACTIVITY_SCHEDULE_PROMPT

# --- Inicialización del LLM (sin cambios) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

def create_activity_schedule(state: GraphState) -> dict:
    """
    Nodo 4: Crea el Cronograma de Actividades.
    """
    print("---SUBGRAPH: Creando Cronograma---")

    # 1. Leer de forma segura el estado actual
    report_components = state.get("report_components", ReportSchema())
    general_info = report_components.get("general_info", {})
    objectives = report_components.get("objectives", {})
    methodology = report_components.get("methodology", "No se definió metodología.")

    project_title = general_info.get("project_title", "No especificado")
    specific_objectives = objectives.get("specific_objectives_smart", "")

    # 2. Formatear el prompt
    prompt = ACTIVITY_SCHEDULE_PROMPT.format(
        project_title=project_title,
        methodology=methodology,
        specific_objectives_smart=specific_objectives
    )

    # 3. Invocar al LLM
    response = llm.invoke(prompt)
    generated_schedule = response.content

    # 4. Actualizar el esquema del reporte en el estado
    current_report_schema = state.get("report_components", ReportSchema())
    
    # Asegurarnos de que 'execution_plan' exista antes de escribir en él
    if 'execution_plan' not in current_report_schema or not current_report_schema['execution_plan']:
        current_report_schema['execution_plan'] = ExecutionPlan()
        
    current_report_schema['execution_plan']['activity_schedule'] = generated_schedule
    
    # 5. Mensaje de confirmación
    message = AIMessage(content="Cronograma de actividades generado. Procediendo a construir la matriz de riesgos.")
    
    print("--- Cronograma generado y guardado en el estado. ---")

    # 6. Devolver el estado actualizado
    return {
        "report_components": current_report_schema,
        "messages": [message]
    }