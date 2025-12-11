import uuid
from fastapi import APIRouter
from src.schemas.requests import IngestRequest, SelectionRequest, NextStepRequest
from src.tasks.agent_tasks import task_process_agent_step

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from src.core.database import get_db
from src.models.history import AgentSession, AgentStep

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


@router.get("/history/{session_id}")
async def get_session_history(session_id: str, db: Session = Depends(get_db)):
    """Recupera el estado de una sesión para restaurar el Frontend"""
    
    # 1. Buscar la sesión
    session = db.query(AgentSession).filter(AgentSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    # 2. Buscar todos los pasos ejecutados
    steps = db.query(AgentStep).filter(AgentStep.session_id == session_id).all()
    
    # 3. Determinar el estado actual
    # Convertimos los pasos a un diccionario para acceso rápido
    # step_type -> output_data
    history_map = {step.step_type: step.output_data for step in steps}
    
    response = {
        "session_id": session_id,
        "status": session.status,
        "created_at": session.created_at,
        "steps_data": history_map,
        "last_step": steps[-1].step_type if steps else None
    }
    
    return response
