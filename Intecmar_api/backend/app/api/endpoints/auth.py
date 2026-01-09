from datetime import datetime, timedelta
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.db import models
from backend.app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)
from backend.app.schemas import user as schemas
from backend.app.services.magazine.email_service import send_reset_password_email

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=schemas.User, status_code=201, summary="Registrar usuario", description="Crea un nuevo usuario administrador en el sistema.")
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    user = models.User(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        name=user_in.name or None,
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=schemas.Token, summary="Iniciar sesión", description="Autentica al usuario y devuelve un token JWT (Bearer).")
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token(user.email)
    return schemas.Token(access_token=token)

@router.get("/me", response_model=schemas.User, summary="Mi perfil", description="Obtiene la información del usuario autenticado actualmente.")
def me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.post("/forgot-password", status_code=200, summary="Recuperar contraseña", description="Envía un correo con un token de recuperación si el email existe.")
def forgot_password(payload: schemas.PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Genera un token de recuperación y envía un correo al usuario.
    Si el correo no existe, no retornamos error para evitar enumeración de usuarios.
    """
    email = payload.email
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if user:
        token = str(uuid.uuid4())
        # Token válido por 24 horas
        expires = datetime.utcnow() + timedelta(hours=24)
        
        user.reset_token = token
        user.reset_token_expires = expires
        db.commit()
        
        # Enviar correo (asíncrono idealmente, pero síncrono por ahora)
        send_reset_password_email(user.email, token)
    
    return {"message": "Si el correo existe, recibirás instrucciones para restablecer tu contraseña."}

@router.post("/reset-password", status_code=200, summary="Restablecer contraseña", description="Valida el token de recuperación y actualiza la contraseña del usuario.")
def reset_password(payload: schemas.PasswordResetConfirm, db: Session = Depends(get_db)):
    """
    Verifica el token y actualiza la contraseña.
    """
    token = payload.token
    user = db.query(models.User).filter(models.User.reset_token == token).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Token inválido")
        
    if user.reset_token_expires and user.reset_token_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="El token ha expirado")
        
    user.password_hash = get_password_hash(payload.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.add(user)
    db.commit()
    
    return {"message": "Contraseña actualizada correctamente"}
