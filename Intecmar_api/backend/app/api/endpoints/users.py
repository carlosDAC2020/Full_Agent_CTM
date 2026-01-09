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

router = APIRouter(prefix="/users", tags=["Usuarios"])

@router.get("/me", response_model=schemas.User, summary="Obtener mi perfil", description="Devuelve los datos detallados del usuario autenticado.")
def read_user_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.User, summary="Actualizar perfil", description="Permite modificar el nombre, teléfono y biografía del usuario.")
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

@router.put("/me/password", status_code=200, summary="Cambiar contraseña", description="Verifica la contraseña actual y establece una nueva.")
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

from backend.app.services.core.storage import storage_service

@router.post("/me/profile-picture", response_model=schemas.User, summary="Subir foto de perfil", description="Sube una imagen a MinIO y actualiza la URL en el perfil del usuario.")
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validar tipo de archivo
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
    
    # Leer datos
    file_data = await file.read()
    
    # Nombre único
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"avatar_{uuid.uuid4().hex}.{ext}"
    
    # Carpeta en MinIO (basada en email del usuario)
    folder = f"{current_user.email}/profile_picture"
    
    # Subir a MinIO
    object_key = f"{folder}/{filename}"
    key = storage_service.upload_file(
        file_path_or_data=file_data,
        object_key=object_key,
        content_type=file.content_type
    )
    
    if not key:
        raise HTTPException(status_code=500, detail="Error al subir la imagen a MinIO")
        
    # La nueva URL apunta al proxy de MinIO
    new_url = f"/api/minio_avatar/{current_user.email}/{filename}"
    
    # Si había una imagen local antigua, podríamos intentar limpiarla, 
    # pero el usuario pidió migrar a MinIO, así que priorizamos la nueva lógica.
    
    current_user.profile_picture = new_url
    db.commit()
    db.refresh(current_user)
    return current_user
