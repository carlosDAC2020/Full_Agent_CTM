"""
Router para gestionar sesiones del agente.
Proporciona endpoints para listar el historial de sesiones.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.db.session import get_db
from backend.app.db.history import AgentSession, AgentStep
from backend.app.db.models import User
from backend.app.core.security import get_current_user  

router = APIRouter(prefix="/agent_sessions", tags=["Sessions"])


@router.get("")
async def list_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas las sesiones del usuario autenticado ordenadas por fecha de creación.
    Incluye un preview del título basado en los datos de ingesta.
    """
    sessions = db.query(AgentSession).filter(
        AgentSession.user_id == current_user.id
    ).order_by(desc(AgentSession.created_at)).limit(50).all()
    
    result = []
    for session in sessions:
        # Intentar extraer un título preview de los datos de ingesta
        title_preview = "Nueva Evaluación"
        
        ingest_step = db.query(AgentStep).filter(
            AgentStep.session_id == session.id,
            AgentStep.step_type == "ingest"
        ).first()
        
        if ingest_step and ingest_step.output_data:
            try:
                # Extraer título de la convocatoria si existe
                call_info = ingest_step.output_data.get("call_info", {})
                if isinstance(call_info, dict):
                    title_preview = call_info.get("title", "Convocatoria")[:50]
                    if len(call_info.get("title", "")) > 50:
                        title_preview += "..."
            except Exception:
                pass
        
        # Obtener el último paso ejecutado
        last_step_record = db.query(AgentStep).filter(
            AgentStep.session_id == session.id
        ).order_by(desc(AgentStep.created_at)).first()
        
        last_step = last_step_record.step_type if last_step_record else None
        
        result.append({
            "id": session.id,
            "status": session.status,
            "created_at": session.created_at.isoformat() if session.created_at else None,
            "title_preview": title_preview,
            "last_step": last_step  # Nuevo campo
        })
    
    return result


@router.delete("/{session_id}")
async def delete_session(session_id: str, db: Session = Depends(get_db)):
    """
    Elimina una sesión y todos sus pasos asociados.
    """
    from fastapi import HTTPException
    
    # Verificar que la sesión existe
    session = db.query(AgentSession).filter(AgentSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    # Eliminar todos los pasos asociados
    db.query(AgentStep).filter(AgentStep.session_id == session_id).delete()
    
    # Eliminar la sesión
    db.delete(session)
    db.commit()
    
    return {"message": "Sesión eliminada correctamente", "session_id": session_id}



@router.get("/{session_id}/steps")
async def get_session_steps(session_id: str, db: Session = Depends(get_db)):
    """
    Obtiene los pasos ejecutados de una sesión con sus datos de salida.
    Útil para mostrar qué pasos están completados y permitir navegación.
    """
    steps = db.query(AgentStep).filter(
        AgentStep.session_id == session_id
    ).order_by(AgentStep.created_at).all()
    
    return [
        {
            "step_type": step.step_type,
            "created_at": step.created_at.isoformat() if step.created_at else None,
            "has_output": step.output_data is not None
        }
        for step in steps
    ]
