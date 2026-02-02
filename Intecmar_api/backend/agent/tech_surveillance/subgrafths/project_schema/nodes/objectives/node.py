from __future__ import annotations

import os 
import time

from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from backend.agent.tech_surveillance.state import GraphState, ReportSchema, ProjectObjectives
# Importamos los prompts 
from .prompts import SMART_OBJECTIVES_PROMPT
from ...prompts import SHARED_CONTEXT_HEADER

# --- Inicialización del LLM (sin cambios) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

def generate_objectives(state: GraphState) -> dict:
    """
    Nodo 2: Genera los Objetivos del Proyecto usando Structured Output.
    """
    print("---SUBGRAPH: Generando Objetivos (Structured)---")
    
    # Debug API Key (without printing it)
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ ERROR: GEMINI_API_KEY no encontrada en el entorno del worker.")
    
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
    is_objectives_regen_selected = "objectives" in sections_to_regen

    # Si la sección ya existe y no está marcada para regenerar, saltar
    if report_components.objectives and not is_objectives_regen_selected:
        print("⏭️ SKIP: Objetivos ya existen y no fueron seleccionados para regenerar.")
        return {
            "report_components": report_components,
            "messages": [AIMessage(content="Omitiendo generación de Objetivos (contenido persistente).")]
        }

    project_title = "No especificado"
    if report_components.general_info:
        project_title = report_components.general_info.project_title or "No especificado"
    
    # La entrada clave: la justificación del nodo anterior
    justification_obj = report_components.problem_statement_justification
    if justification_obj:
        ps = getattr(justification_obj, 'problem_statement', '')
        j = getattr(justification_obj, 'justification', '')
        justification = f"Planteamiento del Problema: {ps}\nJustificación: {j}"
    else:
        justification = "No hay justificación disponible."
    
    duration = "No especificada"
    if report_components.general_info:
        duration = f"{report_components.general_info.duration_months} meses" if report_components.general_info.duration_months else "No especificada"

    # 2. Formatear el prompt
    initial_schema = state.get("initial_schema") or "No se encontró el esquema inicial."
    
    # Contexto del Paso 3
    selected_methodology = state.get("selected_methodology") or "No especificada"
    selected_idea = state.get("selected_idea")
    
    reference_objectives = ""
    if selected_idea:
        # Extraer objetivos si existen en el objeto o dict
        if isinstance(selected_idea, dict):
            objs = selected_idea.get("idea_specific_objectives") or selected_idea.get("idea_objectives") or selected_idea.get("objectives") or []
            gen_obj = selected_idea.get("idea_general_objective") or selected_idea.get("general_objective") or ""
        else:
            objs = getattr(selected_idea, "idea_specific_objectives", []) or getattr(selected_idea, "idea_objectives", []) or getattr(selected_idea, "objectives", [])
            gen_obj = getattr(selected_idea, "idea_general_objective", "") or getattr(selected_idea, "general_objective", "")
            
        if gen_obj:
            reference_objectives += f"Objetivo General Sugerido: {gen_obj}\n"
        if objs:
            reference_objectives += "Objetivos Específicos Sugeridos:\n" + "\n".join([f"- {o}" for o in objs])

    header_prompt = SHARED_CONTEXT_HEADER.format(
        initial_schema=initial_schema
    )
    prompt = SMART_OBJECTIVES_PROMPT.format(
        project_title=project_title,
        problem_statement_justification=justification,
        duration=duration,
        selected_methodology=selected_methodology,
        reference_objectives=reference_objectives or "No hay objetivos de referencia."
    )

    # 3. Verificar si ya existen objetivos editados por el usuario (SOLO si no forzamos regeneración)
    if selected_idea and not is_objectives_regen_selected:
        if isinstance(selected_idea, dict):
            manual_gen_obj = selected_idea.get("idea_general_objective", "")
            manual_spec_objs = selected_idea.get("idea_specific_objectives", [])
        else:
            manual_gen_obj = getattr(selected_idea, "idea_general_objective", "")
            manual_spec_objs = getattr(selected_idea, "idea_specific_objectives", [])
            
        if manual_gen_obj and manual_spec_objs:
            print("--- Reutilizando objetivos editados por el usuario (Saltando generación) ---")
            spec_objs_markdown = "\n".join([f"- {o}" for o in manual_spec_objs])
            report_components.objectives = ProjectObjectives(
                general_objective=manual_gen_obj,
                specific_objectives_smart=spec_objs_markdown
            )
            return {
                "report_components": report_components,
                "messages": [AIMessage(content="Objetivos manuales preservados. Procediendo a metodología.")]
            }

    # 4. Configurar el LLM para salida estructurada (Fallback si no hay manuales)
    structured_llm = llm.with_structured_output(ProjectObjectives)

    # 5. Invocar al LLM con Reintentos
    full_prompt = header_prompt + "\n" + prompt
    
    objectives_schema = None
    max_retries = 3
    for attempt in range(max_retries):
        try:
            objectives_schema = structured_llm.invoke(full_prompt)
            if objectives_schema: break
        except Exception as e:
            print(f"⚠️ Intento {attempt+1} fallido en Objetivos: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise e

    # 6. Actualizar el esquema del reporte en el estado
    report_components.objectives = objectives_schema
    
    # 6. Mensaje de confirmación
    message = AIMessage(content="Objetivos del proyecto generados (Estructurado). Procediendo a definir la metodología.")
    
    print("--- Objetivos generados y guardados en el estado. ---")

    # 7. Devolver el estado actualizado
    return {
        "report_components": report_components,
        "messages": [message]
    }