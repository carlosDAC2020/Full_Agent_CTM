from __future__ import annotations

import os 
import time
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from backend.agent.tech_surveillance.state import GraphState, ReportSchema, ExecutionPlan
# Importamos los prompts 
from .prompts import RISK_MATRIX_PROMPT
from ...prompts import SHARED_CONTEXT_HEADER

# --- Inicialización del LLM (sin cambios) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

def build_risk_matrix(state: GraphState) -> dict:
    """
    Nodo 5: Construye la Matriz de Riesgos usando Structured Output.
    """
    print("---SUBGRAPH: Construyendo Matriz de Riesgos (Structured)---")
    
    # Debug API Key
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ ERROR: GEMINI_API_KEY no encontrada.")
    # 1. Leer de forma segura el estado actual
    report_components = state.get("report_components") or ReportSchema()
    
    # --- LÓGICA DE REGENERACIÓN SELECTIVA ---
    config = state.get("generation_config")
    if isinstance(config, dict):
        try:
            from backend.agent.tech_surveillance.state import GenerationConfig
            config = GenerationConfig(**config)
        except:
            pass
    
    sections_to_regen = getattr(config, "sections_to_regenerate", []) or []
    
    # La matriz de riesgos está dentro de 'execution_plan'
    has_risks = report_components.execution_plan and report_components.execution_plan.risk_matrix
    if has_risks and "risk_matrix" not in sections_to_regen:
        print("⏭️ SKIP: Matriz de Riesgos ya existe y no fue seleccionada para regenerar.")
        return {
            "report_components": report_components,
            "messages": [AIMessage(content="Omitiendo generación de Matriz de Riesgos (contenido persistente).")]
        }

    project_title = "No especificado"
    if report_components.general_info:
        project_title = report_components.general_info.project_title or "No especificado"
        
    activity_schedule = "No hay cronograma disponible."
    if report_components.execution_plan:
        activity_schedule = report_components.execution_plan.activity_schedule or "No hay cronograma disponible."

    # 2. Formatear el prompt
    initial_schema = state.get("initial_schema") or "No se encontró el esquema inicial."
    header_prompt = SHARED_CONTEXT_HEADER.format(
        initial_schema=initial_schema
    )
    prompt = RISK_MATRIX_PROMPT.format(
        project_title=project_title,
        activity_schedule=activity_schedule
    )

    # 3. Configurar el LLM para salida estructurada
    structured_llm = llm.with_structured_output(ExecutionPlan)

    # 4. Invocar al LLM con Reintentos
    full_prompt = header_prompt + "\n" + prompt
    
    generated_plan = None
    max_retries = 3
    for attempt in range(max_retries):
        try:
            generated_plan = structured_llm.invoke(full_prompt)
            if generated_plan: break
        except Exception as e:
            print(f"⚠️ Intento {attempt+1} fallido en Riesgos: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise e

    # 5. Actualizar el esquema del reporte en el estado
    
    if not report_components.execution_plan:
        report_components.execution_plan = ExecutionPlan()
        
    # Actualizamos SOLO el campo de matriz de riesgos
    if generated_plan.risk_matrix:
        report_components.execution_plan.risk_matrix = generated_plan.risk_matrix
    
    # 6. Mensaje de confirmación
    message = AIMessage(content="Matriz de riesgos construida (Estructurado). Procediendo a definir los impactos del proyecto.")
    
    print("--- Matriz de riesgos generada y guardada en el estado. ---")

    # 7. Devolver el estado actualizado
    return {
        "report_components": report_components,
        "messages": [message]
    }