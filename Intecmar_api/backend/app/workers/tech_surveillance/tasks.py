import asyncio
import os 
import json
import redis
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage

from backend.app.workers.tech_surveillance.celery_app import celery_app
from backend.agent.tech_surveillance.graph import agent 

# --- IMPORTACIONES DE TU AGENTE ---
from backend.agent.tech_surveillance.state import (
    CallInfo, 
    ReportSchema, 
    DocsPaths, 
    proposalIdeaResponse, 
    ProposalIdea,
    GeneralInfo,
    GenerationConfig,
    GraphState
)

# --- IMPORTACIONES DE BASE DE DATOS ---
from backend.app.db.session import SessionLocal
from backend.app.db.history import AgentSession, AgentStep
from backend.app.db.models import User 

# Cliente Redis
redis_url = os.getenv("CELERY_BROKER_URL", "redis://shared_redis:6379/0")

# Usamos from_url para que parseé host, puerto y db automáticamente
redis_client = redis.from_url(redis_url)

# --- MAPEO DE NODOS A MENSAJES DE USUARIO ---
# Estos keys coinciden exactamente con los definidos en tu graph.py
NODE_MESSAGES = {
    "ingest": "📥 Analizando convocatoria y extrayendo datos clave...",
    "presentation_generator": "📝 Generando resumen ejecutivo para la presentación...",
    "presentation_generator_docs": "📊 Diseñando diapositivas y documentos base...",
    "propose_ideas": "💡 Brainstorming: Generando ideas de proyectos innovadores...",
    "proyect_idea": "📐 Estructurando el esquema conceptual del proyecto...",
    "project_idea_doc": "📄 Generando documento PDF del esquema preliminar...",
    "academic_research": "🔍 Realizando investigación académica y estado del arte...",
    "project_schemas": "✍️ Redactando contenido técnico (Metodología, Justificación, Riesgos)...",
    "images_generator": "🎨 Diseñando póster promocional con IA Generativa...",
    "report": "📑 Ensamblando reporte final y propuesta técnica...",
    "vectorizer": "📚 Indexando documentos y conocimientos..."
}

def json_serializer(obj):
    """Serializador maestro para Redis/DB"""
    if hasattr(obj, 'model_dump'):
        return obj.model_dump()
    if hasattr(obj, 'dict'):
        return obj.dict()
    if hasattr(obj, 'content'):
        return obj.content
    return str(obj)

async def run_agent_stream(input_state: dict, task_instance):
    """
    Ejecuta el agente paso a paso (Streaming) y actualiza el estado de Celery.
    """
    # Copia del estado inicial para ir acumulando cambios
    final_state = input_state.copy()
    
    # Usamos astream para recibir eventos por cada nodo que termina
    print(f"--- Iniciando Streaming del Agente ---")
    
    async for event in agent.astream(input_state):
        for node_name, node_output in event.items():
            # 1. Actualizar nuestro estado local con la salida del nodo
            if isinstance(node_output, dict):
                final_state.update(node_output)
            
            # 2. Buscar mensaje amigable para el usuario
            # Si el nodo es un subgrafo, a veces el nombre viene distinto, pero capturamos los principales
            status_msg = NODE_MESSAGES.get(node_name, f"Procesando: {node_name}...")
            
            # 3. Log para depuración
            print(f"--> Nodo terminado: {node_name}")
            
            # 4. Actualizar estado en Celery (PROGRESS)
            # Esto permite al frontend leer 'info.message'
            if task_instance:
                task_instance.update_state(
                    state='PROGRESS', 
                    meta={'message': status_msg}
                )

    return final_state

@celery_app.task(bind=True, name="backend.app.workers.tech_surveillance.tasks.process_agent_step")
def task_process_agent_step(self, session_id: str, input_data: dict, step_type: str):
    """
    Tarea Celery principal.
    bind=True permite acceder a 'self' para actualizar el estado.
    """
    
    print(f"🏁 STARTING TASK task_process_agent_step: step_type={step_type}")
    print(f"🔍 DEBUG INPUT DATA: {json.dumps(input_data, default=str)}")

    # ==========================================
    # 1. GESTIÓN DE BASE DE DATOS (SESIÓN)
    # ==========================================
    db = SessionLocal()
    if step_type == "ingest":
        try:
            existing = db.query(AgentSession).filter(AgentSession.id == session_id).first()
            if not existing:
                new_session = AgentSession(id=session_id, status="active")
                db.add(new_session)
                db.commit()
        except Exception as e:
            print(f"⚠️ Error creando sesión en DB: {e}")
            db.rollback()
    
    # ==========================================
    # 2. RECUPERAR Y REHIDRATAR ESTADO (DB PRIMERO, LUEGO REDIS)
    # ==========================================
    current_state = {}
    
    # CAMBIO: Primero intentamos DB (más confiable y completo)
    try:
        last_step = db.query(AgentStep).filter(
            AgentStep.session_id == session_id
        ).order_by(AgentStep.created_at.desc()).first()
        
        if last_step and last_step.output_data:
            print(f"✅ Estado recuperado de DB para sesión: {session_id}")
            current_state = last_step.output_data
    except Exception as e:
        print(f"⚠️ Error recuperando estado de DB: {e}")
    
    # Fallback a Redis solo si DB no tiene nada
    if not current_state:
        stored_state = redis_client.get(f"agent_state:{session_id}")
        if stored_state:
            print(f"🔄 Estado recuperado de Redis (fallback) para sesión: {session_id}")
            current_state = json.loads(stored_state)
        else:
            print(f"⚠️ No se encontró estado previo para sesión: {session_id}")

    # --- REHIDRATACIÓN PYDANTIC ---
    # Convertimos diccionarios a objetos Pydantic si es necesario
    
    if current_state:
        # 1. call_info
        if "call_info" in current_state and current_state["call_info"]:
            if isinstance(current_state["call_info"], dict):
                try: 
                    current_state["call_info"] = CallInfo(**current_state["call_info"])
                except Exception as e:
                    print(f"⚠️ Error rehydrating call_info: {e}")

        # 2. report_components
        if "report_components" in current_state and isinstance(current_state["report_components"], dict):
            try: 
                current_state["report_components"] = ReportSchema(**current_state["report_components"])
                # DEBUG: Log general_info status
                rc = current_state["report_components"]
                if rc.general_info:
                    print(f"✅ REHYDRATE report_components.general_info: title='{rc.general_info.project_title}', desc='{str(rc.general_info.project_description)[:50]}...'")
                else:
                    print("⚠️ REHYDRATE report_components: general_info is None")
            except Exception as e:
                print(f"⚠️ Error rehydrating report_components: {e}")

        # 3. docs_paths
        if "docs_paths" in current_state and isinstance(current_state["docs_paths"], dict):
            try: current_state["docs_paths"] = DocsPaths(**current_state["docs_paths"])
            except: pass
        
        # 4. proposal_ideas (Response wrapper)
        if "proposal_ideas" in current_state and isinstance(current_state["proposal_ideas"], dict):
            try: current_state["proposal_ideas"] = proposalIdeaResponse(**current_state["proposal_ideas"])
            except: pass

        # 5. selected_idea
        if "selected_idea" in current_state and isinstance(current_state["selected_idea"], dict):
            si = current_state["selected_idea"]
            # Robust mapping for frontend compatibility
            if "title" in si and not si.get("idea_title"): si["idea_title"] = si.get("title")
            if "desc" in si and not si.get("idea_description"): si["idea_description"] = si.get("desc")
            if "objectives" in si and not si.get("idea_objectives"): si["idea_objectives"] = si.get("objectives")
            try: 
                current_state["selected_idea"] = ProposalIdea(**si)
            except Exception as e:
                print(f"⚠️ Error rehydrating selected_idea: {e}")
        
        # 6. RECUPERACIÓN PARA SESIONES ANTIGUAS: Si no hay selected_idea pero sí hay initial_schema
        if "selected_idea" not in current_state or not current_state["selected_idea"]:
            # Intentar recuperar de report_components.general_info
            if "report_components" in current_state:
                rc = current_state["report_components"]
                if hasattr(rc, "general_info") and rc.general_info:
                    gi = rc.general_info
                    if gi.project_title or gi.project_description:
                        print("🔧 Recuperando selected_idea de report_components.general_info")
                        current_state["selected_idea"] = ProposalIdea(
                            idea_title=gi.project_title,
                            idea_description=gi.project_description,
                            idea_objectives=[]
                        )

    # Inyectar Session ID
    current_state["session_id"] = session_id

    # DEBUG
    print(f"🔍 DEBUG STATE ({step_type}): CallInfo Presente? {'call_info' in current_state}")
    if 'call_info' in current_state:
        # Avoid printing huge objects if they have history
        ci_summary = f"Title: {getattr(current_state['call_info'], 'title', 'N/A')}"
        print(f"🔍 DEBUG CallInfo Summary: {ci_summary}")

    # ==========================================
    # 3. PREPARAR INPUT
    # ==========================================
    if step_type == "ingest":
        current_state["messages"] = [HumanMessage(content=input_data["text"])]
        current_state["route_decision"] = "ingest"
        if "user_email" in input_data:
             current_state["user_email"] = input_data["user_email"]
        
        # Inyectar documentos de contexto si existen
        if "context_docs" in input_data and input_data["context_docs"]:
            if "call_info" not in current_state or not current_state["call_info"]:
                current_state["call_info"] = CallInfo()
            
            call_info = current_state["call_info"]
            if hasattr(call_info, "__setattr__") and not isinstance(call_info, dict):
                # Es un objeto Pydantic
                call_info.context_docs = input_data["context_docs"]
            else:
                # Es un diccionario
                call_info["context_docs"] = input_data["context_docs"]
    
    # Asegurar que user_email se preserva o actualiza si viene en input (para reanudaciones)
    if "user_email" in input_data and not current_state.get("user_email"):
        current_state["user_email"] = input_data["user_email"]
    
    # NUEVO: Lógica para iniciar investigación profunda
    elif step_type == "research":
        current_state["route_decision"] = "research"

    # NUEVO: Lógica para añadir documentos y vectorizar
    elif step_type == "append_docs":
        current_state["route_decision"] = "vectorize"
        
        # Añadir nuevos docs a la lista existente
        if "context_docs" in input_data and input_data["context_docs"]:
            # Inicializar si no existe
            if "call_info" not in current_state or not current_state["call_info"]:
                 current_state["call_info"] = CallInfo()
            
            call_info = current_state["call_info"]
            
            # Helper para obtener/setear lista
            if isinstance(call_info, dict):
                current_list = call_info.get("context_docs") or []
                current_list.extend(input_data["context_docs"])
                call_info["context_docs"] = current_list
            else:
                # Objeto Pydantic
                if not call_info.context_docs:
                    call_info.context_docs = []
                call_info.context_docs.extend(input_data["context_docs"])
    
    elif step_type == "proposal_ideas":
        current_state["route_decision"] = "proposal_ideas"
        
        # FIXED: Check existence of key rather than truthiness (handles empty string case better)
        if "selected_thematic_line" in input_data:
            current_state["selected_thematic_line"] = input_data["selected_thematic_line"]
            print(f"✅ INJECTED selected_thematic_line: {input_data['selected_thematic_line']}")
            
        if "selected_methodology" in input_data:
            current_state["selected_methodology"] = input_data["selected_methodology"]
            print(f"✅ INJECTED selected_methodology: {input_data['selected_methodology']}")
    
    elif step_type == "project_idea":
        current_state["route_decision"] = "project_idea"
        if "selected_idea" in input_data:
            si = input_data["selected_idea"]
            # Robust mapping for input
            if "title" in si and not si.get("idea_title"): si["idea_title"] = si["title"]
            if "desc" in si and not si.get("idea_description"): si["idea_description"] = si["desc"]
            if "objectives" in si and not si.get("idea_objectives"): si["idea_objectives"] = si["objectives"]
            current_state["selected_idea"] = ProposalIdea(**si)
            
            # --- NUEVO: Inicializar GeneralInfo con la idea seleccionada inmediatamente ---
            # Esto asegura que si el siguiente nodo necesita esta info, ya esté ahí.
            if "report_components" not in current_state or not current_state["report_components"]:
                current_state["report_components"] = ReportSchema(
                    general_info=GeneralInfo(
                        project_title=si.get("idea_title"),
                        project_description=si.get("idea_description"),
                        duration_months=si.get("duration_time"),
                        executor_entity=si.get("executor_entity"),
                        executor_entity_logo=si.get("executor_entity_logo"),
                        coejecutors_entities=si.get("coejecutors_entities"),
                        coejecutors_entities_logos=si.get("coejecutors_entities_logos"),
                        collaborators_entities=si.get("collaborators_entities"),
                        collaborators_entities_logos=si.get("collaborators_entities_logos"),
                        keywords=current_state.get("call_info").keywords if "call_info" in current_state and current_state["call_info"] else []
                    )
                )
            else:
                rc = current_state["report_components"]
                if not rc.general_info:
                    rc.general_info = GeneralInfo()
                
                gi = rc.general_info
                gi.project_title = si.get("idea_title") or gi.project_title
                gi.project_description = si.get("idea_description") or gi.project_description
                gi.duration_months = si.get("duration_time") or gi.duration_months
                gi.executor_entity = si.get("executor_entity") or gi.executor_entity
                gi.executor_entity_logo = si.get("executor_entity_logo") or gi.executor_entity_logo
                gi.coejecutors_entities = si.get("coejecutors_entities") or gi.coejecutors_entities
                gi.coejecutors_entities_logos = si.get("coejecutors_entities_logos") or gi.coejecutors_entities_logos
                gi.collaborators_entities = si.get("collaborators_entities") or gi.collaborators_entities
                gi.collaborators_entities_logos = si.get("collaborators_entities_logos") or gi.collaborators_entities_logos

                # Intentar heredar palabras clave de la convocatoria si no hay
                if not gi.keywords and "call_info" in current_state and current_state["call_info"]:
                    gi.keywords = current_state["call_info"].keywords or []
            # -------------------------------------------------------------------------

            
    elif step_type == "generate_project":
        current_state["route_decision"] = "generate_proyect" # Typo intencional según tu grafo
        
        # Inject generation_config if provided
        if "generation_config" in input_data and input_data["generation_config"]:
            config_data = input_data["generation_config"]
            current_state["generation_config"] = GenerationConfig(**config_data)
            print(f"✅ INJECTED generation_config: {config_data}")

        # Ensure thematic line is preserved if present in state but not in general_info
        if "selected_thematic_line" in current_state and current_state["report_components"]:
            rc = current_state["report_components"]
            if rc.general_info and not rc.general_info.thematic_line:
                rc.general_info.thematic_line = current_state["selected_thematic_line"]
                print(f"✅ PERSISTED thematic_line: {rc.general_info.thematic_line}")
        
        # DEBUG: Verificar qué hay en el estado
        print(f"🔍 DEBUG (generate_project): selected_idea presente? {'selected_idea' in current_state}")
        if 'selected_idea' in current_state:
            print(f"🔍 DEBUG selected_idea: {current_state['selected_idea']}")
        
        print(f"🔍 DEBUG (generate_project): report_components presente? {'report_components' in current_state}")
        if 'report_components' in current_state:
            rc = current_state['report_components']
            if hasattr(rc, 'general_info'):
                print(f"🔍 DEBUG report_components.general_info: {rc.general_info}")
            else:
                print(f"🔍 DEBUG report_components (dict keys): {rc.keys() if isinstance(rc, dict) else 'Not a dict'}")

    # ==========================================
    # 4. EJECUTAR AGENTE (STREAMING)
    # ==========================================
    try:
        # CAMBIO: Usamos run_agent_stream en lugar de invoke directo
        # Pasamos 'self' para que pueda actualizar el estado de la tarea
        new_state = asyncio.run(run_agent_stream(current_state, self))
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error ejecutando agente: {error_msg}")
        
        # Mapeo de errores comunes para mensajes más limpios
        friendly_error = error_msg
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            friendly_error = "Cuota de IA excedida (Gemini). Por favor, intenta de nuevo en unos segundos."
        
        # ROLLBACK de estado en DB: Volver a 'active' para que el usuario pueda reintentar
        try:
            db_rollback = SessionLocal()
            session_rec = db_rollback.query(AgentSession).filter(AgentSession.id == session_id).first()
            if session_rec:
                session_rec.status = "active"
                session_rec.current_task_id = None
                db_rollback.commit()
            db_rollback.close()
        except Exception as db_err:
            print(f"⚠️ Error en rollback de DB: {db_err}")

        # Importante: devolvemos error para que el frontend lo sepa
        return {"status": "error", "error": friendly_error}

    # ==========================================
    # 5. GUARDAR ESTADO (REDIS)
    # ==========================================
    serialized_state = json.dumps(new_state, default=json_serializer)
    redis_client.set(f"agent_state:{session_id}", serialized_state)

    # ==========================================
    # 6. GUARDAR HISTORIAL (POSTGRES)
    # ==========================================
    try:
        clean_output_dict = json.loads(serialized_state)
        
        step_record = AgentStep(
            session_id=session_id,
            step_type=step_type,
            input_data=input_data,
            output_data=clean_output_dict,
            created_at=datetime.utcnow()
        )
        db.add(step_record)
        
        if step_type == "generate_project":
             session_record = db.query(AgentSession).filter(AgentSession.id == session_id).first()
             if session_record:
                 session_record.status = "completed"
                 session_record.current_task_id = None
        elif step_type in ["research", "ingest", "append_docs"]:
             session_record = db.query(AgentSession).filter(AgentSession.id == session_id).first()
             if session_record:
                 session_record.status = "active"
                 session_record.current_task_id = None

        db.commit()
    except Exception as e:
        print(f"⚠️ Error guardando en DB: {e}")
        db.rollback()
    finally:
        db.close()

    # ==========================================
    # 7. RETORNO FINAL
    # ==========================================
    return {
        "status": "completed", 
        "step": step_type, 
        "data": serialized_state 
    }