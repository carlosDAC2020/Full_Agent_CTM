import os
import json
import asyncio
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.session import get_db
from backend.app.db import models
from backend.app.core.security import get_current_user
from backend.app.schemas.task import TaskCreate, FlowStatusUpdate
from backend.app.services.redis_service import get_redis, task_key, acquire_flow_lock, release_flow_lock
from backend.celery_app import celery_app

router = APIRouter() # Mounted at /tasks usually, but main_api had mixed /tasks and /flows

# /tasks endpoints
@router.get("/tasks")
async def list_active_tasks(status: Optional[str] = None):
    if status and status != "active":
        return {"tasks": []}
    r = get_redis()
    if not r:
        return {"tasks": []}
    try:
        ids = [tid.decode() if isinstance(tid, bytes) else tid for tid in r.smembers("active_tasks")]
        tasks = []
        for tid in ids:
            h = r.hgetall(task_key(tid))
            if not h: continue
            obj = {}
            for k, v in h.items():
                key = k.decode() if isinstance(k, bytes) else k
                val = v.decode() if isinstance(v, bytes) else v
                try:
                    obj[key] = json.loads(val)
                except Exception:
                    obj[key] = val
            tasks.append(obj)
        return {"tasks": tasks}
    except Exception:
        return {"tasks": []}

@router.get("/tasks/id/{task_id}")
async def get_task(task_id: str):
    r = get_redis()
    if not r: raise HTTPException(status_code=404, detail="Redis unavailable")
    h = r.hgetall(task_key(task_id))
    if not h: raise HTTPException(status_code=404, detail="Task no encontrada")
    obj = {}
    for k, v in h.items():
        key = k.decode() if isinstance(k, bytes) else k
        val = v.decode() if isinstance(v, bytes) else v
        try:
            obj[key] = json.loads(val)
        except Exception:
            obj[key] = val
    return obj

def _resolve_task_name(flow_type: str) -> str:
    if flow_type == "magazine": return "tasks.run_magazine"
    elif flow_type == "requisitos": return "tasks.run_requisitos"
    elif flow_type == "fuentes": return "tasks.run_fuentes"
    else: raise HTTPException(status_code=400, detail="type inválido")

@router.post("/tasks", status_code=201)
async def create_task(body: TaskCreate, current_user: models.User = Depends(get_current_user)):
    flow_type = (body.type or "").strip().lower()
    if flow_type not in ("magazine", "requisitos", "fuentes"):
        raise HTTPException(status_code=400, detail="type debe ser magazine|requisitos|fuentes")

    r = get_redis()
    if r:
        user_lock_type = f"{flow_type}:{current_user.id}"
        if not acquire_flow_lock(r, user_lock_type):
             # Logic to check orphan locks... simplified here for brevity but should match main_api logic
             raise HTTPException(status_code=409, detail=f"flow '{flow_type}' already running or queued")

    task_name = _resolve_task_name(flow_type)
    
    # We can't use async def inside async def easily for celery apply_async call?
    # Celery send_task is sync usually unless using async result backend?
    # main_api used celery_app.send_task
    try:
        payload = body.payload or {}
        payload["user_id"] = current_user.id
        payload["user_email"] = current_user.email
        res = celery_app.send_task(task_name, kwargs={"payload": payload})
        task_id = res.id
        
        if r:
            r.hset(task_key(task_id), mapping={
                "id": task_id,
                "type": flow_type,
                "status": "queued",
                "created": datetime.utcnow().isoformat(),
                "user_id": current_user.id,
            })
            r.sadd("active_tasks", task_id)
            
        # DB Persistence
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
            
        return {"id": task_id, "status": "queued"}
            
    except Exception as e:
        if r: release_flow_lock(r, f"{flow_type}:{current_user.id}")
        raise HTTPException(status_code=500, detail=f"No se pudo encolar la tarea: {e}")

@router.get("/tasks/stream")
async def tasks_stream():
    r = get_redis()
    if not r:
        async def _noop():
             while True: 
                yield "event: keepalive\n" + "data: {}\n\n"
                await asyncio.sleep(15)
        return StreamingResponse(_noop(), media_type="text/event-stream")

    pubsub = r.pubsub()
    pubsub.subscribe("tasks_events")

    async def event_generator():
        try:
            yield "event: hello\n" + "data: {}\n\n"
            last_ping = time.time()
            while True:
                msg = pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if msg and msg.get("type") == "message":
                    data = msg.get("data")
                    if isinstance(data, (bytes, bytearray)): data = data.decode()
                    try:
                        js = json.loads(data)
                        ev_type = js.get("type") or "message"
                        yield f"event: {ev_type}\n" + f"data: {json.dumps(js)}\n\n"
                    except Exception:
                        yield "data: {}\n\n"
                now = time.time()
                if now - last_ping >= 10:
                    last_ping = now
                    yield ": keepalive\n\n"
                await asyncio.sleep(0.1)
        finally:
            try: pubsub.close() 
            except: pass

    headers = {"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"}
    return StreamingResponse(event_generator(), media_type="text/event-stream", headers=headers)

# /flows endpoints
@router.post("/flows/{task_id}/status")
def update_flow_status(
    task_id: str,
    body: FlowStatusUpdate,
    x_worker_token: str | None = Header(default=None, alias="X-Worker-Token"),
    db: Session = Depends(get_db),
):
    if not (settings.WORKER_TOKEN and x_worker_token and x_worker_token == settings.WORKER_TOKEN):
        raise HTTPException(status_code=401, detail="Unauthorized")
    flow = db.query(models.Flow).filter(models.Flow.task_id == task_id).first()
    if not flow:
        raise HTTPException(status_code=404, detail="Flow no encontrado")

    s = (body.status or "").lower().strip()
    if s: flow.status = s
    if body.name: flow.name = body.name
    if body.meta is not None: flow.meta = body.meta

    now = datetime.utcnow()
    flow.updated_at = now
    if flow.status in ("completed", "error"):
        flow.finished_at = now

    db.commit()
    return {"ok": True, "id": flow.id, "task_id": flow.task_id, "status": flow.status}

@router.get("/flows/history")
def flows_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    flows = db.query(models.Flow).filter(models.Flow.user_id == current_user.id).order_by(models.Flow.updated_at.desc()).limit(100).all()
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
