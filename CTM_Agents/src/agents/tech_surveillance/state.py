# state.py

from typing_extensions import TypedDict
from typing import List, Optional, Annotated
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

# --- Funciones de Utilidad ---

def latest_value(current, updates):
    """Toma el último valor, ignora duplicados desde nodos paralelos."""
    if isinstance(updates, list):
        return updates[-1] if updates else current
    return updates

# --- Esquemas Anidados para el Reporte ---

class GeneralInfo(TypedDict):
    """Sección 2: Generalidades del Proyecto."""
    project_title: Optional[str] = None
    project_description: Optional[str] = None
    duration_months: Optional[int] = None
    thematic_line: Optional[str] = None
    keywords: Optional[List[str]] = None
    # Puedes añadir más campos extraídos del PDF, como entidades
    main_entity: Optional[str] = None
    collaborating_entities: Optional[List[str]] = None

class TheoreticalFramework(TypedDict):
    """Sección 4: Marco Teórico."""
    body: Optional[str] = None          # El texto principal de la investigación
    references_apa: Optional[str] = None # La bibliografía extraída y formateada

class ProjectObjectives(TypedDict):
    """Sección 5: Objetivos."""
    general_objective: Optional[str] = None
    specific_objectives_smart: Optional[str] = None # El texto generado con el formato SMART

class ExecutionPlan(TypedDict):
    """Sección 7: Plan de Ejecución y Gestión."""
    activity_schedule: Optional[str] = None  # El cronograma en formato Markdown
    risk_matrix: Optional[str] = None        # La matriz de riesgos en formato Markdown

class ReportSchema(TypedDict):
    """
    Contenedor principal para todos los componentes estructurados del informe final.
    Cada campo corresponde a una sección principal de la plantilla Markdown.
    """
    # Secciones generadas por nodos
    executive_summary: Optional[str] = None                # Sección 1
    problem_statement_justification: Optional[str] = None  # Sección 3
    methodology: Optional[str] = None                      # Sección 6
    results_and_impacts: Optional[str] = None              # Sección 8
    
    # Secciones compuestas de sub-esquemas
    general_info: Optional[GeneralInfo] = None
    theoretical_framework: Optional[TheoreticalFramework] = None
    objectives: Optional[ProjectObjectives] = None
    execution_plan: Optional[ExecutionPlan] = None

# --- Estado Principal del Grafo ---

class GraphState(TypedDict):
    """
    Representa el estado de nuestro grafo, ahora más organizado.
    """
    # --- Estado de la Conversación y Entrada ---
    messages: Annotated[list[BaseMessage], add_messages]
    document_urls: Optional[List[str]] = None
    
    # --- Control de Flujo ---
    route_decision: Annotated[Optional[str], latest_value] = None

    # --- Componentes para la Generación de Imágenes ---
    image_prompt: Annotated[Optional[str], latest_value] = None
    generated_image_path: Annotated[Optional[str], latest_value] = None
    
    # --- ESQUEMA CENTRAL DEL REPORTE ---
    # Este objeto se irá llenando progresivamente por los diferentes nodos.
    report_components: Annotated[Optional[ReportSchema], latest_value] = None

    # --- Campo Final ---
    # El nodo de reporte final tomará 'report_components' y generará este string.
    final_report: Annotated[Optional[str], latest_value] = None