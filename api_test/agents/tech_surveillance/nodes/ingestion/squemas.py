
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

class IngestionResult(BaseModel):
    """Result of the ingestion process, containing potential Call Info."""
    call_info: Optional[CallInfo] = Field(default=None, description="Extracted Call for Proposals info, if present.")