from pydantic import BaseModel
from typing import Optional

class SourcesSearchRequest(BaseModel):
    query: str

class SourcesAISearchRequest(BaseModel):
    tema: Optional[str] = None

class SourceCreate(BaseModel):
    name: str
    type: Optional[str] = None
    url: str

class SourceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None
    hidden: Optional[bool] = None
