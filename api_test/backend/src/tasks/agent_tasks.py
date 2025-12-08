import asyncio
import json
from src.core.celery_app import celery_app
from src.agents.tech_surveillance.graph import agent 
from langchain_core.messages import HumanMessage
import redis

from src.core.database import SessionLocal
from src.models.history import AgentSession, AgentStep
from datetime import datetime

# Cliente Redis para guardar el estado intermedio del agente
redis_client = redis.Redis(host='redis', port=6379, db=0)

def json_serializer(obj):
    """Tu serializador del script original"""
    if hasattr(obj, 'model_dump'):
        return obj.model_dump()
    if hasattr(obj, 'dict'):
        return obj.dict()
    return str(obj)

async def run_agent_step(input_state: dict):
    """Ejecuta un paso del grafo"""
    result = await agent.ainvoke(input_state)
    return result

@celery_app.task(name="process_agent_step")
def task_process_agent_step(session_id: str, input_data: dict, step_type: str):
    """
    Tarea de Celery que maneja la lógica asíncrona del agente.
    Recupera el estado anterior de Redis (si existe), lo actualiza y corre el agente.
    """
    # 1. Crear sesión de DB (SQLAlchemy)
    db = SessionLocal()
    
    # Verificar si la "Session" existe en DB, si no, crearla (Caso primer paso: ingest)
    try:
        if step_type == "ingest":
            # Verificar si ya existe para evitar duplicados en reintentos
            existing_session = db.query(AgentSession).filter(AgentSession.id == session_id).first()
            if not existing_session:
                new_session = AgentSession(id=session_id, status="active")
                db.add(new_session)
                db.commit()
    except Exception as e:
        print(f"Error DB creando sesión: {e}")
        db.rollback()
    
    # 2. Recuperar estado previo si existe
    current_state = {}
    stored_state = redis_client.get(f"agent_state:{session_id}")
    if stored_state:
        current_state = json.loads(stored_state)
    
    # 3. Preparar el input según el paso (Ingesta, Selección, etc.)
    # Fusionamos el input nuevo con el estado actual
    if step_type == "ingest":
        current_state["messages"] = [HumanMessage(content=input_data["text"])]
        current_state["route_decision"] = "ingest"
        current_state["session_id"] = session_id 
    elif step_type == "proposal_ideas":
        current_state["route_decision"] = "proposal_ideas"
    elif step_type == "project_idea":
        current_state["route_decision"] = "project_idea"
        # Asumimos que input_data trae el índice o la idea seleccionada
        current_state["selected_idea"] = input_data.get("selected_idea")
    elif step_type == "generate_project":
        current_state["route_decision"] = "generate_proyect"

    # 4. Ejecutar el agente (wrapper asíncrono)
    try:
        new_state = asyncio.run(run_agent_step(current_state))
    except Exception as e:
        return {"status": "error", "error": str(e)}

    # 5. Serializar y guardar estado nuevo en Redis
    serialized_state = json.dumps(new_state, default=json_serializer)
    redis_client.set(f"agent_state:{session_id}", serialized_state)

    # 6. Retornar una versión limpia para el Frontend
    # (No retornes todo el estado gigante, solo lo necesario para la UI)
    try:
        # Preparamos los datos para guardar (cuidado con guardar JSONs gigantes)
        # Podrías filtrar el serialized_state para guardar solo lo importante
        
        step_record = AgentStep(
            session_id=session_id,
            step_type=step_type,
            input_data=input_data,     # JSONB en Postgres
            output_data=new_state,     # SQLAlchemy convierte dict a JSON automáticamente
            created_at=datetime.utcnow()
        )
        db.add(step_record)
        
        # Si es el último paso, marcamos la sesión como completada
        if step_type == "generate_project":
            session_record = db.query(AgentSession).filter(AgentSession.id == session_id).first()
            if session_record:
                session_record.status = "completed"
        
        db.commit()
        print(f"💾 Paso '{step_type}' guardado en DB para sesión {session_id}")

    except Exception as e:
        print(f"❌ Error guardando historial en DB: {e}")
        db.rollback()
    finally:
        db.close() # Importante cerrar la sesión

    # 3. Retornar respuesta al Frontend
    response = {
        "status": "completed",
        "step": step_type,
        "data": serialized_state 
    }
    return response