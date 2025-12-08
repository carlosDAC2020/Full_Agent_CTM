import uuid
from fastapi import APIRouter
from src.schemas.requests import IngestRequest, SelectionRequest, NextStepRequest
from src.tasks.agent_tasks import task_process_agent_step

router = APIRouter(prefix="/api/agent", tags=["Agent Actions"])

@router.post("/ingest")
async def start_ingest(request: IngestRequest):
    session_id = str(uuid.uuid4())
    task = task_process_agent_step.delay(
        session_id=session_id, 
        input_data={"text": request.text}, 
        step_type="ingest"
    )
    return {"task_id": task.id, "session_id": session_id}

@router.post("/generate-ideas")
async def generate_ideas(request: NextStepRequest):
    task = task_process_agent_step.delay(
        session_id=request.session_id, 
        input_data={}, 
        step_type="proposal_ideas"
    )
    return {"task_id": task.id, "session_id": request.session_id}

@router.post("/select-idea")
async def select_idea(request: SelectionRequest):
    task = task_process_agent_step.delay(
        session_id=request.session_id, 
        input_data={"selected_idea": request.selected_idea}, 
        step_type="project_idea"
    )
    return {"task_id": task.id, "session_id": request.session_id}

@router.post("/finalize")
async def finalize_project(request: NextStepRequest):
    task = task_process_agent_step.delay(
        session_id=request.session_id, 
        input_data={}, 
        step_type="generate_project"
    )
    return {"task_id": task.id, "session_id": request.session_id}