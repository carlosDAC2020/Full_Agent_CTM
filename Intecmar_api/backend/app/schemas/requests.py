from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class IngestRequest(BaseModel):
    text: str

class SelectionRequest(BaseModel):
    session_id: str
    selected_idea: dict

class NextStepRequest(BaseModel):
    session_id: str

class ConvocatoriaOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    source: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[datetime] = None
    fecha_inicio: Optional[date] = None
    deadline: Optional[datetime] = None
    fecha_cierre: Optional[date] = None
    type_financy: Optional[str] = None
    monto: Optional[str] = None
    requisitos: Optional[list] = None
    beneficios: Optional[list] = None
    lugar: Optional[str] = None

    class Config:
        from_attributes = True