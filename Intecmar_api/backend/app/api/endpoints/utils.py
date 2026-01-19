import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.schemas.email import EmailSettings, SendEmailRequest
from backend.app.services.magazine.email_service import send_smtp_email
from backend.app.utils.files import ensure_outputs
from backend.app.db.session import get_db
from backend.app.db import models

from backend.app.services.core.storage import storage_service

router = APIRouter(tags=["Utilidades del Sistema"])

# Initialize templates
# Estructura del proyecto:
#   Intecmar_api/
#     backend/
#       app/api/endpoints/utils.py  (este archivo)
#     templates/                    (carpeta real de templates)
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
templates = Jinja2Templates(directory=os.path.join(_root, "templates"))

@router.get("/viewer", summary="Visor de PDF", description="Sirve la página del visor de PDF tipo flipbook.")
async def viewer_page(request: Request):
    """Sirve el visor de PDF tipo flipbook básico."""
    return templates.TemplateResponse("magazine/viewer.html", {"request": request})

@router.get("/minio/{bucket_type}/{path:path}", summary="Proxy MinIO", description="Proxy universal para descargar o visualizar archivos almacenados en MinIO.")
async def serve_minio_unified(bucket_type: str, path: str):
    """
    Proxy universal para MinIO.
    bucket_type: 'users', 'agent' (aunque ahora todo esté en intecmar-data).
    """
    from fastapi.responses import Response
    import mimetypes
    from urllib.parse import unquote
    
    # Decodificar caracteres como %40 (@)
    path = unquote(path)
    
    # Intentar descargar
    data = storage_service.download_file(path)
    
    if data is None:
        raise HTTPException(status_code=404, detail="Archivo no encontrado en MinIO")
    
    filename = path.split('/')[-1]
    mime_type, _ = mimetypes.guess_type(filename)
    if not mime_type:
        if filename.endswith('.md'): mime_type = "text/markdown"
        else: mime_type = "application/octet-stream"
        
    return Response(
        content=data,
        media_type=mime_type,
        headers={"Cache-Control": "max-age=3600"}
    )

@router.get("/minio_pdf/{user_email:path}/{filename}")
async def serve_minio_pdf(user_email: str, filename: str):
    return await serve_minio_unified("magazine", f"{user_email}/Magazines/{filename}")

@router.get("/minio_avatar/{user_email:path}/{filename}")
async def serve_minio_avatar(user_email: str, filename: str):
    return await serve_minio_unified("profile", f"{user_email}/profile_picture/{filename}")

@router.get("/minio_agent/{path:path}")
async def serve_minio_agent_asset(path: str):
    return await serve_minio_unified("agent", path)


@router.post("/upload_pdf", summary="Subir PDF temporal", description="Sube un archivo PDF al servidor para ser usado en el envío de correos.")
async def upload_pdf(pdf_file: UploadFile = File(...)):
    """Recibe un archivo PDF y lo guarda en outputs/uploads/ devolviendo su ruta relativa."""
    if not pdf_file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    upload_dir = settings.UPLOADS_DIR
    ensure_outputs(upload_dir)
    
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
    # Return relative path for frontend usage?
    # backend uses 'outputs/uploads/name.pdf'. Frontend usually prepends nothing if served statically?
    # main_api returns "outputs/uploads/name.pdf" (relative to CWD).
    # ensure consistency.
    rel_path = os.path.join("outputs", "uploads", safe_name).replace("\\", "/")
    return {"status": "success", "pdf_path": rel_path}

# Email Settings
@router.get("/email_settings", summary="Obtener ajustes de email", description="Devuelve la configuración de correo (remitente y favoritos) del sistema.")
async def get_email_settings(db: Session = Depends(get_db)):
    # Leer configuración desde BD; si no existe, usar DEFAULT_SENDER_EMAIL y lista vacía
    cfg = db.query(models.EmailConfig).first()
    if cfg is None:
        sender_email = settings.DEFAULT_SENDER_EMAIL
        favs = []
    else:
        sender_email = cfg.sender_email or settings.DEFAULT_SENDER_EMAIL
        favs = cfg.favorite_emails or []

    return {
        "sender_email": sender_email,
        "favorite_emails": favs,
        "sender": sender_email,
        "favorites": favs,
    }

@router.post("/email_settings")
async def save_email_settings(payload: EmailSettings, db: Session = Depends(get_db)):
    import re

    def _is_email(x: str) -> bool:
        return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", x or ""))

    sender_val = payload.sender_email or payload.sender or settings.DEFAULT_SENDER_EMAIL
    if not _is_email(sender_val):
        sender_val = settings.DEFAULT_SENDER_EMAIL
    favs_in = payload.favorite_emails if isinstance(payload.favorite_emails, list) else payload.favorites
    favs = [e for e in (favs_in or []) if _is_email(e)]

    cfg = db.query(models.EmailConfig).first()
    if cfg is None:
        cfg = models.EmailConfig(sender_email=sender_val, favorite_emails=favs)
        db.add(cfg)
    else:
        cfg.sender_email = sender_val
        cfg.favorite_emails = favs

    db.commit()

    return {"status": "ok"}

@router.post("/send_email", summary="Enviar email", description="Envía la revista digital mediante SMTP a una lista de destinatarios.")
async def send_email(payload: SendEmailRequest):
    import re
    if not payload.recipients:
        raise HTTPException(status_code=400, detail="Debes especificar al menos un destinatario")
    email_re = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    if not email_re.match(payload.sender or ""):
        raise HTTPException(status_code=400, detail="Remitente inválido")
    bad = [r for r in payload.recipients if not email_re.match(r)]
    if bad:
        raise HTTPException(status_code=400, detail=f"Destinatarios inválidos: {', '.join(bad)}")

    # Resolve PDF path logic
    # moved partially to here since it depends on input
    from urllib.parse import urlparse
    if payload.pdf_path:
        pdf_path = payload.pdf_path.lstrip("/")
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail=f"PDF no encontrado en servidor: {pdf_path}")
    else:
        # resolve from url
        if not payload.pdf_url:
            raise HTTPException(status_code=400, detail="pdf_url es requerido")
        parsed = urlparse(payload.pdf_url)
        path = parsed.path if parsed.scheme else payload.pdf_url
        if "/outputs/" in path:
            fname = path.split("/outputs/")[-1]
            pdf_path = os.path.join(settings.OUTPUTS_DIR, os.path.basename(fname))
        else:
            pdf_path = path.lstrip("/")
        if not os.path.exists(pdf_path):
             raise HTTPException(status_code=404, detail=f"PDF no encontrado en servidor: {pdf_path}")
    
    try:
        from backend.app.services.magazine.email_service import send_notification_email
        
        # Send to each recipient using the branded template
        for recipient in payload.recipients:
            title = "Revista Compartida"
            if payload.user_name:
                body = f"La persona <strong>{payload.user_name}</strong> te comparte la siguiente información sobre el magazine de convocatorias que te podrían interesar investigar."
            else:
                body = "Adjuntamos la revista de convocatorias que te podrían interesar investigar."
                
            send_notification_email(
                to_email=recipient,
                subject=payload.subject or "Revista de Convocatorias INTECMAR AI",
                title=title,
                body=body,
                attachments=[pdf_path]
            )
        return {"status": "sent"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando correo: {e}")
