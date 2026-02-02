import os
import shutil
import tempfile
from fastapi import File, UploadFile, Form

import uuid
from fastapi import APIRouter
from backend.app.schemas.requests import IngestRequest, SelectionRequest, NextStepRequest, IdeaGenerationRequest
from backend.app.workers.tech_surveillance.tasks import task_process_agent_step

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from backend.app.db.session import get_db
from backend.app.db.history import AgentSession, AgentStep
from backend.app.core.security import get_current_user
from backend.app.db.models import User

import json
from typing import List, Optional, Union
from pydantic import BaseModel
from datetime import datetime, date
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
    created_at: Optional[Union[datetime, date, str]] = None
    fecha_inicio: Optional[Union[datetime, date, str]] = None
    deadline: Optional[Union[datetime, date, str]] = None
    fecha_cierre: Optional[Union[datetime, date, str]] = None
    type_financy: Optional[str] = None
    monto: Optional[str] = None
    requisitos: Optional[Union[list, str]] = []
    beneficios: Optional[Union[list, str]] = []
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
                full_key = f"{session_base_path}/context/{file.filename}"
                object_key = storage_service.upload_file(tmp_path, full_key)
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
    request: IdeaGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # DEBUG: Log para ver qué recibe el backend
    print(f"📥 RECEIVED /generate-ideas request:")
    print(f"   session_id: {request.session_id}")
    print(f"   selected_thematic_line: {request.selected_thematic_line}")
    print(f"   selected_methodology: {request.selected_methodology}")
    
    # Verify session belongs to user
    session = db.query(AgentSession).filter(
        AgentSession.id == request.session_id,
        AgentSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or access denied")
    
    task = task_process_agent_step.delay(
        session_id=request.session_id, 
        input_data={
            "user_email": current_user.email,
            "selected_thematic_line": request.selected_thematic_line,
            "selected_methodology": request.selected_methodology
        }, 
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
        input_data={
            "user_email": current_user.email,
            "generation_config": request.generation_config
        }, 
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
                full_key = f"{session_base_path}/context/{file.filename}"
                object_key = storage_service.upload_file(tmp_path, full_key)
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


@router.post("/upload-alliance-logo", summary="Subir logo de alianza", description="Sube un logo de entidad aliada (ejecutor, coejecutor, colaborador) a la carpeta de la sesión.")
async def upload_alliance_logo(
    session_id: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sube un logo de alianza a MinIO en la carpeta alianzas/ de la sesión."""
    # Verificar que la sesión pertenece al usuario
    session = db.query(AgentSession).filter(
        AgentSession.id == session_id,
        AgentSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or access denied")
    
    # Generar nombre único para evitar colisiones
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".png"
    unique_name = f"{uuid.uuid4().hex[:8]}_{file.filename}"
    
    # Ruta en MinIO: {email}/Agent_Sessions/{session_id}/alianzas/{unique_name}
    minio_path = f"{current_user.email}/Agent_Sessions/{session_id}/alianzas/{unique_name}"
    
    # Guardar temporalmente y subir
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    
    try:
        object_key = storage_service.upload_file(tmp_path, minio_path)
        if not object_key:
            raise HTTPException(status_code=500, detail="Error uploading file to storage")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    
    return {
        "path": object_key,
        "url": f"/api/minio_agent/{object_key}",
        "filename": unique_name
    }


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
                        # Proxy url, pdf, pptx, md
                        for field in ["url", "pdf", "pptx", "md"]:
                            if field in entry and entry[field] and "/" in entry[field]:
                                if not entry[field].startswith("/api/"):
                                    entry[field] = f"/api/minio_agent/{entry[field]}"
                
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
            
            # 3. Selected Idea & General Info Alliance Logos
            # Para general_info en report_components
            if "report_components" in step_data and step_data["report_components"]:
                rc = step_data["report_components"]
                if "general_info" in rc and rc["general_info"]:
                    gi = rc["general_info"]
                    # Proxy executor logo
                    if gi.get("executor_entity_logo") and "/" in gi["executor_entity_logo"]:
                        if not gi["executor_entity_logo"].startswith("/api/"):
                            gi["executor_entity_logo"] = f"/api/minio_agent/{gi['executor_entity_logo']}"
                    
                    # Proxy coexecutors logos
                    if gi.get("coejecutors_entities_logos") and isinstance(gi["coejecutors_entities_logos"], list):
                        gi["coejecutors_entities_logos"] = [
                            f"/api/minio_agent/{logo}" if logo and "/" in logo and not str(logo).startswith("/api/") else logo 
                            for logo in gi["coejecutors_entities_logos"]
                        ]
                    
                    # Proxy collaborators logos
                    if gi.get("collaborators_entities_logos") and isinstance(gi["collaborators_entities_logos"], list):
                        gi["collaborators_entities_logos"] = [
                            f"/api/minio_agent/{logo}" if logo and "/" in logo and not str(logo).startswith("/api/") else logo 
                            for logo in gi["collaborators_entities_logos"]
                        ]
                    rc["general_info"] = gi
                step_data["report_components"] = rc

            # Para selected_idea directo
            if "selected_idea" in step_data and step_data["selected_idea"]:
                si = step_data["selected_idea"]
                if isinstance(si, dict):
                    if si.get("executor_entity_logo") and "/" in si["executor_entity_logo"]:
                        if not si["executor_entity_logo"].startswith("/api/"):
                            si["executor_entity_logo"] = f"/api/minio_agent/{si['executor_entity_logo']}"
                    
                    if si.get("coejecutors_entities_logos") and isinstance(si["coejecutors_entities_logos"], list):
                        si["coejecutors_entities_logos"] = [
                            f"/api/minio_agent/{logo}" if logo and "/" in logo and not str(logo).startswith("/api/") else logo 
                            for logo in si["coejecutors_entities_logos"]
                        ]
                    
                    if si.get("collaborators_entities_logos") and isinstance(si["collaborators_entities_logos"], list):
                        si["collaborators_entities_logos"] = [
                            f"/api/minio_agent/{logo}" if logo and "/" in logo and not str(logo).startswith("/api/") else logo 
                            for logo in si["collaborators_entities_logos"]
                        ]
                    step_data["selected_idea"] = si
            
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
