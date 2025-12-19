from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class GenerateRequest(BaseModel):
    tema: Optional[str] = None

class SavedCreate(BaseModel):
    item_ref: str
    metadata: Optional[Dict[str, Any]] = None

class IdsRequest(BaseModel):
    ids: List[int]
    title: Optional[str] = None
