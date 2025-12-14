# backend/main_api.py
import os
import sys
import json
from dotenv import load_dotenv
from datetime import datetime
import time

import smtplib
from email.message import EmailMessage
import mimetypes


# IMPORTANTE: Cargar las variables de entorno ANTES de importar el agente
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Permitir ejecutar este archivo como script: `python backend/main_api.py`
# Agregar la carpeta raíz del proyecto al sys.path para poder importar `backend.*`
_CUR_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.abspath(os.path.join(_CUR_DIR, '..'))
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union, Tuple
from pathlib import Path as SysPath
from fpdf import FPDF
import requests
from bs4 import BeautifulSoup
import re
import shutil
import json
from urllib.parse import urlparse
import asyncio
from backend.celery_app import celery_app
from backend.db.session import Base, engine
from backend.db import models as _db_models  # ensure models are registered
from backend.auth import router as auth_router
from backend.auth import get_current_user
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.db import models

# Redis for task state and SSE pub/sub
try:
    from redis import Redis
except Exception:
    Redis = None  # type: ignore

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

def _get_redis() -> Optional["Redis"]:
    if Redis is None:
        return None
    try:
        return Redis.from_url(REDIS_URL)
    except Exception:
        return None

def mono(text: str) -> str:
    """Formatea el texto para mostrarlo en fuente monoespaciada en el PDF."""

# Importar el agente (preferir ruta absoluta del paquete backend)
try:
    from backend.agent.graph import app as agent_app
except Exception:
    try:
        from backend.agent.graph import workflow
        agent_app = workflow.compile()
    except Exception:
        # Fallback para entornos donde `backend` no está como paquete
        from agent.graph import workflow  # type: ignore
        agent_app = workflow.compile()  # type: ignore

# Asegurar que el directorio outputs exista
os.makedirs("outputs", exist_ok=True)

# Crear la aplicación FastAPI
api = FastAPI(title="Magazine Generator API", version="1.0.0")

# Configuración de CORS
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos desde el directorio outputs
api.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")
api.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
# Servir recursos utilizados por frontend/PDF
api.mount("/img", StaticFiles(directory="img"), name="img")
api.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Routers
api.include_router(auth_router)

@api.on_event("startup")
def _startup_create_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"DB init error: {e}")

@api.get("/viewer")
async def viewer_page():
    """Sirve el visor de PDF tipo flipbook básico (frontend/viewer.html)."""
    front_view = os.path.join("frontend", "viewer.html")
    if not os.path.exists(front_view):
        raise HTTPException(status_code=404, detail="viewer.html no encontrado")
    return FileResponse(front_view)
class GenerateRequest(BaseModel):
    tema: Optional[str] = None

# ===================== User endpoints (auth required) =====================

class SavedCreate(BaseModel):
    item_ref: str
    metadata: Optional[Dict[str, Any]] = None


@api.get("/magazines")
async def list_my_magazines(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(models.Magazine).filter(models.Magazine.user_id == current_user.id).order_by(models.Magazine.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "filename": r.filename,
            "title": r.title,
            "size_bytes": r.size_bytes,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "url": f"/outputs/{r.filename}" if r.filename else None,
        }
        for r in rows
    ]


@api.get("/saved")
async def list_my_saved(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(models.SavedItem).filter(models.SavedItem.user_id == current_user.id).order_by(models.SavedItem.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "item_ref": r.item_ref,
            "metadata": r.metadata,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


@api.post("/saved", status_code=201)
async def create_saved(payload: SavedCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not (payload.item_ref or "").strip():
        raise HTTPException(status_code=400, detail="item_ref requerido")
    row = models.SavedItem(user_id=current_user.id, item_ref=payload.item_ref.strip(), metadata=payload.metadata or None)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id}


@api.delete("/saved/{saved_id}", status_code=204)
async def delete_saved(saved_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(models.SavedItem).filter(models.SavedItem.id == saved_id, models.SavedItem.user_id == current_user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(row)
    db.commit()
    return


@api.get("/history")
async def user_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Devuelve historial del usuario autenticado.
    Combina:
    - Magazines generados (DB) como 'completed'.
    - Tareas activas (Redis) como 'process'.
    """
    items: list[dict] = []
    # 1) Magazines (completados)
    try:
        rows = (
            db.query(models.Magazine)
            .filter(models.Magazine.user_id == current_user.id)
            .order_by(models.Magazine.created_at.desc())
            .limit(20)
            .all()
        )
        for r in rows:
            meta_url = None
            try:
                if r.filename and r.filename.lower().endswith('.pdf'):
                    sidecar = r.filename[:-4] + 'json'
                    if os.path.exists(os.path.join('outputs', sidecar)):
                        meta_url = f"/outputs/{sidecar}"
            except Exception:
                meta_url = None
            items.append({
                "id": r.id,
                "name": r.title or r.filename or f"Magazine #{r.id}",
                "date": r.created_at.isoformat() if r.created_at else None,
                "status": "completed",
                "url": f"/outputs/{r.filename}" if r.filename else None,
                "meta_url": meta_url,
                "kind": "magazine",
            })
    except Exception:
        pass

    # 2) Flujos persistidos en DB (incluye completed/error/queued/running)
    try:
        flows = (
            db.query(models.Flow)
            .filter(models.Flow.user_id == current_user.id)
            .order_by(models.Flow.updated_at.desc())
            .limit(30)
            .all()
        )
        name_map = {
            "magazine": "Generación de Magazine",
            "requisitos": "Extracción de Requisitos",
            "fuentes": "Descubrimiento de Fuentes",
        }
        for f in flows:
            meta = f.meta or {}
            items.insert(0, {
                "id": f.task_id or f.id,
                "name": f.name or name_map.get((f.type or '').lower(), (f.type or 'flujo').title()),
                "date": (f.updated_at or f.created_at).isoformat() if (f.updated_at or f.created_at) else None,
                "status": (f.status or 'queued').lower(),
                "kind": "flow",
                "url": meta.get("result_url"),
            })
    except Exception:
        pass

    # 3) Tareas activas (Redis) - efímeras, complementan a DB
    r = _get_redis()
    if r:
        try:
            ids = [tid.decode() if isinstance(tid, bytes) else tid for tid in r.smembers("active_tasks")]
            for tid in ids:
                h = r.hgetall(_task_key(tid))
                if not h:
                    continue
                kv = {}
                for k, v in h.items():
                    key = k.decode() if isinstance(k, bytes) else k
                    val = v.decode() if isinstance(v, bytes) else v
                    kv[key] = val
                try:
                    uid = int(kv.get("user_id") or 0)
                except Exception:
                    uid = 0
                if uid != current_user.id:
                    continue
                st = (kv.get("status") or "").lower()
                flow_type = (kv.get("type") or "flujo").lower()
                name_map = {
                    "magazine": "Generación de Magazine",
                    "requisitos": "Extracción de Requisitos",
                    "fuentes": "Descubrimiento de Fuentes",
                }
                items.insert(0, {
                    "id": tid,
                    "name": name_map.get(flow_type, flow_type.title()),
                    "date": kv.get("created"),
                    "status": "process" if st in ("queued", "running") else st or "process",
                })
        except Exception:
            pass
    return {"items": items[:30]}


# ===== Flows: endpoints para sincronizar estado y consultar historial propio =====
try:
    from pydantic import BaseModel
except Exception:  # pydantic ya debería estar instalado
    BaseModel = object  # fallback mínimo


class FlowStatusUpdate(BaseModel):
    status: str
    name: str | None = None
    meta: dict | None = None


@api.post("/flows/{task_id}/status")
def update_flow_status(
    task_id: str,
    body: FlowStatusUpdate,
    x_worker_token: str | None = Header(default=None, alias="X-Worker-Token"),
    db: Session = Depends(get_db),
):
    """Actualiza el estado de un Flow por task_id (solo Worker).
    Requiere header X-Worker-Token que coincida con WORKER_TOKEN.
    """
    worker_token = os.getenv("WORKER_TOKEN")
    if not (worker_token and x_worker_token and x_worker_token == worker_token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    flow = db.query(models.Flow).filter(models.Flow.task_id == task_id).first()
    if not flow:
        raise HTTPException(status_code=404, detail="Flow no encontrado")

    s = (body.status or "").lower().strip()
    if s:
        flow.status = s
    if body.name:
        flow.name = body.name
    if body.meta is not None:
        flow.meta = body.meta

    now = datetime.utcnow()
    flow.updated_at = now
    if flow.status in ("completed", "error"):
        flow.finished_at = now

    db.commit()
    return {"ok": True, "id": flow.id, "task_id": flow.task_id, "status": flow.status}


@api.get("/flows/history")
def flows_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Historial de flujos persistidos para el usuario actual (solo DB)."""
    flows = (
        db.query(models.Flow)
        .filter(models.Flow.user_id == current_user.id)
        .order_by(models.Flow.updated_at.desc())
        .limit(100)
        .all()
    )
    data = []
    for f in flows:
        data.append({
            "id": f.id,
            "task_id": f.task_id,
            "type": f.type,
            "name": f.name,
            "status": f.status,
            "created_at": f.created_at.isoformat() if f.created_at else None,
            "updated_at": f.updated_at.isoformat() if f.updated_at else None,
            "finished_at": f.finished_at.isoformat() if f.finished_at else None,
            "meta": f.meta or {},
        })
    return {"items": data}

# Email settings file
EMAIL_SETTINGS_FILE = os.path.join("outputs", "email_settings.json")

@api.get("/", include_in_schema=False)
async def root():
    # Redirige al usuario a la ruta estática donde vive la landing
    return RedirectResponse(url="/frontend/landing.html")

# ===================== Background Tasks API (V2 Loader) =====================

class TaskCreate(BaseModel):
    type: str
    payload: Optional[Dict[str, Any]] = None

def _task_key(task_id: str) -> str:
    return f"task:{task_id}"

def _flow_lock_key(flow_type: str) -> str:
    return f"flow_lock:{flow_type}"

def _acquire_flow_lock(r: "Redis", flow_type: str, ttl: int = 60 * 60) -> bool:
    try:
        return bool(r.set(_flow_lock_key(flow_type), "1", nx=True, ex=ttl))
    except Exception:
        return True  # be permissive if no redis

def _release_flow_lock(r: Optional["Redis"], flow_type: str):
    if not r:
        return
    try:
        r.delete(_flow_lock_key(flow_type))
    except Exception:
        pass

@api.get("/tasks")
async def list_active_tasks(status: Optional[str] = None):
    """Listar tareas activas para rehidratación de UI. Solo 'active' soportado por ahora."""
    if status and status != "active":
        return {"tasks": []}
    r = _get_redis()
    if not r:
        return {"tasks": []}
    try:
        ids = [tid.decode() if isinstance(tid, bytes) else tid for tid in r.smembers("active_tasks")]
        tasks = []
        for tid in ids:
            h = r.hgetall(_task_key(tid))
            if not h:
                continue
            obj: Dict[str, Any] = {}
            for k, v in h.items():
                key = k.decode() if isinstance(k, bytes) else k
                val = v.decode() if isinstance(v, bytes) else v
                # try to parse json
                try:
                    obj[key] = json.loads(val)
                except Exception:
                    obj[key] = val
            tasks.append(obj)
        return {"tasks": tasks}
    except Exception:
        return {"tasks": []}

@api.get("/tasks/id/{task_id}")
async def get_task(task_id: str):
    r = _get_redis()
    if not r:
        raise HTTPException(status_code=404, detail="Task no encontrada")
    h = r.hgetall(_task_key(task_id))
    if not h:
        raise HTTPException(status_code=404, detail="Task no encontrada")
    obj: Dict[str, Any] = {}
    for k, v in h.items():
        key = k.decode() if isinstance(k, bytes) else k
        val = v.decode() if isinstance(v, bytes) else v
        try:
            obj[key] = json.loads(val)
        except Exception:
            obj[key] = val
    return obj

def _resolve_task_name(flow_type: str) -> str:
    if flow_type == "magazine":
        return "tasks.run_magazine"
    elif flow_type == "requisitos":
        return "tasks.run_requisitos"
    elif flow_type == "fuentes":
        return "tasks.run_fuentes"
    else:
        raise HTTPException(status_code=400, detail="type inválido")

@api.post("/tasks", status_code=201)
async def create_task(body: TaskCreate, current_user: models.User = Depends(get_current_user)):
    flow_type = (body.type or "").strip().lower()
    if flow_type not in ("magazine", "requisitos", "fuentes"):
        raise HTTPException(status_code=400, detail="type debe ser magazine|requisitos|fuentes")

    r = _get_redis()
    if r:
        # lock por usuario+tipo para evitar duplicados por usuario
        user_lock_type = f"{flow_type}:{current_user.id}"
        if not _acquire_flow_lock(r, user_lock_type):
            # Verificar si el lock está huérfano (sin tareas activas de ese tipo PARA ESTE USUARIO)
            try:
                ids = [tid.decode() if isinstance(tid, bytes) else tid for tid in r.smembers("active_tasks")]
                has_same_type_active = False
                for tid in ids:
                    h = r.hgetall(_task_key(tid))
                    if not h:
                        continue
                    kv = { (k.decode() if isinstance(k, bytes) else k): (v.decode() if isinstance(v, bytes) else v) for k, v in h.items() }
                    t = (kv.get("type") or "").lower()
                    st = (kv.get("status") or "").lower()
                    try:
                        uid = int(kv.get("user_id") or 0)
                    except Exception:
                        uid = 0
                    if uid == current_user.id and t == flow_type and st in ("queued", "running"):
                        has_same_type_active = True
                        break
                if not has_same_type_active:
                    # Lock obsoleto: liberarlo y continuar
                    _release_flow_lock(r, user_lock_type)
                    if not _acquire_flow_lock(r, user_lock_type):
                        raise HTTPException(status_code=409, detail=f"flow '{flow_type}' already running or queued")
                else:
                    raise HTTPException(status_code=409, detail=f"flow '{flow_type}' already running or queued")
            except HTTPException:
                raise
            except Exception:
                # Si hay error comprobando, mantener la semántica de 409
                raise HTTPException(status_code=409, detail=f"flow '{flow_type}' already running or queued")

    # ejecutar con Celery (secuencial: configurar worker concurrency=1)
    task_name = _resolve_task_name(flow_type)
    async def _apply_async():
        try:
            # Celery returns AsyncResult
            payload = body.payload or {}
            payload["user_id"] = current_user.id
            payload["user_email"] = current_user.email
            res = celery_app.send_task(task_name, kwargs={"payload": payload}, queue="flows")
            task_id = res.id
            # Pre-registrar en Redis
            if r:
                r.hset(_task_key(task_id), mapping={
                    "id": task_id,
                    "type": flow_type,
                    "status": "queued",
                    "created": datetime.utcnow().isoformat(),
                    "user_id": current_user.id,
                })
                r.sadd("active_tasks", task_id)
            return task_id
        except Exception as e:
            # liberar lock si falló el encolado
            _release_flow_lock(r, f"{flow_type}:{current_user.id}")
            raise HTTPException(status_code=500, detail=f"No se pudo encolar la tarea: {e}")

    task_id = await _apply_async()
    # Persistir Flow en DB
    try:
        nm = _resolve_task_name(flow_type)
        name_map = {
            "magazine": "Generación de Magazine",
            "requisitos": "Extracción de Requisitos",
            "fuentes": "Descubrimiento de Fuentes",
        }
        flow = models.Flow(
            user_id=current_user.id,
            task_id=task_id,
            type=flow_type,
            name=name_map.get(flow_type, flow_type.title()),
            status="queued",
            meta=body.payload or {},
        )
        with next(get_db()) as _db:
            _db.add(flow)
            _db.commit()
    except Exception as e:
        print(f"No se pudo persistir Flow: {e}")
    return {"id": task_id, "status": "queued"}


@api.get("/tasks/stream")
async def tasks_stream():
    """SSE global reenviando eventos de Redis pub/sub 'tasks_events'.
    Incluye keepalive periódico para proxies HTTP/2 (Codespaces).
    """
    r = _get_redis()
    if not r:
        # fallback simple: stream keepalive sin eventos
        async def _noop_gen():
            while True:
                yield "event: keepalive\n" + "data: {}\n\n"
                await asyncio.sleep(15)
        return StreamingResponse(_noop_gen(), media_type="text/event-stream")

    pubsub = r.pubsub()
    pubsub.subscribe("tasks_events")

    async def event_generator():
        try:
            # Send a hello event
            yield "event: hello\n" + "data: {}\n\n"
            last_ping = time.time()
            while True:
                msg = pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if msg and msg.get("type") == "message":
                    data = msg.get("data")
                    if isinstance(data, (bytes, bytearray)):
                        data = data.decode()
                    try:
                        js = json.loads(data)
                        ev_type = js.get("type") or "message"
                        yield f"event: {ev_type}\n" + f"data: {json.dumps(js)}\n\n"
                    except Exception:
                        yield "data: {}\n\n"
                # keepalive ping every 10s
                now = time.time()
                if now - last_ping >= 10:
                    last_ping = now
                    yield ": keepalive\n\n"
                await asyncio.sleep(0.1)
        finally:
            try:
                pubsub.close()
            except Exception:
                pass

    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        # Codespaces proxies sometimes buffer without this
        "X-Accel-Buffering": "no",
    }
    return StreamingResponse(event_generator(), media_type="text/event-stream", headers=headers)

@api.post("/generate")
async def generate_magazine(req: GenerateRequest | None = None):
    """
    Endpoint para generar un magazine basado en un tema.
    """

    print(f"🔑 Clave de Gemini cargada: {os.getenv('GEMINI_API_KEY') is not None}")

    try:
        default_topic = os.getenv(
            "DEFAULT_TOPIC",
            "convocatorias de financiación nacionales e internacionales y eventos en ciencia, tecnología e inteligencia artificial para startups"
        )
        tema = (req.tema if req and req.tema else default_topic)
        print(f"📥 Generando magazine para tema: {tema}")

        inputs = {"tema": tema}

        # Ejecutar el agente
        result = {}
        for output in agent_app.stream(inputs):
            for key, value in output.items():
                if key in ['contenido_curado', 'pdf_path']:
                    result[key] = value
        
        # Obtener la ruta del PDF generado
        pdf_path = result.get("pdf_path")

        # URL del PDF generado (si existe)
        pdf_url = None
        if pdf_path:
            safe_path = pdf_path.replace('\\', '/')
            pdf_url = f"/{safe_path}"

        # Contenido curado para frontend (si disponible)
        contenido_curado = result.get("contenido_curado", [])
        # No forzar error si falta el PDF: devolvemos 200 con lo que haya
        # Intentar asociar IDs guardados por URL
        try:
            saved_items = _load_json_list(os.path.join("outputs", "convocatorias.json"))
            by_url = {}
            for it in saved_items:
                u = str(it.get("url") or it.get("source") or "").strip()
                if u:
                    by_url[u] = it
            for it in contenido_curado:
                u = str(it.get("url_original") or "").strip()
                if u and u in by_url:
                    it["id"] = by_url[u].get("id")
        except Exception:
            pass

        return {
            "status": "success",
            "message": "Magazine generado exitosamente",
            "pdf_url": pdf_url,
            "contenido_curado": contenido_curado,
        }
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al generar el magazine: {str(e)}")

# ===================== Requirements Extraction =====================
try:
    # Reusar el LLM configurado en el agente
    from agent.nodes import llm as agent_llm
except Exception:
    agent_llm = None

# Utilidades de búsqueda web para fuentes
try:
    from backend.agent.tools import search_all as web_search_all  # type: ignore
except Exception:
    try:
        from agent.tools import search_all as web_search_all  # type: ignore
    except Exception:
        web_search_all = None

@api.get("/requirements/{item_id}")
async def get_requirements(item_id: int):
    """Extrae requisitos para una convocatoria/evento por su ID.
    - Busca el item en outputs/convocatorias.json
    - Descarga la página original (y posibles PDFs enlazados)
    - Invoca LLM para devolver una lista concisa de requisitos
    """
    items = _load_json_list(os.path.join("outputs", "convocatorias.json"))
    item = next((it for it in items if int(it.get("id", -1)) == int(item_id)), None)
    if not item:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")

    url = item.get("url") or item.get("source")
    if not url:
        return {"id": item_id, "requirements": ["No especificado"], "sources": []}

    # Descargar contenido de la página
    try:
        resp = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html.parser')
        text = soup.get_text(" ", strip=True)
        # Buscar enlaces a PDFs
        pdf_links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.lower().endswith('.pdf'):
                if href.startswith('http'):
                    pdf_links.append(href)
                else:
                    try:
                        from urllib.parse import urljoin
                        pdf_links.append(urljoin(url, href))
                    except Exception:
                        pass
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"No se pudo acceder a la URL: {e}")

    # Construir prompt para LLM
    prompt = f"""
    Eres un asistente experto en convocatorias. A partir del texto de la página y, si aplica, documentos vinculados, devuelve SOLO un JSON con este formato:
    {{"requirements": ["req1", "req2", "req3", ...]}}

    Reglas:
    - Extrae requisitos concretos y accionables (documentos, criterios, elegibilidad, fechas clave).
    - Mantenlos concisos (10-18 palabras máximo por requisito), en español neutro.
    - Si no se encuentran, devuelve {{"requirements": ["No especificado"]}}.

    Título: {item.get('title')}
    Tipo: {item.get('type')}
    Enlace: {url}
    Texto:
    {text[:8000]}
    """

    # Llamada a LLM y parseo robusto de JSON
    requirements: List[str] = []
    if agent_llm is None:
        requirements = ["No especificado"]
    else:
        try:
            raw = agent_llm.invoke(prompt).content
            import re as _re, json as _json
            m = _re.search(r"\{.*\}", raw, _re.DOTALL)
            js = _json.loads(m.group(0) if m else raw)
            reqs = js.get("requirements")
            if isinstance(reqs, list) and reqs:
                # Normalizar: quitar líneas vacías y recortar
                requirements = [str(r).strip() for r in reqs if str(r).strip()]
        except Exception:
            requirements = ["No especificado"]

    # Persistir en outputs/convocatorias.json
    try:
        json_path = os.path.join("outputs", "convocatorias.json")
        items_all = _load_json_list(json_path)
        changed = False
        for it in items_all:
            if int(it.get("id", -1)) == int(item_id):
                it["requisitos"] = requirements or ["No especificado"]
                changed = True
                break
        if changed:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(items_all, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # No interrumpir la respuesta si falla la persistencia
        print(f"No se pudo persistir requisitos: {e}")

    return {
        "id": item_id,
        "requirements": requirements or ["No especificado"],
        "sources": [url] + pdf_links[:5],
        "saved": True
    }

# ===================== Sources Search (Fuentes de Investigación) =====================

class SourcesSearchRequest(BaseModel):
    query: str

@api.post("/sources/search")
async def search_sources(payload: SourcesSearchRequest):
    """Busca posibles fuentes en la web y marca si ya existen en outputs/sources.json.
    Devuelve una lista de objetos {title, url, exists, id?}.
    """
    q = (payload.query or '').strip()
    if not q:
        return {"results": []}

    # Cargar fuentes existentes
    sources_path = os.path.join("outputs", "sources.json")
    existing = _load_json_list(sources_path)

    def _norm(u: str) -> str:
        try:
            p = urlparse(u)
            host = (p.netloc or '').lower().lstrip('www.')
            path = (p.path or '').rstrip('/')
            return f"{host}{path}"
        except Exception:
            return (u or '').lower().strip()

    existing_map = {}
    for s in existing:
        key = _norm(s.get('url', ''))
        if key:
            existing_map[key] = s

    results = []
    if web_search_all is None:
        hits = []
    else:
        # Limitar resultados para UI
        try:
            hits = web_search_all(q, tavily_max=3, brave_max=1) or []
        except Exception:
            hits = []

    for h in hits:
        url = h.get('url') or ''
        title = h.get('title') or url
        key = _norm(url)
        matched = existing_map.get(key)
        results.append({
            "title": title,
            "url": url,
            "exists": matched is not None,
            "id": matched.get('id') if matched else None
        })

    # Ordenar: nuevas (exists=false) primero
    results.sort(key=lambda x: (x.get('exists', False), (x.get('title') or '').lower()))
    return {"results": results}

class SourcesAISearchRequest(BaseModel):
    tema: Optional[str] = None

@api.post("/sources/ai_search")
async def ai_search_sources(payload: SourcesAISearchRequest | None = None):
    """Flujo con LLM: genera consultas y descubre fuentes (nombre y URL).
    Respuesta: { results: [ { title, url, exists, id? } ] }
    """
    # Temas fijos solicitados
    fixed_topics = [
        "inteligencia artificial",
        "ciencia",
        "tecnología",
        "naval",
    ]

    # 1) Generar consultas
    consultas: List[str] = []
    if agent_llm is not None:
        try:
            prompt = f"""
            Eres un experto en OSINT. Devuelve SOLAMENTE 8 consultas de búsqueda (una por línea) para encontrar portales oficiales y bases de datos de convocatorias y eventos relevantes.
            Debes cubrir específicamente estos temas: {', '.join(fixed_topics)}.
            Enfócate en sitios gubernamentales, multilaterales, universidades y grandes organizaciones. Incluye variantes en español e inglés.
            No enumeres ni agregues comentarios, solo una consulta por línea.
            Ejemplos de términos: portal convocatorias, funding opportunities, grants database, procurement, calls for proposals.
            """
            raw = agent_llm.invoke(prompt).content.strip()
            consultas = [c.strip() for c in raw.splitlines() if c.strip()][:8]
        except Exception:
            consultas = []
    if not consultas:
        consultas = [
            "portal convocatorias inteligencia artificial site:.gov OR site:.edu",
            "funding opportunities artificial intelligence grants database",
            "convocatorias ciencia universidad portal investigación",
            "science research funding opportunities site:.gov",
            "portal convocatorias tecnología ministerio site:.gov",
            "technology grants database international organizations",
            "convocatorias naval defensa site:.gov",
            "naval research funding calls for proposals",
        ]

    # 2) Buscar con web_search_all
    hits: List[Dict[str, Any]] = []
    if web_search_all is not None:
        for q in consultas:
            try:
                hits.extend(web_search_all(q, tavily_max=2, brave_max=1) or [])
            except Exception:
                pass

    # 3) Dedupe por URL normalizada
    def _norm(u: str) -> str:
        try:
            p = urlparse(u)
            host = (p.netloc or '').lower().lstrip('www.')
            path = (p.path or '').rstrip('/')
            return f"{host}{path}"
        except Exception:
            return (u or '').lower().strip()

    seen = set()
    unique = []
    for h in hits:
        url = h.get('url') or ''
        if not url:
            continue
        key = _norm(url)
        if key in seen:
            continue
        seen.add(key)
        title = h.get('title') or url
        unique.append({"title": title, "url": url})

    # 4) Marcar existentes
    existing = _load_json_list(os.path.join("outputs", "sources.json"))
    existing_map = {}
    for s in existing:
        k = _norm(s.get('url', ''))
        if k:
            existing_map[k] = s

    results = []
    for it in unique:
        url = it.get('url') or ''
        k = _norm(url)
        matched = existing_map.get(k)
        results.append({
            "title": it.get('title') or url,
            "url": url,
            "exists": matched is not None,
            "id": matched.get('id') if matched else None
        })

    # 5) Ordenar nuevas primero
    results.sort(key=lambda x: (x.get('exists', False), (x.get('title') or '').lower()))
    return {"results": results, "queries": consultas}

# ===================== Helpers & New Endpoints =====================

def _ensure_outputs():
    os.makedirs("outputs", exist_ok=True)

def _load_json_list(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _save_json_list(path: str, data: list):
    _ensure_outputs()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _load_json_dict(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_json_dict(path: str, data: dict):
    _ensure_outputs()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class IdsRequest(BaseModel):
    ids: List[int]
    title: Optional[str] = None


class PDF(FPDF):
    # --- PALETA DE COLORES Y FUENTES DEL DISEÑO ---
    COLOR_HEADER = (0, 68, 136)
    COLOR_TITLE = (26, 32, 44)
    COLOR_SECTION_TITLE = (112, 128, 150)
    COLOR_BODY_TEXT = (74, 85, 104)
    COLOR_BACKGROUND_GREY = (247, 250, 252)
    FONT_SERIF = 'RobotoSlab'
    FONT_SANS = 'Roboto'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = os.path.join(script_dir, '..', 'img')
        
        self._load_fonts(script_dir)
        
    def _load_fonts(self, base_path):
        """Carga las fuentes personalizadas para el diseño."""
        try:
            self.add_font(self.FONT_SANS, '', os.path.join(base_path, 'Roboto-Regular.ttf'), uni=True)
            self.add_font(self.FONT_SANS, 'B', os.path.join(base_path, 'Roboto-Bold.ttf'), uni=True)
            self.add_font(self.FONT_SERIF, 'B', os.path.join(base_path, 'RobotoSlab-Bold.ttf'), uni=True)
        except Exception as e:
            raise RuntimeError(f"Error cargando fuentes. Detalle: {e}")

    def footer(self):
        pass
    
    def draw_section(self, icon_name, title, text, width):
        """Dibuja una sección con un icono de imagen, título y texto."""
        icon_path = os.path.join(self.img_dir, icon_name)
        y_start = self.get_y()
        x_start = self.get_x()

        if os.path.exists(icon_path):
            self.image(icon_path, x=x_start, y=y_start, w=10)

        self.set_xy(x_start + 15, y_start)
        self.set_font(self.FONT_SANS, 'B', 9)
        self.set_text_color(*self.COLOR_SECTION_TITLE)
        self.cell(width - 15, 10, title.upper())
        self.ln(15)

        self.set_x(x_start)
        self.set_font(self.FONT_SANS, '', 11)
        self.set_text_color(*self.COLOR_BODY_TEXT)
        if isinstance(text, list):
            text = '\n• ' + '\n• '.join(filter(None, text))
        self.multi_cell(width, 16, str(text))
        self.ln(10)

    def draw_call_card(self, item: dict):
        self.add_page()
        
        # --- 1. CABECERA (CON LÓGICA DINÁMICA) ---
        # Mapeo para traducir el 'type' del JSON a un texto legible
        type_mapping = {
            'convocatoria_nacional': 'Convocatorias Nacionales',
            'convocatoria_internacional': 'Convocatorias Internacionales',
            'evento': 'Eventos'
        }
        # Obtener el tipo del JSON, con un valor por defecto seguro
        item_type = item.get("type", "convocatoria_nacional").lower()
        # Buscar el texto correspondiente. Si no lo encuentra, usa 'Convocatorias' como fallback.
        header_text = type_mapping.get(item_type, 'Convocatorias')

        self.set_fill_color(*self.COLOR_HEADER)
        self.set_text_color(255, 255, 255)
        self.set_font(self.FONT_SANS, '', 18)
        # Usar la variable header_text en lugar del texto fijo
        self.cell(0, 30, f"   {header_text}", fill=True, align='L', new_x='LMARGIN', new_y='NEXT')
        
        icon_grid_path = os.path.join(self.img_dir, 'logo-cotecmar.png')
        if os.path.exists(icon_grid_path):
            self.image(icon_grid_path, x=self.w - self.r_margin - 66, y=self.t_margin - 34, w=84)

        self.ln(25)

        # --- 2. TÍTULO PRINCIPAL ---
        self.set_font(self.FONT_SERIF, 'B', 24)
        self.set_text_color(*self.COLOR_TITLE)
        self.multi_cell(0, 30, item.get("title", "Sin Título"))
        self.ln(25)

        # --- Definición de la geometría de las columnas ---
        y_columns_start = self.get_y()
        col_width = (self.w - self.l_margin - self.r_margin - 30) / 2
        gutter = 30
        x_col_left = self.l_margin
        x_col_right = self.l_margin + col_width + gutter

        # --- Columna Izquierda ---
        self.set_y(y_columns_start)
        self.set_x(x_col_left)
        kw_list = [kw for kw in item.get("keywords", []) if isinstance(kw, str) and "convocatoria" not in kw.lower()]
        dirigido_a = ", ".join(kw_list) or "No especificado"
        self.draw_section('icon_person.png', "DIRIGIDO A", dirigido_a, col_width)

        self.set_x(x_col_left)
        self.draw_section('icon_target.png', "OBJETIVO", item.get("description", "No especificado"), col_width)

        self.set_x(x_col_left)
        monto = item.get("monto", "No especificado")
        tipo_fin = item.get("type_financy", "No especificado")
        fin_txt = f"Monto: {monto}\nTipo: {tipo_fin}"
        self.draw_section('icon_money.png', "FINANCIAMIENTO", fin_txt, col_width)

        self.set_x(x_col_left)
        kws = item.get("keywords", [])
        kws_print = [kw for kw in kws if isinstance(kw, str)]
        self.draw_section('icon_tag.png', "KEYWORDS", ', '.join(kws_print) if kws_print else 'No especificado', col_width)
        y_left_end = self.get_y()

        # --- Columna Derecha ---
        self.set_y(y_columns_start)
        self.set_x(x_col_right)
        fecha_inicio = item.get("fecha_inicio") or item.get("inicio") or "No especificado"
        fecha_cierre = item.get("fecha_cierre") or item.get("deadline") or "No especificado"
        fechas_txt = f"Inicio: {fecha_inicio}\nCierre: {fecha_cierre}"
        self.draw_section('icon_clock.png', "FECHAS IMPORTANTES", fechas_txt, col_width)

        self.set_x(x_col_right)
        enlace = item.get("url") or item.get("source") or "No especificado"
        self.draw_section('icon_info.png', "MÁS INFORMACIÓN", enlace, col_width)

        self.set_x(x_col_right)
        self.draw_section('icon_check.png', "BENEFICIOS", item.get("beneficios", "No especificados"), col_width)

        # Colocar el cursor al final del bloque más bajo
        self.set_y(max(y_left_end, self.get_y()))

@api.post("/generate_pdf_from_ids")
async def generate_pdf_from_ids(
    payload: IdsRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Genera un PDF a partir de IDs guardados en outputs/convocatorias.json.
    """
    try:
        # Construir la ruta al archivo convocatorias.json
        convocatorias_path = os.path.join("outputs", "convocatorias.json")
        print(f"Buscando archivo en: {os.path.abspath(convocatorias_path)}")
        
        # Verificar si el archivo existe
        if not os.path.exists(convocatorias_path):
            error_msg = f"No se encontró el archivo: {convocatorias_path}"
            print(error_msg)
            raise HTTPException(status_code=404, detail=error_msg)
            
        # Cargar los datos
        items = _load_json_list(convocatorias_path)
        print(f"Se cargaron {len(items)} convocatorias")
        
        # Verificar que se cargaron datos
        if not items:
            error_msg = "El archivo de convocatorias está vacío"
            print(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
            
        # Buscar las convocatorias solicitadas
        selected = [it for it in items if it.get("id") in payload.ids]
        
        if not selected:
            # Mostrar más detalles del error para diagnóstico
            error_msg = f"No se encontraron convocatorias para los IDs enviados. IDs solicitados: {payload.ids}, IDs disponibles: {[it.get('id') for it in items]}"
            print(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)

        # Nombre solicitado: magazine_YYYY-MM-DD_HH-mm.pdf
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        pdf_name = f"magazine_{ts}.pdf"
        pdf_path = os.path.join("outputs", pdf_name)

        pdf = PDF(orientation='P', unit='pt', format='A4')
        pdf.set_auto_page_break(auto=True, margin=40)
        pdf.set_margins(left=40, top=40, right=40)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(script_dir, '..', 'assets')
        inicio_cover = os.path.join(assets_dir, 'inicio.png')
        nacionales_cover = os.path.join(assets_dir, 'nacionales.png')
        internacionales_cover = os.path.join(assets_dir, 'internacionales.png')
        eventos_cover = os.path.join(assets_dir, 'eventos.png')
        cierre_cover = os.path.join(assets_dir, 'cierre.png')

        def add_fullpage_image(image_path: str):
            if os.path.exists(image_path):
                from PIL import Image as PILImage
                pdf.add_page()
                try:
                    with PILImage.open(image_path) as im:
                        iw, ih = im.size
                except Exception:
                    iw, ih = (1000, 1414)
                pw, ph = float(pdf.w), float(pdf.h)
                scale = min(pw / iw, ph / ih)
                w = iw * scale
                h = ih * scale
                x = (pw - w) / 2.0
                y = (ph - h) / 2.0
                pdf.image(image_path, x=x, y=y, w=w, h=h)

        add_fullpage_image(inicio_cover)

        nacionales = [it for it in selected if str(it.get('type', 'convocatoria_nacional')).lower() == 'convocatoria_nacional']
        internacionales = [it for it in selected if str(it.get('type', '')).lower() == 'convocatoria_internacional']
        eventos = [it for it in selected if 'evento' in str(it.get('type', '')).lower()]

        if nacionales:
            add_fullpage_image(nacionales_cover)
            for it in nacionales:
                pdf.draw_call_card(it)

        if internacionales:
            add_fullpage_image(internacionales_cover)
            for it in internacionales:
                pdf.draw_call_card(it)

        if eventos:
            add_fullpage_image(eventos_cover)
            for it in eventos:
                pdf.draw_call_card(it)

        add_fullpage_image(cierre_cover)

        pdf.output(pdf_path)
        print(f"PDF generado exitosamente en: {pdf_path}")
        # Persistir en DB para historial del usuario
        try:
            size_bytes = None
            try:
                size_bytes = os.path.getsize(pdf_path)
            except Exception:
                pass
            title = (payload.title or '').strip() or f"Magazine personalizado ({len(selected)} ítems)"
            row = models.Magazine(
                user_id=current_user.id,
                filename=pdf_name,
                title=title,
                size_bytes=size_bytes,
            )
            db.add(row)
            db.commit()
        except Exception as e:
            # No interrumpir la respuesta si la persistencia falla
            print(f"No se pudo guardar Magazine en DB: {e}")
        # Guardar sidecar JSON con metadatos (selected_ids, title, user_id, created_at)
        try:
            sidecar_name = pdf_name[:-4] + 'json' if pdf_name.lower().endswith('.pdf') else pdf_name + '.json'
            sidecar_path = os.path.join('outputs', sidecar_name)
            meta = {
                "selected_ids": [int(i) for i in (payload.ids or [])],
                "title": title,
                "user_id": current_user.id,
                "created_at": datetime.utcnow().isoformat(),
                "pdf": f"/outputs/{pdf_name}",
            }
            _save_json_dict(sidecar_path, meta)
        except Exception as e:
            print(f"No se pudo guardar sidecar JSON: {e}")
        # Asegurarse de que la URL sea accesible
        viewer_url = f"/viewer?file=/outputs/{pdf_name}"
        return {"status": "success", "pdf_url": f"/outputs/{pdf_name}", "viewer_url": viewer_url}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {e}")

# --------------------- Email settings ---------------------

class EmailSettings(BaseModel):
    # Backward- and forward-compatible fields
    sender_email: Optional[str] = None
    favorite_emails: Optional[List[str]] = None
    # Also accept alternative keys some frontends may send
    sender: Optional[str] = None
    favorites: Optional[List[str]] = None

@api.get("/email_settings")
async def get_email_settings():
    raw = _load_json_dict(EMAIL_SETTINGS_FILE)
    # Normalize keys
    sender_email = raw.get("sender_email") or raw.get("sender") or os.getenv("DEFAULT_SENDER_EMAIL", "harithodevoz@gmail.com")
    favs = raw.get("favorite_emails")
    if not isinstance(favs, list):
        favs = raw.get("favorites") if isinstance(raw.get("favorites"), list) else []
    # Return both keys for compatibility
    return {
        "sender_email": sender_email,
        "favorite_emails": favs,
        "sender": sender_email,
        "favorites": favs,
    }

@api.post("/email_settings")
async def save_email_settings(payload: EmailSettings):
    # Basic email validation
    def _is_email(x: str) -> bool:
        return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", x or ""))

    # Normalize incoming fields
    sender_val = payload.sender_email or payload.sender or os.getenv("DEFAULT_SENDER_EMAIL", "harithodevoz@gmail.com")
    if not _is_email(sender_val):
        sender_val = os.getenv("DEFAULT_SENDER_EMAIL", "harithodevoz@gmail.com")
    favs_in = payload.favorite_emails if isinstance(payload.favorite_emails, list) else payload.favorites
    favs: List[str] = [e for e in (favs_in or []) if _is_email(e)]

    data = {
        "sender_email": sender_val,
        "favorite_emails": favs,
        # Also store alternative keys for forward compatibility
        "sender": sender_val,
        "favorites": favs,
    }
    _save_json_dict(EMAIL_SETTINGS_FILE, data)
    return {"status": "ok"}

# --------------------- Send Email ---------------------

class SendEmailRequest(BaseModel):
    pdf_url: Optional[str] = None
    pdf_path: Optional[str] = None
    sender: str
    recipients: List[str]
    subject: Optional[str] = "Revista de Convocatorias COTECMAR"

def _resolve_pdf_path(pdf_url: str) -> str:
    """Given a URL like '/outputs/file.pdf' or absolute URL, return local filesystem path."""
    if not pdf_url:
        raise HTTPException(status_code=400, detail="pdf_url es requerido")
    parsed = urlparse(pdf_url)
    path = parsed.path if parsed.scheme else pdf_url
    # Normalize and map to local outputs folder
    if "/outputs/" in path:
        fname = path.split("/outputs/")[-1]
        local = os.path.join("outputs", os.path.basename(fname))
    else:
        # If a direct relative path already
        local = path.lstrip("/")
    if not os.path.exists(local):
        raise HTTPException(status_code=404, detail=f"PDF no encontrado en servidor: {local}")
    return local

def _send_smtp(sender: str, to_list: List[str], subject: str, body: str, attachments: List[str]):
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASS")
    use_tls = os.getenv("SMTP_TLS", "true").lower() in ("1", "true", "yes")
    demo_mode = os.getenv("DEMO_MODE", "false").lower() in ("1", "true", "yes")

    if demo_mode:
        # Simular envío guardando el .eml
        _ensure_outputs()
        out_dir = os.path.join("outputs", "sent_emails")
        os.makedirs(out_dir, exist_ok=True)
        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = ", ".join(to_list)
        msg["Subject"] = subject
        msg.set_content(body)
        for path in attachments:
            ctype, _ = mimetypes.guess_type(path)
            maintype, subtype = (ctype.split("/", 1) if ctype else ("application", "octet-stream"))
            with open(path, "rb") as f:
                msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(path))
        fname = os.path.join(out_dir, f"email_{int(time.time())}.eml")
        with open(fname, "wb") as f:
            f.write(bytes(msg))
        return

    if not host:
        raise HTTPException(status_code=500, detail="SMTP_HOST no configurado. Define variables SMTP_* o activa DEMO_MODE=true")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(to_list)
    msg["Subject"] = subject
    msg.set_content(body)

    for path in attachments:
        ctype, _ = mimetypes.guess_type(path)
        maintype, subtype = (ctype.split("/", 1) if ctype else ("application", "octet-stream"))
        with open(path, "rb") as f:
            msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(path))

    with smtplib.SMTP(host, port) as server:
        if use_tls:
            server.starttls()
        if user and password:
            server.login(user, password)
        server.send_message(msg)

@api.post("/send_email")
async def send_email(payload: SendEmailRequest):
    # Validate
    if not payload.recipients:
        raise HTTPException(status_code=400, detail="Debes especificar al menos un destinatario")
    email_re = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    if not email_re.match(payload.sender or ""):
        raise HTTPException(status_code=400, detail="Remitente inválido")
    bad = [r for r in payload.recipients if not email_re.match(r)]
    if bad:
        raise HTTPException(status_code=400, detail=f"Destinatarios inválidos: {', '.join(bad)}")

    # Resolve PDF path
    if payload.pdf_path:
        pdf_path = payload.pdf_path.lstrip("/")
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail=f"PDF no encontrado en servidor: {pdf_path}")
    else:
        pdf_path = _resolve_pdf_path(payload.pdf_url or "")

    # Compose and send
    try:
        _send_smtp(
            sender=payload.sender,
            to_list=payload.recipients,
            subject=payload.subject or "Revista de Convocatorias COTECMAR",
            body="Adjuntamos la revista de convocatorias generada.",
            attachments=[pdf_path],
        )
        return {"status": "sent"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando correo: {e}")

# --------------------- Upload PDF ---------------------

@api.post("/upload_pdf")
async def upload_pdf(pdf_file: UploadFile = File(...)):
    """Recibe un archivo PDF y lo guarda en outputs/uploads/ devolviendo su ruta relativa."""
    if not pdf_file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    upload_dir = os.path.join("outputs", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    safe_name = os.path.basename(pdf_file.filename)
    dest_path = os.path.join(upload_dir, safe_name)
    try:
        with open(dest_path, "wb") as out:
            shutil.copyfileobj(pdf_file.file, out)
    finally:
        try:
            pdf_file.file.close()
        except Exception:
            pass
    rel_path = dest_path.replace("\\", "/")
    return {"status": "success", "pdf_path": rel_path}


# --------------------- Sources CRUD ---------------------

SOURCES_FILE = os.path.join("outputs", "sources.json")

def _next_source_id(items: list) -> int:
    if not items:
        return 1
    try:
        return max(int(x.get("id", 0)) for x in items) + 1
    except Exception:
        return len(items) + 1

class SourceCreate(BaseModel):
    name: str
    type: Optional[str] = None
    url: str

class SourceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None
    hidden: Optional[bool] = None

@api.get("/sources")
async def get_sources() -> List[Dict[str, Any]]:
    return _load_json_list(SOURCES_FILE)

@api.post("/sources")
async def create_source(src: SourceCreate):
    items = _load_json_list(SOURCES_FILE)
    new_obj = {"id": _next_source_id(items), "name": src.name, "type": src.type or "", "url": src.url, "hidden": False}
    items.append(new_obj)
    _save_json_list(SOURCES_FILE, items)
    return new_obj

@api.put("/sources/{source_id}")
async def update_source(source_id: int = Path(...), patch: SourceUpdate = None):
    items = _load_json_list(SOURCES_FILE)
    for it in items:
        if int(it.get("id", -1)) == int(source_id):
            if patch.name is not None:
                it["name"] = patch.name
            if patch.type is not None:
                it["type"] = patch.type
            if patch.url is not None:
                it["url"] = patch.url
            if patch.hidden is not None:
                it["hidden"] = bool(patch.hidden)
            _save_json_list(SOURCES_FILE, items)
            return it
    raise HTTPException(status_code=404, detail="Source no encontrada")

@api.patch("/sources/{source_id}/toggle")
async def toggle_source(source_id: int = Path(...)):
    items = _load_json_list(SOURCES_FILE)
    for it in items:
        if int(it.get("id", -1)) == int(source_id):
            it["hidden"] = not bool(it.get("hidden", False))
            _save_json_list(SOURCES_FILE, items)
            return it
    raise HTTPException(status_code=404, detail="Source no encontrada")

@api.delete("/sources/{source_id}")
async def delete_source(source_id: int = Path(...)):
    items = _load_json_list(SOURCES_FILE)
    initial_len = len(items)
    items = [it for it in items if int(it.get("id", -1)) != int(source_id)]
    if len(items) == initial_len:
        raise HTTPException(status_code=404, detail="Source no encontrada")
    _save_json_list(SOURCES_FILE, items)
    return {"status": "success", "message": "Source eliminada"}

# ---- Run server if executed directly (after all routes are defined) ----
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)