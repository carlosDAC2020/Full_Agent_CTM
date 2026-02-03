from pydantic import BaseModel, Field
from typing import Optional, List, Annotated, Any, Dict
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict


# --- Esquemas Anidados para el Reporte (Pydantic) ---

class GeneralInfo(BaseModel):
    """Sección 2: Generalidades del Proyecto."""
    project_title: Optional[str] = Field(
        default=None, 
        description="Title of the project")
    project_description: Optional[str] = Field(
        default=None, 
        description="Project description")
    duration_months: Optional[int] = Field(
        default=None, 
        description="Duration in months")
    thematic_line: Optional[str] = Field(
        default=None, 
        description="Thematic line")
    keywords: Optional[List[str]] = Field(
        default=None, 
        description="Keywords separated by commas")

    # aliansas
    executor_entity: Optional[str] = Field(
        default=None, 
        description="Executor entity"
    )
    executor_entity_logo: Optional[str] = Field(
        default=None, 
        description="Executor entity logo"
    )   
    coejecutors_entities: Optional[List[str]] = Field(
        default=None, 
        description="Co-executors entities list"
    )
    coejecutors_entities_logos: Optional[List[str]] = Field(
        default=None, 
        description="Co-executors entities logos list"
    )
    collaborators_entities: Optional[List[str]] = Field(
        default=None, 
        description="Collaborators entities list"
    )
    collaborators_entities_logos: Optional[List[str]] = Field(
        default=None, 
        description="Collaborators entities logos list"
    )

class TheoreticalFramework(BaseModel):
    """Schema for the Theoretical Framework and State of the Art section."""
    
    body: Optional[str] = Field(
        default=None, 
        description=(
            "The main narrative text of the report in Markdown format. "
            "It must explicitly include content for sections: "
            "4.1 (Introduction to Domain), "
            "4.2 (Literature Review), "
            "4.3 (State of the Art), and "
            "4.4 (Knowledge Gaps). "
            "Do NOT include the references list here."
        )
    )
    references_apa: Optional[str] = Field(
        default=None, 
        description=(
            "The complete list of bibliographic references corresponding to Section 9. "
            "Must be strictly formatted in APA 7th Edition style. "
            "This field should contain the list of citations."
        )
    )

class Justification(BaseModel):
    """Section 3: Problem Statement and Justification."""
    problem_statement: Optional[str] = Field(
        default=None,
        description=(
            "The Problem Statement (Planteamiento del Problema). "
            "It should clearly define the problem, its magnitude, and current context."
        )
    )
    justification: Optional[str] = Field(
        default=None,
        description=(
            "The Project Justification (Justificación). "
            "It should explain why this project is the necessary solution and its strategic importance."
        )
    )

class ProjectObjectives(BaseModel):
    """Section 5: Project Objectives."""
    general_objective: Optional[str] = Field(
        default=None, 
        description=(
            "The general objective of the project. This should be a single, comprehensive statement "
            "that defines the overall goal of the project."
        )
    )
    specific_objectives_smart: Optional[str] = Field(
        default=None, 
        description=(
            "The specific objectives of the project, formatted as a Markdown list. "
            "These objectives must strictly adhere to the SMART criteria (Specific, Measurable, "
            "Achievable, Relevant, Time-bound)."
        )
    )

class Methodology(BaseModel):
    """Section 6: Proposed Methodology."""
    content: Optional[str] = Field(
        default=None,
        description=(
            "The complete text for the Proposed Methodology section in Markdown. "
            "It should describe the approach, methods, and techniques that will be used to achieve the objectives."
        )
    )

class ExecutionPlan(BaseModel):
    """Section 7: Execution and Management Plan."""
    activity_schedule: Optional[str] = Field(
        default=None, 
        description=(
            "A detailed activity schedule or Gantt chart description in Markdown format. "
            "It should outline the phases, activities, and estimated duration for each."
        )
    )
    risk_matrix: Optional[str] = Field(
        default=None, 
        description=(
            "A risk matrix or analysis in Markdown format (e.g., a table). "
            "It should identify potential risks, their probability, impact, and mitigation strategies."
        )
    )
    budget: Optional[str] = Field(
        default=None,
        description=(
            "A detailed budget or financial plan in Markdown format (e.g., a table). "
            "It should outline the resources and costs required for the project."
        )
    )

class Impacts(BaseModel):
    """Section 8: Expected Results and Impacts."""
    content: Optional[str] = Field(
        default=None,
        description=(
            "The complete text for the Expected Results and Impacts section in Markdown. "
            "It should detail the scientific, technological, economic, and social impacts of the project."
        )
    )

class ExecutiveSummary(BaseModel):
    """Section 1: Executive Summary."""
    content: Optional[str] = Field(
        default=None,
        description=(
            "The Executive Summary of the project in Markdown. "
            "It should provide a concise overview of the entire project, including the problem, objectives, methodology, and expected results."
        )
    )

class ReportSchema(BaseModel):
    """Contenedor principal para componentes estructurados del informe."""
    executive_summary: Optional[ExecutiveSummary] = Field(default=None, description="Sección 1")
    problem_statement_justification: Optional[Justification] = Field(default=None, description="Sección 3")
    methodology: Optional[Methodology] = Field(default=None, description="Sección 6")
    results_and_impacts: Optional[Impacts] = Field(default=None, description="Sección 8")
    
    general_info: Optional[GeneralInfo] = Field(default=None, description="Información general")
    theoretical_framework: Optional[TheoreticalFramework] = Field(default=None, description="Marco teórico")
    objectives: Optional[ProjectObjectives] = Field(default=None, description="Objetivos")
    execution_plan: Optional[ExecutionPlan] = Field(default=None, description="Plan de ejecución")

class CallInfo(BaseModel):
    """Información extraída de la convocatoria."""
    title: Optional[str] = Field(default=None, description="Título de la convocatoria")
    objective: Optional[str] = Field(default=None, description="Objetivo principal de la convocatoria")
    description: Optional[str] = Field(default=None, description="Descripción detallada o resumen de la convocatoria")
    funding: Optional[str] = Field(default=None, description="Información sobre financiamiento")
    keywords: Optional[List[str]] = Field(default=None, description="Palabras clave de la convocatoria")
    important_dates: Optional[str] = Field(default=None, description="Opening and closing dates of the call (e.g., 'Apertura: [Fecha] | Cierre: [Fecha]')")
    dates: Optional[str] = Field(default=None, description="Alias for important_dates to ensure compatibility")
    benefits: Optional[List[str]] = Field(default=None, description="Beneficios listados")
    
    # lineas tematicas
    thematic_lines: Optional[List[str]] = Field(
        default=None, 
        description="Lineas tematicas listadas"
    )

    # enfoque metodologico
    methodology: Optional[str] = Field(
        default=None, 
        description="Enfoque metodologico de la convocatoria (ej: MGA WEB, SMART, PMI, SCRUM)"
    )
    
    suggested_frameworks: Optional[List[str]] = Field(
        default=["MGA WEB", "SMART", "PMI", "SCRUM", "ISO 21500"],
        description="Lista de marcos metodológicos sugeridos o detectados"
    )
    
    presentation_history: Optional[List[dict]] = Field(
        default=None, 
        description="History of generated presentations (versions)."
    )

    url: Optional[str] = Field(
        default=None, 
        description="URL de más información"
    )

    context_docs: Optional[List[str]] = Field(
        default=None,
        description="Rutas a documentos relevantes de la convocatoria"
    )

class ProposalIdea(BaseModel):
    """Idea de proyecto propuesta por el usuario."""
    idea_title: Optional[str] = Field(
        default=None, 
        description="Título de la idea de proyecto"
    )
    idea_description: Optional[str] = Field(
        default=None, 
        description="Descripción de la idea de proyecto"
    ) 
    # objetivo genral
    idea_general_objective: Optional[str] = Field(
        default=None, 
        description="Objetivo general de la idea de proyecto"
    )
    # objetivos espeficios
    idea_specific_objectives: Optional[List[str]] = Field(
        default=None, 
        description="5 objetivos de la idea de proyecto basadas en en la metodologia seleccionada"
    )
    # Alias para compatibilidad con frontend
    idea_objectives: Optional[List[str]] = Field(
        default=None, 
        description="Alias para idea_specific_objectives"
    )

    # Duración sugerida (inferida de la convocatoria o generada por el modelo)
    suggested_duration_months: Optional[int] = Field(
        default=None, 
        description="Duración sugerida del proyecto en meses, inferida de la información de la convocatoria"
    )

    # ---------------- campos q debe llenar el usuario -----------------

    # duracion
    duration_time: Optional[str] = Field(
        default=None, 
        description="Duración del proyecto"
    )
    # aliansas
    executor_entity: Optional[str] = Field(
        default=None, 
        description="Executor entity"
    )
    executor_entity_logo: Optional[str] = Field(
        default=None, 
        description="Executor entity logo"
    )   
    coejecutors_entities: Optional[List[str]] = Field(
        default=None, 
        description="Co-executors entities list"
    )
    coejecutors_entities_logos: Optional[List[str]] = Field(
        default=None, 
        description="Co-executors entities logos list"
    )
    collaborators_entities: Optional[List[str]] = Field(
        default=None, 
        description="Collaborators entities list"
    )
    collaborators_entities_logos: Optional[List[str]] = Field(
        default=None, 
        description="Collaborators entities logos list"
    )

class proposalIdeaResponse(BaseModel):
    ideas: Optional[List[ProposalIdea]] = Field(
        default=None,
        description="Lista de ideas de proyecto propuestas"
    )

class DocsPaths(BaseModel):
    """Rutas de documentos generados."""
    # documentos referentes a la presentacion de la convoctaoria 
    presentation_oath_md: Optional[str] = Field(
        default=None, 
        description="Ruta del documento de presentación en Markdown"
    )
    presentation_oath_pdf: Optional[str] = Field(
        default=None, 
        description="Ruta del documento de presentación en PDF"
    )
    presentation_oath_pptx: Optional[str] = Field(
        default=None, 
        description="Ruta del documento de presentación en PPTX"
    )

    # documentpos relevantes al documento de investigacion del proyecto 
    proyect_proposal_initial_schema_md: Optional[str] = Field(
        default=None, 
        description="Ruta del documento de esquema inicial de propuesta de proyecto en Markdown"
    )
    proyect_proposal_initial_schema_pdf: Optional[str] = Field(
        default=None, 
        description="Ruta del documento de esquema inicial de propuesta de proyecto en PDF"
    )
    proyect_proposal_md: Optional[str] = Field(
        default=None, 
        description="Ruta del documento de propuesta de proyecto en Markdown"
    )
    proyect_proposal_pdf: Optional[str] = Field(
        default=None, 
        description="Ruta del documento de propuesta de proyecto en PDF"
    )

    # documento de imagen generada
    poster_image_path: Optional[str] = Field(
        default=None, 
        description="Ruta del poster del proyetco generado"
    )


class GenerationConfig(BaseModel):
    """Configuración para la generación del reporte (Paso 4)."""
    charLimit: int = Field(default=2050, description="Límite aproximado de caracteres por sección.")
    refStyle: str = Field(default="APA", description="Estilo de citación (APA, IEEE, etc.).")
    
    # Nuevos campos para regeneración selectiva
    sections_to_regenerate: List[str] = Field(default_factory=list, description="Lista de IDs de secciones a regenerar.")
    redo_theoretical_framework: bool = Field(default=False, description="Si es True, se vuelve a ejecutar academic_research.")
    section_char_limits: Dict[str, int] = Field(default_factory=dict, description="Límites específicos por sección.")
    poster_prompt_override: Optional[str] = Field(default=None, description="Nuevo prompt para la generación del póster.")
    base_image_path: Optional[str] = Field(default=None, description="Ruta de imagen base a usar (historial) en lugar de generar una nueva con IA.")


class GenerationItem(BaseModel):
    """Representa una iteración de generación (Poster + PDF + MD)."""
    timestamp: str = Field(description="ISO timestamp of generation")
    poster_path: Optional[str] = Field(default=None, description="Path or URL to the poster image")
    base_image_path: Optional[str] = Field(default=None, description="Path or URL to the base poster image (no logos)")
    pdf_path: Optional[str] = Field(default=None, description="Path or URL to the PDF report")
    md_path: Optional[str] = Field(default=None, description="Path or URL to the Markdown report")
    prompt_used: Optional[str] = Field(default=None, description="Prompt used for this generation")

    class Config:
        validate_assignment = True

class GraphState(TypedDict):
    """Estado del grafo con validación Pydantic."""
    messages: Annotated[list[BaseMessage], add_messages]
    document_urls: Optional[List[str]]

    # decisión de ruta desde el enrutador solo tenga disponibles estas dos opciones
    #"ingest": "ingest",
    #"generate_proyect": "proyect_idea",
    route_decision: Optional[str] = "ingest"  
    call_info: Optional[CallInfo] # Información de la convocatoria
    image_prompt: Optional[str]
    generated_image_path: Optional[str]
    report_components: Optional[ReportSchema]  # Ahora Pydantic
    final_report: Optional[str]

    # ideas de proyecto propuestas
    proposal_ideas: Optional[proposalIdeaResponse]
    selected_idea: Optional[ProposalIdea]
    
    # Preferencias del usuario para la generación de ideas
    selected_thematic_line: Optional[str]
    selected_methodology: Optional[str]

    # resumen de presentacion
    presentation_summary : Optional[str]
    
    # esquema incial de dpocumento 
    initial_schema: Optional[str]

    # rutas de documentos generados
    docs_paths: Optional[DocsPaths]

    # Configuracion de generacion
    generation_config: Optional[GenerationConfig]
    
    randonm_response: Optional[Any]

    # id de secion de la ejcucion 
    session_id : Optional[str]
    
    # Email del usuario para organizacion de carpetas
    user_email: Optional[str]
    
    # Historial de generaciones
    generation_history: Optional[List[GenerationItem]]