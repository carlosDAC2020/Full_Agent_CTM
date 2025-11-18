
from __future__ import annotations

import os 
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos los nuevos esquemas del estado
from agents.tech_surveillance.state import GraphState, ReportSchema, ProjectObjectives
# Importamos los prompts 
from .prompts import SMART_OBJECTIVES_PROMPT

# --- Inicialización del LLM (sin cambios) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

def generate_objectives(state: GraphState) -> dict:
    """
    Nodo 2: Genera los Objetivos del Proyecto.
    """
    print("---SUBGRAPH: Generando Objetivos---")

    # 1. Leer de forma segura el estado actual
    report_components = state.get("report_components", ReportSchema())
    general_info = report_components.get("general_info", {})
    
    project_title = general_info.get("project_title", "No especificado")
    # La entrada clave: la justificación del nodo anterior
    justification = report_components.get("problem_statement_justification", "No hay justificación disponible.")

    # 2. Formatear el prompt
    prompt = SMART_OBJECTIVES_PROMPT.format(
        project_title=project_title,
        problem_statement_justification=justification
    )

    # 3. Invocar al LLM
    response = llm.invoke(prompt)
    generated_text = response.content

    # 4. Separar el objetivo general de los específicos
    general_obj, specific_objs = separate_objectives(generated_text)

    # 5. Construir el objeto ProjectObjectives
    objectives_schema = ProjectObjectives(
        general_objective=general_obj,
        specific_objectives_smart=specific_objs
    )

    # 6. Actualizar el esquema del reporte en el estado
    current_report_schema = state.get("report_components", ReportSchema())
    current_report_schema['objectives'] = objectives_schema
    
    # 7. Mensaje de confirmación
    message = AIMessage(content="Objetivos del proyecto generados. Procediendo a definir la metodología.")
    
    print("--- Objetivos generados y guardados en el estado. ---")

    # 8. Devolver el estado actualizado
    return {
        "report_components": current_report_schema,
        "messages": [message]
    }


def separate_objectives(full_text: str) -> tuple[str, str]:
    """
    Separa el objetivo general de los objetivos específicos usando el encabezado como ancla.
    """
    general_header = "### 5.1. Objetivo General"
    specific_header = "### 5.2. Objetivos Específicos (SMART)"
    
    try:
        # Encuentra las posiciones de los encabezados
        start_general = full_text.index(general_header)
        start_specific = full_text.index(specific_header)
        
        # Extrae el texto para el objetivo general
        general_obj_text = full_text[start_general + len(general_header):start_specific].strip()
        
        # El resto del texto son los objetivos específicos
        specific_obj_text = full_text[start_specific:].strip()
        
        return general_obj_text, specific_obj_text
    except ValueError:
        # Si no encuentra los encabezados, no puede separar. Retorna el texto completo en específicos.
        return "No se pudo extraer el objetivo general.", full_text