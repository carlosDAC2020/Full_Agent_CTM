from pydantic import BaseModel, Field


class ProjectInfo(BaseModel):
    """Información extraída de la descripción de un proyecto."""
    title: str = Field(description="Un título conciso y descriptivo para el proyecto.")
    description: str = Field(description="Una descripción de una sola frase que resuma el objetivo principal del proyecto.")
