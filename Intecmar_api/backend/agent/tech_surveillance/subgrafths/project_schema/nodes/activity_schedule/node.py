
from __future__ import annotations

import os 
import time
import re

from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# Importamos los nuevos esquemas del estado
from backend.agent.tech_surveillance.state import GraphState, ReportSchema, ExecutionPlan, GeneralInfo
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
    
    # Si la sección ya existe y no está marcada para regenerar, saltar
    # El cronograma está dentro de 'execution_plan'
    has_schedule = report_components.execution_plan and report_components.execution_plan.activity_schedule
    if has_schedule and "activity_schedule" not in sections_to_regen:
        print("⏭️ SKIP: Cronograma ya existe y no fue seleccionado para regenerar.")
        return {
            "report_components": report_components,
            "messages": [AIMessage(content="Omitiendo generación de Cronograma (contenido persistente).")]
        }

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
    duration = "No especificada"
    if report_components.general_info:
        duration = f"{report_components.general_info.duration_months} meses" if report_components.general_info.duration_months else "No especificada"

    # 2. Configuración (Límite de caracteres)
    char_limit = getattr(config, "charLimit", 2500) if config else 2500
    section_limits = getattr(config, "section_char_limits", {}) or {}
    char_limit = section_limits.get("activity_schedule", char_limit)
    
    print(f"--- Usando límite de caracteres: {char_limit} ---")

    # 3. Formatear el prompt
    prompt = ACTIVITY_SCHEDULE_PROMPT.format(
        project_title=project_title,
        methodology=methodology,
        specific_objectives_smart=specific_objectives,
        duration=duration,
        char_limit=char_limit
    )

    # 3. Configurar el LLM para salida estructurada
    # Usamos un esquema intermedio para capturar también la duración
    structured_llm = llm.with_structured_output(ScheduleGenerationOutput)

    # 4. Invocar al LLM con Reintentos
    full_prompt = header_prompt + "\n" + prompt
    
    generated_output = None
    max_retries = 3
    for attempt in range(max_retries):
        try:
            generated_output = structured_llm.invoke(full_prompt)
            if generated_output: break
        except Exception as e:
            print(f"⚠️ Intento {attempt+1} fallido en Cronograma: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise e

    # 5. Actualizar el esquema del reporte en el estado
    
    # --- POST-PROCESAMIENTO DE FORMATO ---
    schedule_text = generated_output.activity_schedule
    if schedule_text:
        # Asegurar espacio ANTES de los encabezados para evitar amontonamiento
        # 1. Normalizar ### (asegurar que tenga \n\n antes)
        schedule_text = re.sub(r'([^ \n])###', r'\1\n\n###', schedule_text)
        schedule_text = re.sub(r'\n###', r'\n\n###', schedule_text)
        
        # 2. Colapsar saltos de línea excesivos (máximo 2)
        schedule_text = re.sub(r'\n{3,}', r'\n\n', schedule_text)
        
        # 3. Limpiar espacios iniciales/finales
        schedule_text = schedule_text.strip()
        
        # 4. Corregir posibles alucinaciones de caracteres no latinos (ej: Hindi)
        # Solo permitimos caracteres ASCII, extendidos del español y símbolos comunes de MD
        # (Este es un fallback agresivo pero seguro si el modelo alucina)
        # schedule_text = re.sub(r'[^\x00-\x7F\xc0-\xff]', '', schedule_text) # Opcional: demasiado agresivo
        
        generated_output.activity_schedule = schedule_text

    # Asegurarnos de que 'execution_plan' exista
    if not report_components.execution_plan:
        report_components.execution_plan = ExecutionPlan()
        
    # Actualizamos el campo de cronograma
    if generated_output.activity_schedule:
        report_components.execution_plan.activity_schedule = generated_output.activity_schedule
        
    # Actualizamos la duración en GeneralInfo SOLO si no existe previamente
    # Esto preserva el valor definido en el Paso 3 (esquema inicial)
    if generated_output.duration_months:
        if not report_components.general_info:
            report_components.general_info = GeneralInfo()
        
        # Solo actualizar si no hay un valor previo
        if not report_components.general_info.duration_months:
            report_components.general_info.duration_months = generated_output.duration_months
            print(f"--- Duración del proyecto establecida: {generated_output.duration_months} meses ---")
        else:
            print(f"--- Duración del proyecto preservada: {report_components.general_info.duration_months} meses (ignorando {generated_output.duration_months}) ---")
    
    # 6. Mensaje de confirmación
    message = AIMessage(content=f"Cronograma generado (Duración: {generated_output.duration_months} meses). Procediendo a matriz de riesgos.")
    
    print("--- Cronograma generado y guardado en el estado. ---")

    # 7. Devolver el estado actualizado
    return {
        "report_components": report_components,
        "messages": [message]
    }
