"""
Router para autenticación y gestión de usuarios.
Proporciona endpoint para obtener información del usuario autenticado.
"""
from fastapi import APIRouter, Depends
from src.core.auth import get_current_user
from backend.app.db.models import User

router = APIRouter(prefix="/api", tags=["Auth"])


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Retorna la información del usuario autenticado.
    Usado por el frontend para mostrar datos del usuario en el sidebar.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role
    }
