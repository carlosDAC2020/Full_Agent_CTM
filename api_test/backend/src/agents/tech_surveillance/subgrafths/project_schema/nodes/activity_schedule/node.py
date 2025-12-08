
from __future__ import annotations

import os 
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# Importamos los nuevos esquemas del estado
from agents.tech_surveillance.state import GraphState, ReportSchema, ExecutionPlan, GeneralInfo
# Importamos los prompts 
from .prompts import ACTIVITY_SCHEDULE_PROMPT
from ...prompts import SHARED_CONTEXT_HEADER

# --- Inicialización del LLM (sin cambios) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

class ScheduleGenerationOutput(BaseModel):
    """Salida estructurada para la generación del cronograma."""
    activity_schedule: str = Field(description="A detailed activity schedule or Gantt chart description in Markdown format.")
    duration_months: int = Field(description="The total duration of the project in months, derived from the schedule.")

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

    
    initial_schema = state.get("initial_schema") or "No se encontró el esquema inicial."

    header_prompt = SHARED_CONTEXT_HEADER.format(
        initial_schema=initial_schema
    )
    # 2. Formatear el prompt
    prompt = ACTIVITY_SCHEDULE_PROMPT.format(
        project_title=project_title,
        methodology=methodology,
        specific_objectives_smart=specific_objectives
    )

    # 3. Configurar el LLM para salida estructurada
    # Usamos un esquema intermedio para capturar también la duración
    structured_llm = llm.with_structured_output(ScheduleGenerationOutput)

    # 4. Invocar al LLM
    full_prompt = header_prompt + "\n" + prompt
    generated_output = structured_llm.invoke(full_prompt)

    # 5. Actualizar el esquema del reporte en el estado
    
    # Asegurarnos de que 'execution_plan' exista
    if not report_components.execution_plan:
        report_components.execution_plan = ExecutionPlan()
        
    # Actualizamos el campo de cronograma
    if generated_output.activity_schedule:
        report_components.execution_plan.activity_schedule = generated_output.activity_schedule
        
    # Actualizamos la duración en GeneralInfo
    if generated_output.duration_months:
        if not report_components.general_info:
            report_components.general_info = GeneralInfo()
        report_components.general_info.duration_months = generated_output.duration_months
        print(f"--- Duración del proyecto actualizada: {generated_output.duration_months} meses ---")
    
    # 6. Mensaje de confirmación
    message = AIMessage(content=f"Cronograma generado (Duración: {generated_output.duration_months} meses). Procediendo a matriz de riesgos.")
    
    print("--- Cronograma generado y guardado en el estado. ---")

    # 7. Devolver el estado actualizado
    return {
        "report_components": report_components,
        "messages": [message]
    }
