from pydantic import BaseModel, Field

class RouteQuery(BaseModel):
    """Clasifica la intención del usuario."""
    decision: Literal["PROYECTO", "CHAT"] = Field(
        description="La decisión sobre a dónde enrutar el mensaje del usuario. Debe ser 'PROYECTO' o 'CHAT'."
    )