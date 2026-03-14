
from __future__ import annotations

import os 
import time

from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# Importamos los nuevos esquemas del estado
from backend.agent.tech_surveillance.state import GraphState, ReportSchema, ExecutionPlan
# Importamos los prompts 
from .prompts import BUDGET_PROMPT
from ...prompts import SHARED_CONTEXT_HEADER

# --- Inicialización del LLM ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

class BudgetOutput(BaseModel):
    """Salida estructurada para la generación del presupuesto."""
    budget: str = Field(description="A detailed budget or financial plan in Markdown format.")

def generate_budget(state: GraphState) -> dict:
    """
    Nodo 8: Genera el Presupuesto del Proyecto.
    """
    print("---SUBGRAPH: Generando Presupuesto---")
    
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
    
    # El presupuesto está dentro de 'execution_plan'
    has_budget = report_components.execution_plan and report_components.execution_plan.budget
    if has_budget and "budget" not in sections_to_regen:
        print("⏭️ SKIP: Presupuesto ya existe y no fue seleccionado para regenerar.")
        return {
            "report_components": report_components,
            "messages": [AIMessage(content="Omitiendo generación de Presupuesto (contenido persistente).")]
        }

    project_title = "No especificado"
    if report_components.general_info:
        project_title = report_components.general_info.project_title or "No especificado"
        
    specific_objectives = ""
    if report_components.objectives:
        specific_objectives = report_components.objectives.specific_objectives_smart or ""
        
    methodology = report_components.methodology or "No se definió metodología."
    
    duration = "No especificada"
    if report_components.general_info:
        duration = report_components.general_info.duration_months or "No especificada"

    # Información de la convocatoria (para límites de financiamiento)
    call_info = state.get("call_info")
    funding_info = "No especificado (ajustar a un presupuesto de I+D estándar)"
    if call_info:
        funding_info = call_info.funding or funding_info

    initial_schema = state.get("initial_schema") or "No se encontró el esquema inicial."

    header_prompt = SHARED_CONTEXT_HEADER.format(
        initial_schema=initial_schema
    )

    # Configuración (Límite de caracteres)
    char_limit = getattr(config, "charLimit", 2500) if config else 2500
    section_limits = getattr(config, "section_char_limits", {}) or {}
    char_limit = section_limits.get("budget", char_limit)

    # 2. Formatear el prompt
    prompt = BUDGET_PROMPT.format(
        project_title=project_title,
        methodology=methodology,
        specific_objectives_smart=specific_objectives,
        duration=duration,
        char_limit=char_limit,
        funding_limit=funding_info
    )

    # 3. Configurar el LLM para salida estructurada
    structured_llm = llm.with_structured_output(BudgetOutput)

    # 4. Invocar al LLM con Reintentos
    full_prompt = header_prompt + "\n" + prompt
    
    generated_output = None
    max_retries = 3
    for attempt in range(max_retries):
        try:
            generated_output = structured_llm.invoke(full_prompt)
            if generated_output: break
        except Exception as e:
            print(f"⚠️ Intento {attempt+1} fallido en Presupuesto: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise e

    # 5. Actualizar el esquema del reporte en el estado
    if not report_components.execution_plan:
        report_components.execution_plan = ExecutionPlan()
        
    if generated_output.budget:
        report_components.execution_plan.budget = generated_output.budget
    
    # 6. Mensaje de confirmación
    message = AIMessage(content="Presupuesto generado correctamente. Procediendo.")
    
    print("--- Presupuesto generado y guardado en el estado. ---")

    # 7. Devolver el estado actualizado
    return {
        "report_components": report_components,
        "messages": [message]
    }
