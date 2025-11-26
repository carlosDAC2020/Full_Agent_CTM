# squemas.py

from pydantic import BaseModel, Field
from typing import Optional, List

class CallInfo(BaseModel):
    """Structured information extracted from a Call for Proposals (Convocatoria)."""
    title: Optional[str] = Field(default=None, description="Title of the Call/Convocatoria.")
    objective: Optional[str] = Field(default=None, description="Main objective of the call.")
    funding: Optional[str] = Field(default=None, description="Funding details (amount, type).")
    keywords: Optional[List[str]] = Field(default=None, description="Keywords related to the call.")
    important_dates: Optional[str] = Field(default=None, description="Start and end dates.")
    benefits: Optional[List[str]] = Field(default=None, description="List of benefits.")
    url: Optional[str] = Field(default=None, description="URL for more info.")

class ProjectInfo(BaseModel):
    """Structured information extracted from a user's project description."""
    title: str = Field(
        description="A clear and descriptive title for the project. It should capture the main subject and goal."
    )
    description: str = Field(
        description="A concise summary of the project (2-4 sentences). It should explain the main objective, the technology involved, and the desired outcome."
    )
    keywords: list[str] = Field(
        description="A list of 3-5 relevant keywords or technologies mentioned in the text (e.g., 'AI', 'Maintenance 5.0', 'Naval Industry')."
    )

class IngestionResult(BaseModel):
    """Result of the ingestion process, containing potential Call Info and Project Info."""
    call_info: Optional[CallInfo] = Field(default=None, description="Extracted Call for Proposals info, if present.")
    project_info: ProjectInfo = Field(description="Extracted or GENERATED project info.")
    is_generated_project: bool = Field(default=False, description="True if the project info was generated/invented based on the call, False if provided by user.")