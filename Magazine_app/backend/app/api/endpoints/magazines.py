import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.session import get_db
from backend.app.db import models
from backend.app.core.security import get_current_user
from backend.app.schemas.magazine import GenerateRequest, IdsRequest, SavedCreate
from backend.app.services.redis_service import get_redis, task_key
from backend.app.services.agent_service import run_magazine_generation_stream
from backend.app.services.pdf_engine import generate_pdf
from backend.app.utils.files import load_json_list, save_json_dict

router = APIRouter()

# --- Saved Items ---
@router.get("/saved")
async def list_my_saved(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(models.SavedItem).filter(models.SavedItem.user_id == current_user.id).order_by(models.SavedItem.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "item_ref": r.item_ref,
            "metadata": r.item_metadata, # Accessing mapped column
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]

@router.post("/saved", status_code=201)
async def create_saved(payload: SavedCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not (payload.item_ref or "").strip():
        raise HTTPException(status_code=400, detail="item_ref requerido")
    # using 'item_metadata' as kwarg for model
    row = models.SavedItem(user_id=current_user.id, item_ref=payload.item_ref.strip(), item_metadata=payload.metadata or None)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id}

@router.delete("/saved/{saved_id}", status_code=204)
async def delete_saved(saved_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(models.SavedItem).filter(models.SavedItem.id == saved_id, models.SavedItem.user_id == current_user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(row)
    db.commit()
    return

# --- Magazines ---
@router.get("/magazines")
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

@router.post("/generate")
async def generate_magazine(req: GenerateRequest | None = None):
    """
    Endpoint para generar un magazine basado en un tema.
    """
    print(f"🔑 Clave de Gemini cargada: {bool(settings.GEMINI_API_KEY)}")
    try:
        tema = (req.tema if req and req.tema else settings.DEFAULT_TOPIC)
        print(f"📥 Generando magazine para tema: {tema}")
        
        result = await run_magazine_generation_stream(tema)
        
        pdf_path = result.get("pdf_path")
        pdf_url = None
        if pdf_path:
            # Normalize path for URL
            # Expected '/outputs/...' relative to mount?
            # result["pdf_path"] is usually absolute or relative to CWD?
            # agent usually saves to 'outputs/'.
            safe_path = pdf_path.replace('\\', '/')
            if not safe_path.startswith('/'): safe_path = '/' + safe_path
            pdf_url = safe_path

        contenido_curado = result.get("contenido_curado", [])

        # Try to associate IDs
        try:
            saved_items = load_json_list(settings.CONVOCATORIAS_FILE)
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

@router.post("/generate_pdf_from_ids")
async def generate_pdf_from_ids(
    payload: IdsRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        convocatorias_path = settings.CONVOCATORIAS_FILE
        if not os.path.exists(convocatorias_path):
             raise HTTPException(status_code=404, detail="Archivo convocatorias.json no encontrado")
             
        items = load_json_list(convocatorias_path)
        selected = [it for it in items if it.get("id") in payload.ids]
        
        if not selected:
             raise HTTPException(status_code=400, detail="No se encontraron convocatorias para los IDs enviados")

        # Use Service
        pdf_path, pdf_name = generate_pdf(selected)
        
        # Persist DB
        try:
            size_bytes = os.path.getsize(pdf_path)
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
            print(f"No se pudo guardar Magazine en DB: {e}")
            
        # Sidecar JSON
        try:
            sidecar_name = pdf_name[:-4] + 'json' if pdf_name.endswith('.pdf') else pdf_name + '.json'
            sidecar_path = os.path.join(settings.OUTPUTS_DIR, sidecar_name)
            meta = {
                "selected_ids": [int(i) for i in (payload.ids or [])],
                "title": title,
                "user_id": current_user.id,
                "created_at": datetime.utcnow().isoformat(),
                "pdf": f"/outputs/{pdf_name}",
            }
            save_json_dict(sidecar_path, meta)
        except Exception as e:
            print(f"No se pudo guardar sidecar JSON: {e}")
            
        return {
            "status": "success", 
            "pdf_url": f"/outputs/{pdf_name}", 
            "viewer_url": f"/viewer?file=/outputs/{pdf_name}"
        }
    except HTTPException: raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {e}")

# --- History ---
@router.get("/history")
async def user_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Devuelve historial del usuario autenticado."""
    items: list[dict] = []
    
    # 1) Magazines
    try:
        rows = db.query(models.Magazine).filter(models.Magazine.user_id == current_user.id).order_by(models.Magazine.created_at.desc()).limit(20).all()
        for r in rows:
            meta_url = None
            try:
                if r.filename and r.filename.lower().endswith('.pdf'):
                    sidecar = r.filename[:-4] + 'json'
                    if os.path.exists(os.path.join(settings.OUTPUTS_DIR, sidecar)):
                        meta_url = f"/outputs/{sidecar}"
            except Exception: pass
            
            items.append({
                "id": r.id,
                "name": r.title or r.filename or f"Magazine #{r.id}",
                "date": r.created_at.isoformat() if r.created_at else None,
                "status": "completed",
                "url": f"/outputs/{r.filename}" if r.filename else None,
                "meta_url": meta_url,
                "kind": "magazine",
            })
    except Exception: pass

    # 2) Flows
    try:
        flows = db.query(models.Flow).filter(models.Flow.user_id == current_user.id).order_by(models.Flow.updated_at.desc()).limit(30).all()
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
    except Exception: pass

    # 3) Active Tasks (Redis)
    r = get_redis()
    if r:
        try:
            ids = [tid.decode() if isinstance(tid, bytes) else tid for tid in r.smembers("active_tasks")]
            for tid in ids:
                h = r.hgetall(task_key(tid))
                if not h: continue
                kv = {}
                for k, v in h.items():
                   kv[k.decode() if isinstance(k, bytes) else k] = v.decode() if isinstance(v, bytes) else v
                
                try: uid = int(kv.get("user_id") or 0)
                except: uid = 0
                if uid != current_user.id: continue
                
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
        except Exception: pass
        
    return {"items": items[:30]}
