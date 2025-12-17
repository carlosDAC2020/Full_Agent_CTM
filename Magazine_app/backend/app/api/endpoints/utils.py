import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse, RedirectResponse

from backend.app.core.config import settings
from backend.app.schemas.email import EmailSettings, SendEmailRequest
from backend.app.services.email_service import send_smtp_email
from backend.app.utils.files import load_json_dict, save_json_dict, ensure_outputs

router = APIRouter()

@router.get("/viewer")
async def viewer_page():
    """Sirve el visor de PDF tipo flipbook básico (frontend/viewer.html)."""
    front_view = os.path.join("frontend", "viewer.html")
    if not os.path.exists(front_view):
        raise HTTPException(status_code=404, detail="viewer.html no encontrado")
    return FileResponse(front_view)

@router.post("/upload_pdf")
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
@router.get("/email_settings")
async def get_email_settings():
    raw = load_json_dict(settings.EMAIL_SETTINGS_FILE)
    sender_email = raw.get("sender_email") or raw.get("sender") or settings.DEFAULT_SENDER_EMAIL
    favs = raw.get("favorite_emails")
    if not isinstance(favs, list):
        favs = raw.get("favorites") if isinstance(raw.get("favorites"), list) else []
    
    return {
        "sender_email": sender_email,
        "favorite_emails": favs,
        "sender": sender_email,
        "favorites": favs,
    }

@router.post("/email_settings")
async def save_email_settings(payload: EmailSettings):
    import re
    def _is_email(x: str) -> bool:
        return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", x or ""))

    sender_val = payload.sender_email or payload.sender or settings.DEFAULT_SENDER_EMAIL
    if not _is_email(sender_val):
        sender_val = settings.DEFAULT_SENDER_EMAIL
    favs_in = payload.favorite_emails if isinstance(payload.favorite_emails, list) else payload.favorites
    favs = [e for e in (favs_in or []) if _is_email(e)]

    data = {
        "sender_email": sender_val,
        "favorite_emails": favs,
        "sender": sender_val,
        "favorites": favs,
    }
    save_json_dict(settings.EMAIL_SETTINGS_FILE, data)
    return {"status": "ok"}

@router.post("/send_email")
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
        send_smtp_email(
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
