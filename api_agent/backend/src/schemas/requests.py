from pydantic import BaseModel

class IngestRequest(BaseModel):
    text: str

class SelectionRequest(BaseModel):
    session_id: str
    selected_idea: dict

class NextStepRequest(BaseModel):
    session_id: str