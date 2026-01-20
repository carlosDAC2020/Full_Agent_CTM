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
from typing import List, Optional
from pydantic import BaseModel
from backend.app.services.core.storage import storage_service
from backend.app.db.models import Convocatoria

router = APIRouter(prefix="/agent", tags=["Agente I+D+i (Wizard)"])


class ConvocatoriaOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    keywords: Optional[list] = []
    source: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[str] = None  # se serializa como ISO
    fecha_inicio: Optional[str] = None
    deadline: Optional[str] = None
    fecha_cierre: Optional[str] = None
    type_financy: Optional[str] = None
    monto: Optional[str] = None
    requisitos: Optional[list] = []
    beneficios: Optional[list] = []
    lugar: Optional[str] = None

    class Config:
        from_attributes = True

@router.get("/convocatorias", response_model=List[ConvocatoriaOut], summary="Listar convocatorias", description="Obtiene todas las convocatorias guardadas en el sistema para ser usadas como base en una sesión del agente.")
async def list_convocatorias(db: Session = Depends(get_db)):
    """Lista todas las convocatorias guardadas en la base de datos."""
    rows = db.query(Convocatoria).order_by(Convocatoria.created_db_at.desc()).all()
    return rows

@router.post("/ingest", summary="Paso 1: Ingesta", description="Inicia una sesión del agente cargando un texto descriptivo o archivos (RAG). Devuelve el session_id y el primer task_id.")
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
        # Carpeta base para la sesión: user_email/Agent_Sessions/session_id
        session_base_path = f"{current_user.email}/Agent_Sessions/{session_id}"
        print(f"id de session: {session_base_path}")
        for file in files:
            # Create a temporary file to save the uploaded content
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = tmp.name
            
            try:
                # Upload to MinIO in 'context' subfolder
                object_key = storage_service.upload_file(tmp_path, session_base_path, subfolder="context")
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
    
    # Guardar task_id y actualizar status
    session.current_task_id = task.id
    session.status = "researching"
    db.commit()

    return {"task_id": task.id, "session_id": session_id}

@router.post("/generate-ideas", summary="Paso 2: Generar Ideas", description="Basado en la ingesta inicial, dispara el proceso de brainstorming para proponer ideas de proyectos técnicos.")
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

@router.post("/select-idea", summary="Paso 3: Seleccionar Idea", description="Confirma qué idea de las propuestas se desarrollará en el reporte técnico final.")
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

@router.post("/finalize", summary="Paso 5: Finalizar Proyecto", description="Genera el esquema final del proyecto, consolidando toda la investigación y visuales.")
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



@router.post("/research", summary="Paso 4: Investigación Profunda", description="Inicia la fase de investigación técnica utilizando herramientas externas como Arxiv y Semantic Scholar.")
async def start_research(
    request: NextStepRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Inicia la fase de investigación técnica profunda (Presentation Generation)."""
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
        step_type="research"
    )
    
    # Guardar task_id y actualizar status
    session.current_task_id = task.id
    session.status = "researching"
    db.commit()

    return {"task_id": task.id, "session_id": request.session_id}


@router.post("/append-docs", summary="Añadir documentos", description="Permite subir archivos adicionales a una sesión ya iniciada para ser procesados por el motor de RAG.")
async def append_documents(
    session_id: str = Form(...),
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sube documentos adicionales y re-ejecuta la vectorización."""
    # Verify session
    session = db.query(AgentSession).filter(
        AgentSession.id == session_id,
        AgentSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or access denied")

    # Upload files to context folder
    new_docs_paths = []
    if files:
        session_base_path = f"{current_user.email}/Agent_Sessions/{session_id}"
        print(f"📂 [APPEND] Subiendo docs a: {session_base_path}")
        for file in files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = tmp.name
            
            try:
                # Upload to MinIO
                object_key = storage_service.upload_file(tmp_path, session_base_path, subfolder="context")
                if object_key:
                    new_docs_paths.append(object_key)
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
    
    if not new_docs_paths:
        return {"status": "no_files_uploaded", "message": "No valid files received"}

    # Trigger vectorizer task with NEW docs
    task = task_process_agent_step.delay(
        session_id=session_id, 
        input_data={
            "user_email": current_user.email,
            "context_docs": new_docs_paths # Only passing new docs to append logic
        }, 
        step_type="append_docs"
    )
    return {"task_id": task.id, "session_id": session_id, "added_docs": len(new_docs_paths)}


@router.get("/history/{session_id}", summary="Recuperar sesión", description="Obtiene el estado completo y los datos de todos los pasos de una sesión específica para restaurar el wizard.")
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

    # 2. Buscar todos los pasos ejecutados (ORDENADOS por fecha)
    steps = db.query(AgentStep).filter(
        AgentStep.session_id == session_id
    ).order_by(AgentStep.created_at.asc()).all()
    
    # 3. Determinar el estado actual
    history_map = {}
    last_processed_data = None
    
    for step in steps:
        step_data = step.output_data
        
        if step_data and isinstance(step_data, dict):
            # 1. Docs Paths (Direct Keys)
            if "docs_paths" in step_data and step_data["docs_paths"]:
                docs = step_data["docs_paths"]
                for key, val in docs.items():
                     if val and isinstance(val, str) and "/" in val: 
                         # Usar el proxy para mayor estabilidad
                         docs[key] = f"/api/minio_agent/{val}"
                step_data["docs_paths"] = docs
            
            # 2. Call Info (Nested History and Context)
            if "call_info" in step_data and step_data["call_info"]:
                ci = step_data["call_info"]
                
                # Proxy Presentation History
                if "presentation_history" in ci and isinstance(ci["presentation_history"], list):
                    for entry in ci["presentation_history"]:
                        if "url" in entry and entry["url"] and "/" in entry["url"]:
                            if not entry["url"].startswith("/api/"):
                                entry["url"] = f"/api/minio_agent/{entry['url']}"
                
                # Proxy Context Docs
                if "context_docs" in ci and isinstance(ci["context_docs"], list):
                    for i, doc in enumerate(ci["context_docs"]):
                        if isinstance(doc, str) and "/" in doc:
                            url = f"/api/minio_agent/{doc}"
                            ci["context_docs"][i] = {"name": os.path.basename(doc), "url": url}
                        elif isinstance(doc, dict) and "url" in doc and "/" in doc["url"]:
                            if not doc["url"].startswith("/api/"):
                                doc["url"] = f"/api/minio_agent/{doc['url']}"
                
                step_data["call_info"] = ci
            
            last_processed_data = step_data
        
        history_map[step.step_type] = step_data

    response = {
        "session_id": session_id,
        "status": session.status,
        "current_task_id": session.current_task_id,
        "created_at": session.created_at,
        "steps_data": history_map,
        "latest_data": last_processed_data,
        "last_step": steps[-1].step_type if steps else None
    }
    
    return response
