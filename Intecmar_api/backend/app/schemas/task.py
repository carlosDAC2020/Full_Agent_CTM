from pydantic import BaseModel
from typing import Optional, Dict, Any

class FlowStatusUpdate(BaseModel):
    status: str
    name: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

class TaskCreate(BaseModel):
    type: str
    payload: Optional[Dict[str, Any]] = None
