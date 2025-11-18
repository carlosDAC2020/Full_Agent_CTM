from __future__ import annotations

import os 
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from agents.tech_surveillance.state import GraphState, ReportSchema, ExecutionPlan
# Importamos los prompts 
from .prompts import RISK_MATRIX_PROMPT

# --- Inicialización del LLM (sin cambios) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

def build_risk_matrix(state: GraphState) -> dict:
    """
    Nodo 5: Construye la Matriz de Riesgos.
    """
    print("---SUBGRAPH: Construyendo Matriz de Riesgos---")

    # 1. Leer de forma segura el estado actual
    report_components = state.get("report_components", ReportSchema())
    general_info = report_components.get("general_info", {})
    execution_plan = report_components.get("execution_plan", {})

    project_title = general_info.get("project_title", "No especificado")
    activity_schedule = execution_plan.get("activity_schedule", "No hay cronograma disponible.")

    # 2. Formatear el prompt
    prompt = RISK_MATRIX_PROMPT.format(
        project_title=project_title,
        activity_schedule=activity_schedule
    )

    # 3. Invocar al LLM
    response = llm.invoke(prompt)
    generated_matrix = response.content

    # 4. Actualizar el esquema del reporte en el estado
    current_report_schema = state.get("report_components", ReportSchema())
    
    # 'execution_plan' ya debería existir por el nodo anterior, pero por seguridad lo verificamos.
    if 'execution_plan' not in current_report_schema or not current_report_schema['execution_plan']:
        current_report_schema['execution_plan'] = ExecutionPlan()
        
    current_report_schema['execution_plan']['risk_matrix'] = generated_matrix
    
    # 5. Mensaje de confirmación
    message = AIMessage(content="Matriz de riesgos construida. Procediendo a definir los impactos del proyecto.")
    
    print("--- Matriz de riesgos generada y guardada en el estado. ---")

    # 6. Devolver el estado actualizado
    return {
        "report_components": current_report_schema,
        "messages": [message]
    }
    