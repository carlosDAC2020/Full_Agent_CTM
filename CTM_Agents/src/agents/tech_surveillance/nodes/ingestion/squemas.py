# squemas.py

from pydantic import BaseModel, Field

class ProjectInfo(BaseModel):
    """Structured information extracted from a user's project description."""
    title: str = Field(
        description="A clear and descriptive title for the project. It should capture the main subject and goal."
    )
    description: str = Field(
        description="A concise summary of the project (2-4 sentences). It should explain the main objective, the technology involved, and the desired outcome."
    )
    # NUEVO CAMPO SUGERIDO:
    keywords: list[str] = Field(
        description="A list of 3-5 relevant keywords or technologies mentioned in the text (e.g., 'AI', 'Maintenance 5.0', 'Naval Industry')."
    )