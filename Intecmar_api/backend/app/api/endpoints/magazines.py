import os
import io
from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.session import get_db
from backend.app.db import models
from backend.app.core.security import get_current_user
from backend.app.schemas.magazine import GenerateRequest, IdsRequest, SavedCreate
from backend.app.schemas.convocatoria import ConvocatoriaOut
from backend.app.services.magazine.redis_service import get_redis, task_key
from backend.app.services.magazine.agent_service import run_magazine_generation_stream
from backend.app.services.magazine.pdf_engine import generate_pdf
from backend.app.services.core.storage import storage_service
from backend.app.utils.files import load_json_list, save_json_dict

router = APIRouter(tags=["Revista Digital"])


@router.get("/stream_pdf", summary="Stream de PDF desde MinIO", description="Lee un PDF desde MinIO y lo transmite al navegador.")
async def stream_pdf(key: str):
    if not key:
        raise HTTPException(status_code=400, detail="Parámetro 'key' requerido")

    data = storage_service.download_file(key)
    if not data:
        raise HTTPException(status_code=404, detail="Archivo no encontrado en almacenamiento")

    return StreamingResponse(io.BytesIO(data), media_type="application/pdf")

# --- Saved Items ---
@router.get("/saved", summary="Listar mis favoritos", description="Obtiene la lista de convocatorias guardadas por el usuario actual.")
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


@router.get("/convocatorias", response_model=List[ConvocatoriaOut], summary="Listar todas las convocatorias", description="Devuelve todas las convocatorias detectadas y guardadas en la base de datos global.")
async def list_convocatorias(db: Session = Depends(get_db)):
    """Lista todas las convocatorias guardadas en la tabla 'convocatorias'."""
    rows = (
        db.query(models.Convocatoria)
        .order_by(
            models.Convocatoria.created_db_at.desc(),
            models.Convocatoria.created_at.desc().nullslast(),
        )
        .all()
    )
    return rows

@router.post("/saved", status_code=201, summary="Guardar favorito", description="Añade una convocatoria a la lista de favoritos del usuario.")
async def create_saved(payload: SavedCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not (payload.item_ref or "").strip():
        raise HTTPException(status_code=400, detail="item_ref requerido")
    # using 'item_metadata' as kwarg for model
    row = models.SavedItem(user_id=current_user.id, item_ref=payload.item_ref.strip(), item_metadata=payload.metadata or None)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id}

@router.delete("/saved/{saved_id}", status_code=204, summary="Eliminar favorito", description="Quita una convocatoria de la lista de favoritos del usuario.")
async def delete_saved(saved_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(models.SavedItem).filter(models.SavedItem.id == saved_id, models.SavedItem.user_id == current_user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(row)
    db.commit()
    return

# --- Magazines ---
@router.get("/magazines", summary="Listar mis revistas", description="Devuelve la lista de PDFs de revistas generadas por el usuario.")
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

@router.post("/generate", summary="Generar revista automática", description="Inicia un proceso asíncrono para buscar noticias/convocatorias y generar una revista basada en un tema.")
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

@router.post("/generate_pdf_from_ids", summary="Generar PDF desde selección", description="Crea un archivo PDF a partir de una lista específica de IDs de convocatorias.")
async def generate_pdf_from_ids(
    payload: IdsRequest,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        if not payload.ids:
            raise HTTPException(status_code=400, detail="Debes enviar al menos un ID")

        rows = (
            db.query(models.Convocatoria)
            .filter(models.Convocatoria.id.in_(payload.ids))
            .all()
        )

        if not rows:
            raise HTTPException(status_code=400, detail="No se encontraron convocatorias para los IDs enviados")

        # Convert SQLAlchemy objects to plain dicts compatible with PDF engine expectations
        selected = []
        for r in rows:
            item = {
                "id": r.id,
                "title": r.title,
                "description": r.description,
                "keywords": r.keywords or [],
                "source": r.source,
                "type": r.type,
                "url": r.url,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "fecha_inicio": r.fecha_inicio.isoformat() if r.fecha_inicio else None,
                "deadline": r.deadline.isoformat() if r.deadline else None,
                "fecha_cierre": r.fecha_cierre.isoformat() if r.fecha_cierre else None,
                "type_financy": r.type_financy,
                "monto": r.monto,
                "requisitos": r.requisitos or [],
                "beneficios": r.beneficios or [],
                "lugar": r.lugar,
            }
            selected.append(item)

        # Use Service
        pdf_path, pdf_name = generate_pdf(selected)
        
        user_folder = f"{current_user.email}/Magazines"
        object_key = f"{user_folder}/{pdf_name}"
        pdf_stream_path = f"/api/stream_pdf?key={object_key}"

        # Persist DB (incluyendo metadatos que antes iban al sidecar JSON)
        try:
            size_bytes = os.path.getsize(pdf_path) if pdf_path and os.path.exists(pdf_path) else None
            title = (payload.title or '').strip() or f"Magazine personalizado ({len(selected)} ítems)"
            row = models.Magazine(
                user_id=current_user.id,
                filename=pdf_name,
                title=title,
                size_bytes=size_bytes,
                selected_ids=[int(i) for i in (payload.ids or [])],
                meta={
                    "pdf_stream_path": pdf_stream_path,
                },
            )
            db.add(row)
            db.commit()
        except Exception as e:
            print(f"No se pudo guardar Magazine en DB: {e}")

        # Upload to MinIO en background (no bloquea la respuesta al usuario)
        try:
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()

                background_tasks.add_task(
                    storage_service.upload_file,
                    file_path_or_data=pdf_bytes,
                    object_key=object_key,
                )

                try:
                    os.remove(pdf_path)
                except Exception as cleanup_err:
                    print(f"No se pudo eliminar archivo temporal PDF: {cleanup_err}")
        except Exception as e:
            # No interrumpe la respuesta al usuario si falla el upload
            print(f"No se pudo subir el PDF a MinIO: {e}")
            
        # Rutas reales expuestas por la API (api_v1 se monta en /api)
        pdf_stream_url = pdf_stream_path
        viewer_url = f"/api/viewer?file={pdf_stream_url}"

        return {
            "status": "success", 
            "pdf_url": pdf_stream_url,
            "viewer_url": viewer_url,
        }
    except HTTPException: raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {e}")

# --- History ---
@router.get("/history", summary="Mi historial", description="Obtiene un historial unificado de revistas generadas y flujos de trabajo realizados.")
async def user_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Devuelve historial del usuario autenticado."""
    items: list[dict] = []
    
    # 1) Magazines
    try:
        rows = db.query(models.Magazine).filter(models.Magazine.user_id == current_user.id).order_by(models.Magazine.created_at.desc()).limit(20).all()
        for r in rows:
            # Construir URLs solo desde la BD (meta) y MinIO, sin tocar disco
            pdf_url = None
            viewer_url = None

            meta = r.meta or {}
            if isinstance(meta, dict):
                stream_path = meta.get("pdf_stream_path")
                if stream_path:
                    pdf_url = stream_path
                    viewer_url = f"/api/viewer?file={stream_path}"

            # Fallback para revistas antiguas sin meta
            if not pdf_url and r.filename:
                minio_url = f"/api/minio_pdf/{current_user.email}/{r.filename}"
                pdf_url = minio_url
                viewer_url = f"/api/viewer?file={minio_url}"
            
            items.append({
                "id": r.id,
                "name": r.title or r.filename or f"Magazine #{r.id}",
                "date": r.created_at.isoformat() if r.created_at else None,
                "status": "completed",
                "url": pdf_url,
                "viewer_url": viewer_url,
                "meta_url": None,
                "kind": "magazine",
                "selected_ids": r.selected_ids or [],
                "meta": meta,
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
