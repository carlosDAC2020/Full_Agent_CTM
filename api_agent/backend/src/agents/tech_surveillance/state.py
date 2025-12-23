from pydantic import BaseModel, Field
from typing import Optional, List, Annotated , Any
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
    main_entity: Optional[str] = Field(
        default=None, 
        description="Main entity")
    collaborating_entities: Optional[List[str]] = Field(
        default=None, 
        description="Collaborating entities separated by commas")

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
    content: Optional[str] = Field(
        default=None,
        description=(
            "The complete text for the Problem Statement and Justification section in Markdown. "
            "It should clearly define the problem, its magnitude, and why this project is necessary."
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
    funding: Optional[str] = Field(default=None, description="Información sobre financiamiento")
    keywords: Optional[List[str]] = Field(default=None, description="Palabras clave de la convocatoria")
    important_dates: Optional[str] = Field(default=None, description="Fechas importantes (inicio, cierre)")
    benefits: Optional[List[str]] = Field(default=None, description="Beneficios listados")
    url: Optional[str] = Field(default=None, description="URL de más información")
    context_docs: Optional[List[str]] = Field(default=None, description="Rutas de documentos de contexto subidos por el usuario")

class ProposalIdea(BaseModel):
    """Idea de proyecto propuesta por el usuario."""
    idea_title: Optional[str] = Field(default=None, description="Título de la idea de proyecto")
    idea_description: Optional[str] = Field(default=None, description="Descripción de la idea de proyecto") 
    idea_objectives: Optional[List[str]] = Field(default=None, description="5 objetivos de la idea de proyecto basadas en en la metodologia smart ")

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

# --- Estado Principal del Grafo (Híbrido: TypedDict + Pydantic) ---

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

    # resumen de presentacion
    presentation_summary : Optional[str]

    # esquema incial de dpocumento 
    initial_schema: Optional[str]

    # rutas de documentos generados
    docs_paths: Optional[DocsPaths]
    
    randonm_response: Optional[Any]

    # id de secion de la ejcucion 
    session_id : Optional[str]