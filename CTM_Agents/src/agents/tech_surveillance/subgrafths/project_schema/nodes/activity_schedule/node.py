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
    Nodo 4: Crea el Cronograma de Actividades usando Structured Output.
    """
    print("---SUBGRAPH: Creando Cronograma (Structured)---")

    # 1. Leer de forma segura el estado actual
    report_components = state.get("report_components") or ReportSchema()
    
    project_title = "No especificado"
    if report_components.general_info:
        project_title = report_components.general_info.project_title or "No especificado"
        
    specific_objectives = ""
    if report_components.objectives:
        specific_objectives = report_components.objectives.specific_objectives_smart or ""
        
    methodology = report_components.methodology or "No se definió metodología."

    # 2. Formatear el prompt
    prompt = ACTIVITY_SCHEDULE_PROMPT.format(
        project_title=project_title,
        methodology=methodology,
        specific_objectives_smart=specific_objectives
    )

    # 3. Configurar el LLM para salida estructurada
    # Usamos ExecutionPlan, el LLM llenará activity_schedule y dejará risk_matrix en None
    structured_llm = llm.with_structured_output(ExecutionPlan)

    # 4. Invocar al LLM
    generated_plan = structured_llm.invoke(prompt)

    # 5. Actualizar el esquema del reporte en el estado
    
    # Asegurarnos de que 'execution_plan' exista
    if not report_components.execution_plan:
        report_components.execution_plan = ExecutionPlan()
        
    # Actualizamos SOLO el campo de cronograma
    if generated_plan.activity_schedule:
        report_components.execution_plan.activity_schedule = generated_plan.activity_schedule
    
    # 6. Mensaje de confirmación
    message = AIMessage(content="Cronograma de actividades generado (Estructurado). Procediendo a construir la matriz de riesgos.")
    
    print("--- Cronograma generado y guardado en el estado. ---")

    # 7. Devolver el estado actualizado
    return {
        "report_components": report_components,
        "messages": [message]
    }