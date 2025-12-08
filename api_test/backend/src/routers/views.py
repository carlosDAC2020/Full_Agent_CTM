import os
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Frontend"])

# Calculamos rutas relativas para encontrar los templates
# src/routers/views.py -> src/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Renderiza la interfaz gráfica"""
    return templates.TemplateResponse("index.html", {"request": request})