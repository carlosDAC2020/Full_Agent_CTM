import os
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.history import AgentSession

router = APIRouter(tags=["Frontend"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# --- RUTA 1: HOME (DASHBOARD) ---
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("views/home.html", {"request": request})

