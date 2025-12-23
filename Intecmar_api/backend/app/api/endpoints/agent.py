import os
import shutil
import tempfile
from fastapi import File, UploadFile, Form

import uuid
from fastapi import APIRouter
from backend.app.schemas.requests import IngestRequest, SelectionRequest, NextStepRequest
from backend.app.workers.tech_surveillance.tasks import task_process_agent_step

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from backend.app.db.session import get_db
from backend.app.db.history import AgentSession, AgentStep
from backend.app.core.security import get_current_user
from backend.app.db.models import User

import json
from typing import List
from backend.app.services.tech_surveillance.storage import MinioService
from backend.app.db.models import Convocatoria
from backend.app.schemas.requests import IngestRequest, SelectionRequest, NextStepRequest, ConvocatoriaOut

router = APIRouter(prefix="/agent", tags=["Agent Actions"])
storage_service = MinioService()

@router.get("/convocatorias", response_model=List[ConvocatoriaOut])
async def list_convocatorias(db: Session = Depends(get_db)):
    """Lista todas las convocatorias guardadas en la base de datos."""
    rows = db.query(Convocatoria).order_by(Convocatoria.created_db_at.desc()).all()
    return rows

@router.post("/ingest")
async def start_ingest(
    text: str = Form(...),
    files: List[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session_id = str(uuid.uuid4())
    
    # Create session in database with user_id
    session = AgentSession(
        id=session_id,
        user_id=current_user.id,
        status="active"
    )
    db.add(session)
    db.commit()

    # Upload files to context folder
    context_docs_paths = []
    if files:
        for file in files:
            # Create a temporary file to save the uploaded content
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = tmp.name
            
            try:
                # Upload to MinIO in 'context' subfolder
                object_key = storage_service.upload_file(tmp_path, session_id, subfolder="context")
                if object_key:
                    context_docs_paths.append(object_key)
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
    
    task = task_process_agent_step.delay(
        session_id=session_id, 
        input_data={
            "text": text, 
            "user_email": current_user.email,
            "context_docs": context_docs_paths
        }, 
        step_type="ingest"
    )
    return {"task_id": task.id, "session_id": session_id}

@router.post("/generate-ideas")
async def generate_ideas(
    request: NextStepRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify session belongs to user
    session = db.query(AgentSession).filter(
        AgentSession.id == request.session_id,
        AgentSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or access denied")
    
    task = task_process_agent_step.delay(
        session_id=request.session_id, 
        input_data={"user_email": current_user.email}, 
        step_type="proposal_ideas"
    )
    return {"task_id": task.id, "session_id": request.session_id}

@router.post("/select-idea")
async def select_idea(
    request: SelectionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify session belongs to user
    session = db.query(AgentSession).filter(
        AgentSession.id == request.session_id,
        AgentSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or access denied")
    
    task = task_process_agent_step.delay(
        session_id=request.session_id, 
        input_data={"selected_idea": request.selected_idea, "user_email": current_user.email}, 
        step_type="project_idea"
    )
    return {"task_id": task.id, "session_id": request.session_id}

@router.post("/finalize")
async def finalize_project(
    request: NextStepRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify session belongs to user
    session = db.query(AgentSession).filter(
        AgentSession.id == request.session_id,
        AgentSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or access denied")
    
    task = task_process_agent_step.delay(
        session_id=request.session_id, 
        input_data={"user_email": current_user.email}, 
        step_type="generate_project"
    )
    return {"task_id": task.id, "session_id": request.session_id}



@router.get("/history/{session_id}")
async def get_session_history(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Recupera el estado de una sesión para restaurar el Frontend"""
    
    # 1. Buscar la sesión y verificar que pertenece al usuario
    session = db.query(AgentSession).filter(
        AgentSession.id == session_id,
        AgentSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada o acceso denegado")

    # 2. Buscar todos los pasos ejecutados
    steps = db.query(AgentStep).filter(AgentStep.session_id == session_id).all()
    
    # 3. Determinar el estado actual
    history_map = {}
    
    for step in steps:
        step_data = step.output_data
        
        # PROCESAMIENTO DE URLs DE MINIO (Firma)
        # Y new_state tiene todo acumulado. 
        # Así que 'ingest' puede tener 'docs_paths' si se generaron ahí (el grafo dice 'presentation_generator' -> 'ingest'? No, es paralelo o secuencial).
        # En tu grafo, 'ingest' -> 'presentation_generator' -> ...
        # El paso guardado es 'ingest' y luego 'presentation_generator'.
        
        # Si step.step_type es 'ingest' o 'presentation_generator' o cualquiera que tenga docs_paths...
        # Como el estado SE ACUMULA, el último paso tendrá todo. Pero los pasos intermedios también tienen su snapshot.
        # Si el frontend usa history_map['ingest'], espera ver los docs ahí?
        # El frontend usa: if(stepsMap['ingest']) { renderStep1Result(stepsMap['ingest']); }
        
        # Así que debemos procesar CADA paso en el history_map porsiaca el frontend lee de uno específico.
        
        if step_data and isinstance(step_data, dict):
            if "docs_paths" in step_data and step_data["docs_paths"]:
                docs = step_data["docs_paths"]
                for key, val in docs.items():
                     if val and isinstance(val, str) and "/" in val: 
                         docs[key] = storage_service.get_presigned_url(val)
                step_data["docs_paths"] = docs
                
            # Si el step data es string (a veces pasa por serialización doble accidental), parsear, firmar, stringificar.
            # Pero en la DB 'output_data' es JSONB (Postgres) o JSON. Asumimos dict.
        
        history_map[step.step_type] = step_data

    response = {
        "session_id": session_id,
        "status": session.status,
        "created_at": session.created_at,
        "steps_data": history_map,
        "last_step": steps[-1].step_type if steps else None
    }
    
    return response
