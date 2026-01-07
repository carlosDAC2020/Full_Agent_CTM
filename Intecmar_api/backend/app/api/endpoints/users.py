import os
import shutil
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.db import models
from backend.app.core.security import get_current_user, verify_password, get_password_hash
from backend.app.core.config import settings
from backend.app.utils.files import ensure_outputs
from backend.app.schemas import user as schemas

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schemas.User)
def read_user_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.User)
def update_user_me(
    user_in: schemas.UserUpdate, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_in.name is not None:
        current_user.name = user_in.name
    if user_in.phone is not None:
        current_user.phone = user_in.phone
    if user_in.bio is not None:
        current_user.bio = user_in.bio
        
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/me/password", status_code=200)
def change_password(
    password_in: schemas.PasswordChange,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(password_in.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    
    if password_in.current_password == password_in.new_password:
        raise HTTPException(status_code=400, detail="La nueva contraseña no puede ser igual a la anterior")

    current_user.password_hash = get_password_hash(password_in.new_password)
    db.commit()
    return {"message": "Contraseña actualizada correctamente"}

@router.post("/me/profile-picture", response_model=schemas.User)
def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validar tipo de archivo
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
    
    # Directorio para guardar
    upload_dir = os.path.join(settings.OUTPUTS_DIR, "profile_pictures")
    ensure_outputs(upload_dir)
    
    # Nombre único
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{current_user.id}_{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join(upload_dir, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Guardar ruta relativa o URL
    # Asumimos que /outputs está montado en /outputs
    # Backend path: /outputs/profile_pictures/filename
    # Frontend URL: /outputs/profile_pictures/filename
    
    relative_path = f"/outputs/profile_pictures/{filename}"
    
    # Eliminar imagen anterior si existe
    if current_user.profile_picture and current_user.profile_picture.startswith("/outputs/"):
        old_path = current_user.profile_picture.replace("/outputs", settings.OUTPUTS_DIR, 1)
        # Solo eliminar si es un archivo local y no una URL externa
        if os.path.exists(old_path) and "profile_pictures" in old_path:
             try:
                 os.remove(old_path)
             except Exception:
                 pass

    current_user.profile_picture = relative_path
    db.commit()
    db.refresh(current_user)
    return current_user
